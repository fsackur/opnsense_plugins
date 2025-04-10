#! /usr/bin/env python3

import os
import json
from typing import TypedDict
from pytest import fixture
import openapi_spec_validator
from apispec import APISpec

from loader import generate_openapi_spec


class Config(TypedDict):
    source_folder: str


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
def spec(source_folder) -> APISpec:
    spec = generate_openapi_spec(source_folder)
    return spec


@fixture
def spec_validator():
    def validate(spec: APISpec) -> None:
        openapi_spec_validator.validate(spec.to_dict())  # type: ignore
    return validate
