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
from typing import Any, Dict, List, Literal, Tuple, TypeAlias, Callable

import openapi_spec_validator as oasv
from apispec import APISpec

from parse_endpoints import Endpoint, Parameter, get_endpoints
from parse_endpoints import _DEFAULT_OUTPUT_FILE as _DEFAULT_ENDPOINT_OUTPUT_FILE
from parse_xml_models import XmlModel, XmlNode, get_models, _DEFAULT_SOURCE_FOLDER
from parse_xml_models import _DEFAULT_OUTPUT_FILE as _DEFAULT_MODEL_OUTPUT_FILE


SchemaDict =  Dict[str, "SchemaDict | str | bool | List[str]"]



BOOLEAN_SCHEMA = {
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
    # "BaseListField",
    # "GroupMembershipField",
    # "MemberField",
    # "PrivField",
    # "AuthenticationServerField",
    # "AuthGroupField",
    # "CertificateField",
    # "ConfigdActionsField",
    # "CountryField",
    # "InterfaceField",
    # "JsonKeyValueStoreField",
    # "ModelRelationField",
    # "NetworkAliasField",
    # "OptionField",
    # "PortField",
    # "ProtocolField",
    # "VirtualIPField",
    # "InterfaceField",
    # "InterfaceField",
    # "ScheduleField",
    # "TosField",
    # "PolicyContentField",
    "CharonLogLevelField",
    # "IPsecProposalField",
    # "PoolsField",
    # "LaggInterfaceField",
    # "VipInterfaceField",
    # "VlanInterfaceField",
    # "OpenVPNServerField",
    # "UnboundInterfaceField",
]


def get_enum_value_spec(text: str | None = None) -> SchemaDict:
    value: SchemaDict = {"type": "string"}
    if text is not None:
        value["enum"] = [text]

    return {
        "type": "object",
        "properties": {
            "value": value,
            "selected": BOOLEAN_SCHEMA,
        },
        "required": ["value", "selected"]
    }


def get_relation_spec(node: XmlNode) -> SchemaDict:
    """Handle schema for ModelRelationField"""

    props = [child for child in node.children if child.name not in QUALIFIERS]
    refs = []
    for child in props:
        relation_props = {prop.name: prop.value for prop in child.children}
        relation_model: str = relation_props["source"]  # type: ignore
        ref = f"#/components/schemas/{relation_model.lower()}"
        ref = f"{ref}/items/properties/{relation_props['items']}"  # we know that the related model will be array, so look in 'items' subschema
        ref = f"{ref}/properties/{relation_props['display']}"
        refs.append(ref)

    if len(refs) == 1:
        schema = {"$ref": refs[0]}
    else:
        schema = {"oneOf": [{"$ref": ref} for ref in refs]}

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
        }
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
    is_selected_value_dict = node.type in SELECTED_VALUE_FIELD_TYPES


    if node.type == "ModelRelationField":
        if not (has_single_child and first_child.name == "Model"):
            raise ValueError(f"node {node.name} is expected to have a single child named Model")
        return get_relation_spec(first_child)

    elif node.type in ("NetworkField", "HostnameField"):
        spec = {
            "type": "object",
            "additionalProperties": get_enum_value_spec(),
        }

    elif node.type == "OptionField":
        if not has_single_child:
            raise ValueError("enum expected to be primitive")

        _props = {prop.name: get_enum_value_spec(prop.value) for prop in first_child.children}
        spec = {
            "type": "object",
            "properties": _props,
            "additionalProperties": False,
        }

    elif is_selected_value_dict:
        spec = {
            "type": "object",
            "additionalProperties": get_enum_value_spec(),
        }

    elif is_primitive:
        spec = {
            "type": "string",
        }

    else:
        _props = {prop.name: get_model_spec(prop) for prop in props}
        spec = {
            "type": "object",
            "properties": _props,
            "additionalProperties": allow_additional,
        }

    if is_array:
        spec = {
            "type": "array",
            "items": spec,
        }

    return spec


def get_path_parameter_spec(param: Parameter) -> SchemaDict:
    return {
        "in": "path",
        "name": param.name,
        "schema": {"type": "string"},  # TODO
        "required": True,  # to support optional path params, you need another operation without the param :-(
    }


def resolve_component_path(
    model: str | None,
    model_path_map: str | None,
    component_schemas: Dict[str, Dict],
) -> Tuple[str | None, str | None]:

    client_prop = None
    component_path = model

    if model and model_path_map:
        tree: Dict[str, Dict] = component_schemas.get(model)  # type: ignore

        client_prop, model_path = model_path_map.split(":", maxsplit=1)
        breadcrumbs = model_path.split(".") if model_path else []

        while breadcrumbs:
            prop = breadcrumbs[0]
            if "properties" in tree:
                tree = tree["properties"][prop]
                component_path = f"{component_path}/properties/{prop}"
                breadcrumbs = breadcrumbs[1:]
            elif "items" in tree:
                tree = tree["items"]
                component_path = f"{component_path}/items"
                # still on the same breadcrumb; go round again
            else:
                raise KeyError(f"could not find {prop} in {component_path}")

    return client_prop, component_path


def get_operation_content(
    model: str | None,
    model_path_map: str | None,
    component_schemas: Dict[str, Dict],
) -> SchemaDict:
    client_prop, component_path = resolve_component_path(model, model_path_map, component_schemas)

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


def get_operation(endpoint: Endpoint, component_schemas: Dict[str, Dict]) -> SchemaDict:
    method = endpoint.method.lower()

    content = get_operation_content(endpoint.response_model, endpoint.model_path_map, component_schemas)
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
        content = get_operation_content(endpoint.request_model, endpoint.model_path_map, component_schemas)
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

    for name, schema in BASE_SCHEMAS.items():
        spec.components.schema(name, schema)

    for model in models:
        component = get_model_spec(model)
        component["x-mount"] = model.mount  # type: ignore
        spec.components.schema(model.schema_path, component)

    for endpoint in endpoints:
        operation = get_operation(endpoint, spec.components.schemas)
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
            operation = get_operation(endpoint, spec.components.schemas)
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
    model_names = set()
    for ep in endpoints:
        model_names.add(ep.response_model)
        model_names.add(ep.request_model)
    models = [m for m in models if m.schema_path in model_names]

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
