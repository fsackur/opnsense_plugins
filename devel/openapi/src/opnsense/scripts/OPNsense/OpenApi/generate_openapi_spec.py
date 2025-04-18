#! /usr/bin/env python3

"""
Build an OpenApi spec.

It's intended to be called by configd, but CLI args will be added.

Calls `parse_endpoints.py` and `parse_xml_models.py` if their cached JSON output is not found.
"""

import argparse
import os
import pathlib
from collections import defaultdict
from typing import Any, Dict, List, Literal, Tuple, TypeAlias, Callable, Generic, TypeVar, cast

import openapi_spec_validator as oasv
from apispec import APISpec

from parse_endpoints import Endpoint, Parameter, get_endpoints
from parse_endpoints import _DEFAULT_OUTPUT_FILE as _DEFAULT_ENDPOINT_OUTPUT_FILE
from parse_xml_models import XmlModel, XmlNode, get_models, _DEFAULT_SOURCE_FOLDER
from parse_xml_models import _DEFAULT_OUTPUT_FILE as _DEFAULT_MODEL_OUTPUT_FILE


SchemaDict =  Dict[str, "SchemaDict | str | bool | List[str | int]"]

K = TypeVar("K")
V = TypeVar("V")

class LazyDictionary(Generic[K, V]):

    __data: Dict[K, V] | None = None
    _func: Callable[[], Dict[K, V]] = dict

    def __init__(self, func: Callable[[], Dict[K, V]]):
        self.__data = None
        self._func = func

    @property
    def _data(self) -> Dict[K, V]:
        if self.__data is None:
            self.__data = self._func()
        return self.__data

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, name):
        return self._data.__getitem__(name)

    def __setitem__(self, name, value):
        return self._data.__setitem__(name, value)

    def __delitem__(self, name):
        return self._data.__delitem__(name)

    def __deepcopy__(self, memo):
        return self._data

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self._data)})"

    def __getattr__(self, name):
        # if name == "_func":
        #     return self._func
        if name in self.__dict__:
            return self.__dict__[name]
        return getattr(self._data, name)


BOOLEAN_SCHEMA: SchemaDict = {
    "type": "integer",
    "enum": [0, 1],
}


BASE_SCHEMAS = {
    "result": {
        "type": "object",
        "properties": {
            "result": {"type": "string"},
            "validations": {
            },
            "error": {"type": "string"},
            "changed": BOOLEAN_SCHEMA,
        },
        "required": ["result"],
        "additionalProperties": False,
    },

    "response": {
        "type": "object",
        "properties": {
            "response": {"type": "string"},
        },
        "required": ["response"],
        "additionalProperties": False,
    },

    "status": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["ok", "failed", "stopped", "disabled", "running", "unknown", "STUBBED RESPONSE"],  # TODO
            },
            "widget": {},
        },
        "required": ["status"],
        "additionalProperties": False,
    },

    "search.request": {
        "type": "object",
        "properties": {
            "rowCount": {"type": "integer"},
            "current": {"type": "integer"},
            "searchPhrase": {"type": "string"},
            "sort": {"type": "string", "enum": ["asc", "desc"]},
        },
        "additionalProperties": False,
    },

    "search.response": {
        "type": "object",
        "properties": {
            "total": {"type": "integer"},
            "rowCount": {"type": "integer"},
            "current": {"type": "integer"},
            "rows": {"items": {}},
        },
        "additionalProperties": True,
    },
}


# XML tags that are not properties
QUALIFIERS = [
    "Mask",  # regex pattern
    "ValidationMessage", # blah
    "Constraints", # more complex
    "MinimumValue",
    "MaximumValue",
    "Default",
    "default",
    "Required",
    "Multiple",
    "multiple",
    "BlankDesc",
    "Sorted",
    "NetMaskAllowed",
    "AllowDynamic",
    "FieldSeparator",
    "asList",
    "WildcardEnabled",
]


ARRAY_FIELD_TYPES = [
    "AliasField",
    "ArrayField",
    "CAsField",
    "CertificatesField",
    "ClientField",
    "ConnnectionField",
    "FilterRuleField",
    "GatewayField",
    "GroupField",
    "InstanceField",
    "NeighborField",
    "PolicyRulesField",
    "ServerField",
    "SourceNatRuleField",
    "SPDField",
    "TunableField",
    "VipField",
    "VTIField"
]


SELECTED_VALUE_FIELD_TYPES = [
    "CharonLogLevelField",
    "NetworkField",
    "HostnameField",
]


class ComponentRegistry:
    _models: Dict[str, XmlModel] = {}
    _components: Dict[str, SchemaDict] = BASE_SCHEMAS.copy()

    @classmethod
    def import_models(cls, models: List[XmlModel]):
        for model in models:
            cls._models[model.schema_path] = model

    @classmethod
    def register(cls, name: str) -> None:
        if name not in cls._components:
            model = cls._models[name]
            schema = get_model_spec(model)
            schema["x-config-xpath"] = model.mount_path  # type: ignore
            cls._components[name] = schema

    @classmethod
    def get(cls, name: str) -> SchemaDict:
        cls.register(name)
        return cls._components[name]

    @classmethod
    def dump(cls) -> Dict[str, SchemaDict]:
        keys = sorted(cls._components.keys())
        return {k: cls._components[k] for k in keys}

    @classmethod
    def resolve_property_path(cls, component_name: str, model_property_path: str) -> str:
        """Resolve a dot-dereference property path to a slash-separated component schema path"""
        path = component_name
        schema: SchemaDict = cls.get(component_name)

        if not model_property_path:
            return path

        known_schema_props = "properties", "items", "additionalProperties"
        breadcrumbs = model_property_path.split(".")
        while breadcrumbs:
            breadcrumb = breadcrumbs[0]

            if breadcrumb in known_schema_props:
                raise NotImplementedError(f"Need to handle searching for a property named '{breadcrumb}'")

            prop_found = False
            props_to_try = (breadcrumb, *known_schema_props)
            for prop in props_to_try:
                prop_found = prop in schema
                if prop_found:
                    schema = schema[prop]  # type: ignore
                    path = f"{path}/{prop}"

                    if prop == breadcrumb:
                        breadcrumbs = breadcrumbs[1:]
                    break

            if not prop_found:
                raise KeyError(f"could not find {breadcrumb} in {path}")

        return path


def get_selected_value_spec(node: XmlNode) -> SchemaDict:
    return {
        "type": "object",
        "properties": {
            "value": {"type": "string"},
            "selected": BOOLEAN_SCHEMA,
        },
        "required": ["value", "selected"],
        "additionalProperties": False,
        "x-xpath": node.xpath,
    }


def get_enum_value_spec(node: XmlNode) -> SchemaDict:
    spec = get_selected_value_spec(node)
    text = node.value
    if text is not None:
        spec["properties"]["value"]["enum"] = [text]  # type: ignore
    return spec


def get_relation_spec(node: XmlNode) -> SchemaDict:
    """Handle schema for ModelRelationField"""

    props = [child for child in node.children if child.name not in QUALIFIERS]
    if not props:
        raise ValueError(f"{node} has no properties")

    ref_schemas = []
    for prop in props:
        relation_props = {child_prop.name: child_prop.value for child_prop in prop.children}
        relation_model: str = relation_props["source"]  # type: ignore
        relation_model_path: str = relation_props['items']  # type: ignore
        display_prop: str = relation_props['display']  # type: ignore
        if "," in display_prop:  # only happens in swanctl
            display_prop = display_prop.split(",")[0]

        def resolver():
            path = ComponentRegistry.resolve_property_path(
                component_name=relation_model.lower(),
                model_property_path=f"{relation_model_path}.{display_prop}"
            )
            ref = f"#/components/schemas/{path}"
            return {"$ref": ref}

        ref_schemas.append(LazyDictionary(resolver))

    if len(ref_schemas) == 1:
        schema = ref_schemas[0]
    else:
        schema = {"oneOf": ref_schemas}

    spec = {
        "type": "object",
        "additionalProperties": {
            "type": "object",
            "properties": {
                "value": schema,
                "selected": {
                    "type": "integer",  # TODO: 0 or 1
                },
            },
            "additionalProperties": False,
        },
        "x-xpath": node.xpath,
    }
    return spec


def get_model_spec(node: XmlNode) -> SchemaDict:
    """
    Does the heavy lifting. The output becomes the schema for the request body or response, for
    endpoints that use this model.

    Looks like an XmlNode is one of:
    - a type (primitive/array/object)
    - the parent is an object and the node is a property
    - the parent is a property or primitive
    """
    spec: SchemaDict
    _props: SchemaDict

    allow_additional = False

    props: List[XmlNode] = []
    quals: List[XmlNode] = []
    for child in node.children:
        is_qual = child.name in QUALIFIERS
        is_qual = is_qual or (node.type == "LegacyLinkField" and child.name == "Source")
        if is_qual:
            quals.append(child)
            if child.name == "AllowDynamic":
                allow_additional = True
        else:
            props.append(child)

    has_single_child = len(props) == 1
    first_child: XmlNode = (props or [None])[0]  # type: ignore

    is_primitive = not any(props)
    is_array = any(q for q in quals if q.name == "Multiple")
    is_array = is_array or (has_single_child and first_child.type in ARRAY_FIELD_TYPES)

    if node.type == "ModelRelationField":
        if not (has_single_child and first_child.name == "Model"):
            raise ValueError(f"node {node.name} is expected to have a single child named Model")
        return get_relation_spec(first_child)

    elif node.type == "OptionField":
        if not has_single_child:
            raise ValueError("enum expected to be primitive")

        _props = {prop.name: get_enum_value_spec(prop) for prop in first_child.children}
        spec = {
            "type": "object",
            "properties": _props,
            "additionalProperties": False,
            "x-xpath": node.xpath,
        }

    elif node.type in SELECTED_VALUE_FIELD_TYPES:
        spec = {
            "type": "object",
            "additionalProperties": get_selected_value_spec(node),
            "x-xpath": node.xpath,
        }

    elif is_primitive:
        spec = {
            "type": "string",
            "x-xpath": node.xpath,
        }

    else:
        _props = {prop.name: get_model_spec(prop) for prop in props}
        spec = {
            "type": "object",
            "properties": _props,
            "additionalProperties": allow_additional,
            "x-xpath": node.xpath,
        }

    if is_array:
        spec = {
            "type": "array",
            "items": spec,
            "x-xpath": spec.pop("x-xpath"),
        }

    return spec


def get_path_parameter_spec(param: Parameter) -> SchemaDict:
    schema: SchemaDict = BOOLEAN_SCHEMA.copy() if param.type == "boolean" else {"type": param.type}
    if param.has_default:
        schema["default"] = param.default if param.default else {
            "boolean": 0,
            "integer": 0,
            "string": ""
        }[param.type]
    return {
        "in": "path",
        "name": param.name,
        "schema": schema,
        "required": True,  # to support optional path params, you need another operation without the param :-(
    }


def resolve_component_path(
    model: str | None,
    model_path_map: str | None,
) -> Tuple[str | None, str | None]:

    client_prop = None
    component_path = model

    if model and model_path_map:
        client_prop, model_path = model_path_map.split(":", maxsplit=1)
        component_path = ComponentRegistry.resolve_property_path(
            component_name=model,
            model_property_path=model_path,
        )

    return client_prop, component_path


def get_operation_content(
    model: str | None,
    model_path_map: str | None,
) -> SchemaDict:
    client_prop, component_path = resolve_component_path(model, model_path_map)

    if not component_path:
        schema: SchemaDict = {}
    else:
        schema = {"$ref": f"#/components/schemas/{component_path}"}
        if client_prop:
            schema = {
                "type": "object",
                "properties": {
                    client_prop: schema,
                }
            }

    return {
        "application/json": {
            "schema": schema
        },
    }


def get_operation(endpoint: Endpoint) -> SchemaDict:
    method = endpoint.method.lower()

    content = get_operation_content(endpoint.response_model, endpoint.model_path_map)
    responses = {
        "200": {
            "description": endpoint.description,
            "content": content,
        },
    }

    op = {
        "operationId": endpoint.operation_id,
        "responses": responses,
    }

    if endpoint.parameters:
        op["parameters"] = [get_path_parameter_spec(p) for p in endpoint.parameters]

    if method == "post":
        content = get_operation_content(endpoint.request_model, endpoint.model_path_map)
        op["requestBody"] = {
            "required": endpoint.requires_body,
            "content": content,
        }

    return {method: op}


def get_spec(models: List[XmlModel], endpoints: List[Endpoint]) -> APISpec:
    spec = APISpec(
        title="OPNsense API",
        version="25.1",
        openapi_version="3.1.0",
        info={"description": "API for managing your OPNsense firewall"},
    )

    ComponentRegistry.import_models(models)

    model_names = set()
    for ep in endpoints:
        model_names.add(ep.response_model)
        model_names.add(ep.request_model)
    model_names.remove(None)

    for name in model_names:  # type: ignore
        ComponentRegistry.register(cast(str, name))

    components = ComponentRegistry.dump()
    for name, component in components.items():
        spec.components.schema(name, component)

    for endpoint in endpoints:
        operation = get_operation(endpoint)
        spec.path(path=endpoint.path, description=endpoint.description, operations=operation)

    return spec


def validate_spec(spec: APISpec):
    from referencing import Resource
    from referencing.exceptions import Unresolvable
    try:
        oasv.validate_spec(spec.to_dict())  # type: ignore
    except KeyboardInterrupt:
        raise
    except Unresolvable as ex:
        args = []
        for arg in ex.args:
            if isinstance(arg, Resource):
                contents = str(arg.contents)
                if len(contents) > 400:
                    contents = f"{contents[0:400]}..."
                arg = arg.__class__(contents=contents, specification=arg._specification)
            args.append(arg)
        raise ex.__class__(*args).with_traceback(None) from None
    except Exception as ex:
        msg = str(ex)
        if len(msg) > 400:
            msg = f"{msg[0:400]}..."
        raise Exception(msg).with_traceback(None) from None


def test_spec(models: List[XmlModel], endpoints: List[Endpoint]):
    models_by_name = {m.schema_path: m for m in models}
    from itertools import groupby
    endpoints = endpoints.copy()
    key = lambda ep: ep.model or ""
    endpoints.sort(key=key)

    failed = False
    for model_name, eps in groupby(endpoints, key=key):
        spec = get_spec([], [])
        model = models_by_name.get(model_name)
        if model:
            component = get_model_spec(model)
            spec.components.schema(model.schema_path, component)
            try:
                validate_spec(spec)
            except Exception as ex:
                print(component)
                print(ex)
                failed = True
                break

        for endpoint in eps:
            operation = get_operation(endpoint)
            spec.path(path=endpoint.path, description=endpoint.description, operations=operation)
        try:
            validate_spec(spec)
        except Exception as ex:
            print(endpoint)
            print(ex)
            failed = True
            break

    if failed:
        raise Exception("Failed validation")


def generate_openapi_spec(
    source_folder: str,
    should_validate: bool = False,
    module: str | None = None,
    controller: str | None = None,
    cache_folder: str | None = None,
) -> APISpec:

    endpoint_json_path = f"{cache_folder}/{_DEFAULT_ENDPOINT_OUTPUT_FILE}" if cache_folder else None
    model_json_path = f"{cache_folder}/{_DEFAULT_MODEL_OUTPUT_FILE}" if cache_folder else None

    endpoints = get_endpoints(source_folder, json_path=endpoint_json_path)
    if module:
        endpoints = [ep for ep in endpoints if ep.module.lower() == module.lower()]
    if controller:
        endpoints = [ep for ep in endpoints if ep.controller.lower() == controller.lower()]

    models = get_models(source_folder, json_path=model_json_path)

    spec = get_spec(models, endpoints)

    # validation is slow
    if should_validate:
        validate_spec(spec)

    return spec


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="generate an OpenApi spec")
    parser.add_argument("-s", "--source-folder", default=_DEFAULT_SOURCE_FOLDER)
    parser.add_argument("-o", "--output-file", default="openapi.yml")
    parser.add_argument("-m", "--module", help="filter endpoints by module")
    parser.add_argument("-c", "--controller", help="filter endpoints by controller name (excluding Controller suffix)")
    parser.add_argument("--cache-folder", default=None)
    parser.add_argument("-v", "--validate", action="store_true")
    args = parser.parse_args()

    output_file: str = os.path.realpath(args.output_file)

    spec = generate_openapi_spec(
        source_folder=args.source_folder,
        should_validate=args.validate,
        module=args.module,
        controller=args.controller,
        cache_folder=os.path.realpath(args.cache_folder) if args.cache_folder else None,
    )

    output_file_ext = output_file.split(".")[-1]
    if output_file_ext.lower() in ("yml", "yaml"):
        content = spec.to_yaml()
    else:
        import json
        content = json.dumps(spec.to_dict())

    pathlib.Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as file:
        file.write(content)
