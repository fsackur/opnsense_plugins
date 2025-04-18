#! /usr/bin/env python3

import os
import sys
import json
import functools
import inspect
from typing import TypedDict, Dict, Any, Literal
from pytest import fixture
import openapi_spec_validator
from apispec import APISpec
import requests
import urllib3
from requests.auth import HTTPBasicAuth
from openapi_schema_validator import validate
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
# import xml.etree.cElementTree as ElementTree
from xml.etree.ElementTree import Element as XmlElement
from xml.etree.ElementTree import ElementTree, XML

from loader import generate_openapi_spec as _generate_openapi_spec
from loader import load_openapi_spec

HttpMethod = Literal["get"] | Literal["post"]


def memoise(func):
    memo = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        spec = inspect.getfullargspec(func)

        arg_list = list(args)
        remaining_args = spec.args[len(args):]
        for arg in remaining_args:
            value = kwargs.get(arg, None)
            arg_list.append(value)
        hashable_args = tuple(arg_list)

        try:
            spec = memo[hashable_args]
        except KeyError:
            spec = func(*args, **kwargs)
            memo[hashable_args] = spec
        return spec
    return wrapper


generate_openapi_spec = memoise(_generate_openapi_spec)


@fixture(scope="session", autouse=True)
def no_cert_warnings():
    urllib3.disable_warnings()


class ClientConfig(TypedDict):
    source_folder: str
    base_url: str
    api_key: str
    api_secret: str


@fixture(scope="session")
def client_config() -> ClientConfig:
    path = f"{os.path.dirname(__file__)}/config.json"
    try:
        with open(path) as file:
            config_json = file.read()

    except FileNotFoundError as ex:
        default_config = {a: "" for a in ClientConfig.__annotations__.keys()}
        config_json = json.dumps(default_config, indent=4)

        with open(path, "w") as file:
            file.write(config_json)

        msg = f"A default config has been created at {path}. Populate the values in the file."
        raise FileNotFoundError(msg) from None

    return {k: v for k, v in json.loads(config_json).items() if v}  # type: ignore


@fixture(scope="session")
def source_folder(client_config: ClientConfig):
    return client_config["source_folder"]


@fixture(scope="session")
def generate_spec(source_folder) -> APISpec:
    return generate_openapi_spec(source_folder) #, module="auth", controller="priv")


@fixture(scope="session")
def load_spec_from_file() -> APISpec:
    return load_openapi_spec("openapi.yml")


spec = load_spec_from_file if "--yaml" in sys.argv else generate_spec
# spec = generate_spec


@fixture
def spec_validator():
    def validate(spec: APISpec) -> None:
        openapi_spec_validator.validate(spec.to_dict())  # type: ignore
    return validate


class Api:
    def __init__(self, base_url, api_key, api_secret, **_):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(api_key, api_secret)

    def _request_kwargs(self, url, path_params: Dict = {}, data: Dict | None = None):
        for k, v in path_params.items():
            url = url.replace(f"{{{k}}}", str(v))
        if "{" in url:
            raise ValueError(f"Unreplaced param in {url}")

        url = re.sub(r"//|/$", "", url)

        kwargs: Dict[str, Any] = {
            "url": f"{self.base_url}{url}" if url.startswith("/") else f"{self.base_url}/{url}",
            "auth": self.auth,
            "verify": False,
        }
        if data:
            kwargs["data"] = data
        return kwargs

    def get(self, url, path_params: Dict = {}):
        kwargs = self._request_kwargs(url, path_params)
        return requests.get(**kwargs)

    def post(self, url, path_params: Dict = {}, data: Dict | None = None):
        kwargs = self._request_kwargs(url, path_params, data)
        return requests.post(**kwargs)

    def call(self, method: HttpMethod, *args, **kwargs):
        if method == "get":
            return self.get(*args, **kwargs)
        return self.post(*args, **kwargs)


@fixture(scope="session")
def api(client_config: ClientConfig, no_cert_warnings):
    return Api(**client_config)


from typing import *
import re
def gm(_obj, props: Optional[List[str]]=None, show_dunder=False):
    obj: Sequence = _obj if isinstance(_obj, Sequence) else [_obj]
    if len(obj) == 0:
        return

    attrs = dir(obj[0])
    if not show_dunder:
        attrs = [a for a in attrs if not a.startswith("_")]

    if props is not None:
        attrs = [a for a in attrs if any(
            p for p in props if re.match(p, a, re.IGNORECASE)
        )]

    length = len(sorted(attrs, key=len)[-1])
    pad_length = length + 2

    for obj in obj:
        for attr in attrs:
            msg = f"{attr}:".ljust(pad_length, " ")
            try:
                value = getattr(obj, attr)
            except Exception as ex:
                value = ex
            value_msg = repr(value)
            print(f"{msg}{value_msg}")
        print("")


@fixture(scope="session")
def opnsense_config(api: Api) -> XmlElement:
    path = f"{os.path.dirname(__file__)}/config.xml"
    if os.path.exists(path):
        with open(path) as file:
            conf = file.read()
    else:
        conf = api.get("/core/backup/download/this").text
        with open(path, "w") as file:
            file.write(conf)
    root = XML(conf)
    return root

ElementFetcher = Callable[[str], XmlElement]
ElementsFetcher = Callable[[str], List[XmlElement]]

@fixture(scope="session")
def get_node(opnsense_config) -> ElementsFetcher:
    return opnsense_config.findall
    # def get_node(xpath: str) -> XmlElement:
    #     return opnsense_config.findall(xpath)
    # return get_node

@fixture(scope="session")
def model_xml_registry(source_folder) -> ElementFetcher:
    registry = {}
    model_source_folder = None
    for root, _, files in os.walk(source_folder, topdown=True, followlinks=True):
        path_segments = root.split("/")
        if path_segments[-1] != "models" or path_segments[-3] == "tests": continue
        model_source_folder = root

    if not model_source_folder:
        raise FileNotFoundError(f"models not found in {source_folder}")

    def get_xml(rel_path: str) -> XmlElement:
        if rel_path[0] == "/":
            rel_path = rel_path[1:]

        parts = rel_path.split(",", maxsplit=1)
        if len(parts) == 1:
            rel_path, xpath = parts[0], None
        else:
            rel_path, xpath = parts

        if rel_path in registry:
            root = registry[rel_path]
        else:
            xml_file = os.path.join(model_source_folder, rel_path)
            with open(xml_file) as file:
                conf = file.read()
            root = XML(conf)
            registry[rel_path] = root

        if not xpath:
            return root

        node = root.find(xpath)
        if node is None:
            raise AttributeError(f"could not find '{xpath} in {root}")
        return node

    return get_xml
