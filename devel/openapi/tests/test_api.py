#! /usr/bin/env python3

import sys
import os
from io import BytesIO
import csv
from pprint import pprint, pformat
from typing import Dict, Any, Literal, Hashable, Mapping, Tuple
from xml.etree.ElementTree import Element as XmlElement
from xml.etree.ElementTree import ElementTree, XML
import pytest
from pytest import mark, param
from unittest.mock import ANY
from openapi_schema_validator import validate, OAS31Validator
from referencing import Registry, Resource
from jsonschema.exceptions import _Error, SchemaError, ValidationError, best_match

from fixtures import *
from urls import urls

StrDict = Dict[str, Any]


if "--url" in sys.argv:
    index = sys.argv.index("--url")
    url_arg = sys.argv[index + 1]
    filters = re.split(r",\s*|\s+", url_arg)
    _urls = []
    for f in filters:
        _urls.extend(u for u in urls if f in u)
    urls = sorted(set(_urls))

if "--slice" in sys.argv:
    index = sys.argv.index("--slice")
    _slice = sys.argv[index + 1]
    urls = eval(f"urls{_slice}")

log_path = None
if "--log-path" in sys.argv:
    index = sys.argv.index("--log-path")
    log_path = sys.argv[index + 1]
    if not os.path.isabs(log_path):
        log_path = f"{os.path.dirname(__file__)}/{log_path}"


import logging
logger = logging.getLogger(os.path.basename(__file__).replace(".py", ""))
if log_path:
    try:
        os.remove(log_path)
    except FileNotFoundError:
        pass
    handler = logging.FileHandler(log_path)
else:
    handler = logging.StreamHandler(sys.stdout)

# handler.addFilter(LastPartFilter())
formatter = logging.Formatter('%(name)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def dump_xml(node: XmlElement):
    if node is None:
        return ""
    stream = BytesIO()
    tree = ElementTree(node)
    tree.write(stream)
    stream.seek(0)
    return stream.read().decode().strip()


def format_validation_error(ex: ValidationError, response_body, schema, model_xml_registry: ElementFetcher):
    _model = response_body
    model_path = ""
    for prop in ex.path:
        _model = _model[prop]
        model_path = f"{model_path}.{prop}"

    _schema = schema
    xpath = _schema.get("x-xpath", "")
    schema_path = ""
    for prop in ex.schema_path:
        _schema = _schema[prop]
        schema_path = f"{schema_path}.{prop}"
        if isinstance(_schema, (Dict, Mapping)):
            xpath = _schema.get("x-xpath", xpath)

    node = model_xml_registry(xpath) if xpath else None
    xml = "no_xml" if node is None else re.sub(r"\n\s*", "", dump_xml(node))

    return (
        f"{model_path}: {pformat(_model)}",
        f"{schema_path}: {_schema}",
        xml
    )


def log_validation_error(ex, response_body, schema, model_name, model_xml_registry, logger):
    response, schema, xml = format_validation_error(ex, response_body, schema, model_xml_registry)
    logger.getChild("message").error(ex.message)
    logger.getChild("response").error(response)
    logger.getChild(f"schema.{model_name}").error(schema)
    logger.getChild("xml").error(xml)


def assert_against_standard_validator(response_body, schema, model_name, model_xml_registry: ElementFetcher, logger=logger):
    try:
        validate(response_body, schema)
        logger.info(f"pass")
    except Exception as ex:
        logger.error(f"{ex.__class__.__name__}: {ex.args[0]}")
        if isinstance(ex, ValidationError):
            log_validation_error(ex, response_body, schema, model_name, model_xml_registry, logger)
        else:
            logger.exception(ex)
        raise


def validate_all(response_body, schema, model_name, model_xml_registry: ElementFetcher, logger=logger):
    validator = OAS31Validator(schema)
    errors = list(validator.iter_errors(response_body))
    if errors:
        for ex in errors:
            log_validation_error(ex, response_body, schema, model_name, model_xml_registry, logger)
        raise best_match(errors)
    else:
        logger.getChild("message").info("pass")

urls = ["/firewall/alias/additem"]

@mark.parametrize("url", urls)
def test_endpoint(url, spec, api, get_node: ElementsFetcher, model_xml_registry: ElementFetcher, logger=logger):
    logger = logger.getChild("test_endpoint")
    logger = logger.getChild(url)
    method_op = spec._paths[url]
    for method, op in [(k, v) for k, v in method_op.items() if k in ("get", "post")]:
        schema = next(iter(op["responses"]["200"]["content"].values()))["schema"]
        schema, model_name, model_path = resolve_schema(schema, spec.components.schemas)

        body_schema = None
        if "requestBody" in op and op["requestBody"]["required"]:
            body_schema = op["requestBody"]["content"]["application/json"]["schema"]
            body_schema, _, _ = resolve_schema(body_schema, spec.components.schemas)
            # logger.getChild("body_schema").info(body_schema)
            body = create_body(body_schema)
            logger.getChild("body").info(body)

        model = spec.components.schemas.get(model_name, {})
        params = op.get("parameters", [])
        path_params = supply_params(get_node, params, model, model_path or "")

        try:
            response = api.call(method, url, path_params, data=body)
            response.raise_for_status()

            content_type = response.headers['content-type'].split(';')[0].lower()
            logger.getChild("content").info(content_type)

            if content_type == "application/json":
                response_body = response.json()
            elif content_type == "text/csv":
                response_body = read_csv(response.text)
            else:
                response_body = response.text
            print("\n", response_body)
        except Exception as ex:
            logger.getChild("message").error(ex)

        # print(f"response = {response_body}")
        # print(f"schema = {schema}")
        # assert_against_standard_validator(response_body, schema, url, model_name)
        validate_all(response_body, schema, model_name, model_xml_registry, logger)


def resolve_schema(schema: StrDict, components: StrDict): #-> Tuple[StrDict, str | None]:
    model_name = None
    model_path = None

    _schema = schema.copy()

    ref: str | None = _schema.pop("$ref", None)
    if ref is not None:
        model_parts = ref.replace("#/components/schemas/", "")
        if "/" in model_parts:
            model_name, model_path = model_parts.split("/", maxsplit=1)
        else:
            model_name, model_path = model_parts, None

        _schema = components[model_name]
        if model_path:
            breadcrumbs = model_path.split("/")
            for breadcrumb in breadcrumbs:
                _schema = _schema[breadcrumb]

    for k, v in _schema.items():
        if isinstance(v, Mapping):
            v, _model_name, _model_path = resolve_schema(v, components)
            model_name = model_name or _model_name
            model_path = model_path or _model_path
        _schema[k] = v
    return _schema, model_name, model_path


def create_body(schema: StrDict):
    schema = schema.copy()
    _type = schema.pop("type")
    if _type == "object" and "properties" in schema:
        body = {}
        for k in schema.get("required", []): #schema["properties"].keys()):
            body[k] = create_body(schema["properties"][k])
        return body
    elif _type == "object":
        raise NotImplementedError(f"Not expecting associative array in {schema}")
    elif _type == "array":
        return [create_body(schema["items"])]
    else:
        for k in "default", "minimum", "maximum":
            if k in schema:
                return schema[k]
        if "enum" in schema:
            return schema["enum"][0]
        if _type == "string":
            return "foo"
        return 42


def supply_params(get_node: ElementsFetcher, schema_params: List[Dict], model: Dict, model_path: str = ""):
    nodes = []
    kwargs = {}
    if schema_params:
        xpath = model.get("x-config-xpath", None)
        if xpath:
            if model_path:
                x_model_path = model_path.replace("properties/", "").replace("items/", "")
                xpath = f"{xpath}/{x_model_path}"
            nodes = get_node(xpath)
        attrib = nodes[0].attrib if nodes else {}

        for param in schema_params:
            name = param["name"]
            value = attrib[name] if name in attrib else param["schema"].get("default")
            kwargs[name] = value
    return kwargs


def read_csv(content: str):
    lines = content.split("\n")
    reader = csv.DictReader(lines)
    return list(reader)
