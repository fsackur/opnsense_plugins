#! /usr/bin/env python3

"""
Build a dataclass for each API endpoint. These become "operations" in OpenApi spec.

Called by `generate_openapi_spec.py`.
"""

import json
import os
import pathlib
import argparse
import re
import subprocess
from collections import defaultdict
from typing import Any, Dict, List, Literal, Self, TypeAlias, TypedDict, Tuple
from pydantic import BaseModel

from parse_xml_models import get_openapi_schema_path, _DEFAULT_SOURCE_FOLDER


_DEFAULT_OUTPUT_FILE = "endpoints.json"

HttpMethod: TypeAlias = Literal["GET"] | Literal["POST"]

PHP_TO_SPEC_TYPE_MAP = {
    "array": "array",
    "array|null": "array",
    "bool": "boolean",
    "int": "integer",
    "integer": "integer",
    "int|string": "integer",
    "string|int": "integer",
}
PHP_TO_SPEC_TYPE_MAP = defaultdict(lambda: "string", PHP_TO_SPEC_TYPE_MAP)


#region DTOs from ParseControllers.php
# This is, approximately, raw php Reflection.
# TypedDict does not validate; this will not throw. It's only here for linting.
class PhpParameter(TypedDict):
    name: str
    has_default: bool
    default: Any

class ModelDict(TypedDict):
    request_model: str | None
    response_model: str | None

class PhpMethod(ModelDict):
    name: str
    method: HttpMethod
    parameters: List[PhpParameter]
    doc: str | Literal[False]
    requires_body: bool
    model_path_map: str | None

class PhpController(TypedDict):
    name: str
    methods: List[PhpMethod]
    model: str | None
    model_name: str | None
    is_abstract: bool
    doc: str | Literal[False]
#endregion DTOs from ParseControllers.php


class DocComment(BaseModel):
    description: str
    param_descriptions: Dict[str, str]
    param_types: Dict[str, str]

    @classmethod
    def from_php(cls, doc: str) -> Self:
        lines = [l.strip() for l in doc.split("\n")]
        lines = [re.sub(r"^\*\s*", "", l) for l in lines if l not in ("/**", "/*", "*/")]

        descr_lines = []
        param_descr = {}
        param_types = {}
        pattern = re.compile(r"@param\s+(?P<type>\S*)\s*\$(?P<name>\S+)\s*(?P<descr>.*)")
        for line in lines:
            if not line.startswith("@"):
                descr_lines.append(line)
                continue

            m = pattern.match(line)
            if m:
                param_descr[m.group("name")] = m.group("descr")
                param_types[m.group("name")] = m.group("type") or ""

        return cls(
            description=" ".join(descr_lines),
            param_descriptions=param_descr,
            param_types=param_types,
        )


class Parameter(BaseModel):
    name: str
    type: str
    description: str
    has_default: bool
    default: Any

    def __repr__(self):
        if self.has_default:
            default = "null" if self.default is None else str(self.default)
            return f"{self.name}={default}"
        return self.name


class Endpoint(BaseModel):
    """
    In OpenApi terms, this is an "operation", but "endpoint" seems more descriptive.

    Most important part of OpenApi spec. If we skip models, we can still get a spec
    with just this data (but good luck with post requests!)

    OpenApi spec defines "response" (and, optionally, "request") for models.
    Here, "model" is a placeholder. End goal is to stick models into "components".
    """

    description: str
    module: str
    controller: str
    name: str
    method: HttpMethod
    parameters: List[Parameter]
    request_model: str | None
    response_model: str | None
    requires_body: bool
    model_path_map: str | None

    @property
    def path(self) -> str:
        path = f"/{self.module}/{self.controller}/{self.name}".lower()
        params = [f"{{{p.name}}}" for p in self.parameters]
        return "/".join([path] + params)

    @property
    def operation_id(self) -> str:
        name = self.name[0].capitalize() + self.name[1:]
        return f"{self.module}{self.controller}{name}"

    def __repr__(self):
        return self.path


def get_controller_url_segments(class_name: str) -> Tuple[str, str]:
    """Expects, e.g. OPNsense\\Proxy\\Api\\AclController"""
    segments = class_name.split("\\")
    return segments[-3], segments[-1].replace("Controller", "")


def parse_endpoints(ctrl: PhpController) -> List[Endpoint]:

    endpoints = []
    model_name = ctrl["model_name"]
    module, controller_name = get_controller_url_segments(ctrl["name"])

    php_methods = ctrl["methods"]
    for php_method in php_methods:
        models: ModelDict = {}  # type: ignore

        for key in ("request_model", "response_model"):
            model = php_method[key] or ctrl["model"]
            if model and "\\" in model:
                vendor, _module, name = model.split("\\")
                model = get_openapi_schema_path(vendor, _module, name)
            models[key] = model

        model_path_map = php_method["model_path_map"]
        if model_path_map and "static::$internalModelName" in model_path_map:
            if not model_name:
                raise ValueError(f"{ctrl["name"]}.{php_method["name"]}Action does not declare $internalModelName")
            model_path_map = model_path_map.replace("static::$internalModelName", model_name)
        elif model_name and not model_path_map:
            model_path_map = model_name + ":"

        doc = php_method.get("doc") or ""
        comment = DocComment.from_php(doc)

        params = []
        for php_param in php_method["parameters"]:
            description = comment.param_descriptions.get(php_param["name"], "")
            php_type = comment.param_types.get(php_param["name"], "")
            if php_param["has_default"] and not php_type:
                php_type = type(php_param["default"]).__name__

            param = Parameter(
                description=description,
                type=PHP_TO_SPEC_TYPE_MAP[php_type],
                **php_param
            )
            params.append(param)

        endpoint = Endpoint(
            description=comment.description,
            module=module,
            controller=controller_name,
            name=php_method["name"],
            method=php_method["method"],
            parameters=params,
            **models,
            requires_body=php_method["requires_body"],
            model_path_map=model_path_map,
        )
        endpoints.append(endpoint)

    return endpoints


def get_controllers(source_folder: str) -> List[PhpController]:
    """Call ParseControllers.php"""

    script_dir = os.path.dirname(__file__)
    php_script_path = f"{script_dir}/ParseControllers.php"

    php_result = subprocess.run(["php", php_script_path, "-s", source_folder], capture_output=True)
    if php_result.returncode:
        print(php_result.stdout.decode())
        raise subprocess.SubprocessError(php_result.stderr.decode())

    php_controllers: List[PhpController] = json.loads(php_result.stdout)
    return [ctrl for ctrl in php_controllers if not ctrl["is_abstract"]]


def get_endpoints(source_folder=_DEFAULT_SOURCE_FOLDER, json_path: str | None = None) -> List[Endpoint]:

    if json_path and os.path.isfile(json_path):
        with open(json_path) as file:
            endpoint_json = file.read()
        _endpoints = json.loads(endpoint_json)
        endpoints = [Endpoint(**ep) for ep in _endpoints]
        return endpoints

    endpoints = []
    for controller in get_controllers(source_folder):
        endpoints.extend(parse_endpoints(controller))

    if json_path:
        endpoint_json = json.dumps([ep.dict() for ep in endpoints])
        pathlib.Path(json_path).parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w") as file:
            file.write(endpoint_json)

    return endpoints


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="parse OpenApi endpoints")
    parser.add_argument("-s", "--source-folder", default=_DEFAULT_SOURCE_FOLDER)
    parser.add_argument("-o", "--output-file", default=None)
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    source_folder = os.path.realpath(args.source_folder)
    output_file = os.path.realpath(args.output_file) if args.output_file else None
    quiet = args.quiet

    endpoints = get_endpoints(source_folder=source_folder, json_path=output_file)

    if not quiet:
        from pprint import pprint
        pprint(endpoints)
