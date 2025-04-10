#! /usr/bin/env python3

from pytest import fixture
import openapi_spec_validator
from apispec import APISpec

from loader import generate_openapi_spec


@fixture(scope="session")
def source_folder():
    return "/gitroot/upstream/opnsense/core/src/opnsense/"


@fixture(scope="session")
def spec(source_folder) -> APISpec:
    spec = generate_openapi_spec(source_folder)
    return spec


@fixture
def spec_validator():
    def validate(spec: APISpec) -> None:
        openapi_spec_validator.validate(spec.to_dict())  # type: ignore
    return validate
