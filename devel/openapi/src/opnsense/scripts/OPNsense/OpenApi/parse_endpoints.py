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
from typing import Any, Dict, List, Literal, Self, TypeAlias, TypedDict
from pydantic import BaseModel

from parse_xml_models import get_openapi_schema_path, _DEFAULT_SOURCE_FOLDER


_DEFAULT_OUTPUT_FILE = "endpoints.json"

HttpMethod: TypeAlias = Literal["GET"] | Literal["POST"]

#region DTOs from ParseControllers.php
# This is, approximately, raw php Reflection.
# TypedDict does not validate; this will not throw. It's only here for linting.
class PhpParameter(TypedDict):
    name: str
    has_default: bool
    default: Any

class PhpMethod(TypedDict):
    name: str
    method: HttpMethod | Literal["*"]
    parameters: List[PhpParameter]
    doc: str | Literal[False]
    requires_body: bool
    model_path_map: str | None

class PhpController(TypedDict):
    name: str
    methods: List[PhpMethod]
    model: str | None
    is_abstract: bool
    doc: str | Literal[False]
#endregion DTOs from ParseControllers.php


#region intermediate DTOs
# These do validation and throw nice errors. The errors are why they exist.
class DocComment(BaseModel):
    description: str
    param_descriptions: Dict[str, str]

    @classmethod
    def from_php(cls, doc: str) -> Self:
        lines = [l.strip() for l in doc.split("\n")]
        lines = [re.sub(r"^\*\s*", "", l) for l in lines if l not in ("/**", "/*", "*/")]

        descr_lines = []
        param_descr = {}
        pattern = re.compile(r"@param\s+(?P<type>\S*)\s*\$(?P<name>\S+)\s*(?P<descr>.*)")
        for line in lines:
            if not line.startswith("@"):
                descr_lines.append(line)
                continue

            m = pattern.match(line)
            if m:
                param_descr[m.group("name")] = m.group("descr")

        return cls(
            description=" ".join(descr_lines),
            param_descriptions=param_descr,
        )


class Parameter(BaseModel):
    name: str
    description: str
    has_default: bool
    default: Any

    def __repr__(self):
        if self.has_default:
            default = "null" if self.default is None else str(self.default)
            return f"{self.name}={default}"
        return self.name


class Method(BaseModel):
    description: str
    name: str
    method: HttpMethod | Literal["*"]
    parameters: List[Parameter]
    requires_body: bool
    model_path_map: str | None


class Controller(BaseModel):
    name: str
    description: str
    methods: List[Method]
    model: str | None
    is_abstract: bool


def parse_php_controller(ctrl: PhpController) -> Controller:
    model = ctrl["model"]
    if model:
        vendor, _module, name = model.split("\\")
        model = get_openapi_schema_path(vendor, _module, name)

    methods = []
    php_methods = ctrl["methods"]
    for php_method in php_methods:
        doc = php_method.get("doc") or ""
        comment = DocComment.from_php(doc)
        param_descr = comment.param_descriptions

        params = []
        for php_param in php_method["parameters"]:
            description = param_descr.get(php_param["name"], "")
            param = Parameter(
                description=description,
                **php_param,
            )
            params.append(param)

        method = Method(
            description=comment.description,
            name=php_method["name"],
            method=php_method["method"],
            parameters=params,
            requires_body=php_method["requires_body"],
            model_path_map=php_method["model_path_map"],
        )
        methods.append(method)

    return Controller(
        name=ctrl["name"],
        description=ctrl["doc"] or "",  # TODO
        methods=methods,
        model=model,
        is_abstract=ctrl["is_abstract"],
    )
#endregion intermediate DTOs


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
    model: str | None
    requires_body: bool
    model_path_map: str | None

    @property
    def path(self) -> str:
        path = f"/{self.module}/{self.controller}/{self.name}".lower()
        params = [f"{{{p.name}}}" for p in self.parameters]
        return "/".join([path] + params)

    @property
    def operation_id(self) -> str:
        suffix = "_Post" if self.method == "POST" else ""
        name = self.name[0].capitalize() + self.name[1:]
        return f"{self.module}{self.controller}{name}{suffix}"

    def __repr__(self):
        return self.path


def get_controllers(source_folder: str) -> List[Controller]:
    """Call ParseControllers.php"""

    script_dir = os.path.dirname(__file__)
    php_script_path = f"{script_dir}/ParseControllers.php"

    php_result = subprocess.run(["php", php_script_path, "-s", source_folder], capture_output=True)
    if php_result.returncode:
        print(php_result.stdout.decode())
        raise subprocess.SubprocessError(php_result.stderr.decode())

    php_controllers = json.loads(php_result.stdout)
    controllers = []
    for ctrl in php_controllers:
        if not ctrl["is_abstract"]:
            controllers.append(parse_php_controller(ctrl))
    return controllers


def get_controller_url_segments(class_name: str):
    """Expects, e.g. OPNsense\\Proxy\\Api\\AclController"""
    segments = class_name.split("\\")
    return segments[-3], segments[-1].replace("Controller", "")


def parse_endpoints(controller: Controller) -> List[Endpoint]:
    module, controller_name = get_controller_url_segments(controller.name)

    endpoints = []
    for method in controller.methods:
        http_methods: List[HttpMethod] = ["GET", "POST"] if method.method == "*" else [method.method]
        for http_method in http_methods:
            endpoint = Endpoint(
                description=method.description,
                module=module,
                controller=controller_name,
                name=method.name,
                method=http_method,
                parameters=method.parameters,
                model=controller.model,
                requires_body=method.requires_body,
                model_path_map=method.model_path_map,
            )
            endpoints.append(endpoint)

    return endpoints


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
