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
            print("found memo")
        except KeyError:
            print("no memo found")
            spec = func(*args, **kwargs)
            memo[hashable_args] = spec
        return spec
    return wrapper


generate_openapi_spec = memoise(_generate_openapi_spec)


@fixture(autouse=True)
def no_cert_warnings():
    urllib3.disable_warnings()


class Config(TypedDict):
    source_folder: str
    base_url: str
    api_key: str
    api_secret: str


@fixture(scope="session")
def config() -> Config:
    path = f"{os.path.dirname(__file__)}/config.json"
    try:
        with open(path) as file:
            config_json = file.read()

    except FileNotFoundError as ex:
        default_config = {a: "" for a in Config.__annotations__.keys()}
        config_json = json.dumps(default_config, indent=4)

        with open(path, "w") as file:
            file.write(config_json)

        msg = f"A default config has been created at {path}. Populate the values in the file."
        raise FileNotFoundError(msg) from None

    return {k: v for k, v in json.loads(config_json).items() if v}  # type: ignore


@fixture(scope="session")
def source_folder(config: Config):
    return config["source_folder"]


@fixture(scope="session")
def generate_spec(source_folder) -> APISpec:
    return generate_openapi_spec(source_folder)


@fixture(scope="session")
def load_spec_from_file() -> APISpec:
    return load_openapi_spec("openapi.yml")


spec = load_spec_from_file if "--yaml" in sys.argv else generate_spec


@fixture
def spec_validator():
    def validate(spec: APISpec) -> None:
        openapi_spec_validator.validate(spec.to_dict())  # type: ignore
    return validate


class Api:
    def __init__(self, base_url, api_key, api_secret, **_):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(api_key, api_secret)

    def _request_kwargs(self, url, data: Dict | None = None):
        kwargs: Dict[str, Any] = {
            "url": f"{self.base_url}{url}" if url.startswith("/") else f"{self.base_url}/{url}",
            "auth": self.auth,
            "verify": False,
        }
        if data:
            kwargs["data"] = data
        return kwargs

    def get(self, url):
        kwargs = self._request_kwargs(url)
        return requests.get(**kwargs)

    def post(self, url, data: Dict | None = None):
        kwargs = self._request_kwargs(url, data)
        return requests.post(**kwargs)

    def call(self, method: HttpMethod, *args, **kwargs):
        if method == "get":
            return self.get(*args, **kwargs)
        return self.post(*args, **kwargs)


@fixture(scope="session")
def api(config: Config):
    return Api(**config)
