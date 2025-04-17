#! /usr/bin/env python3
from openapi_schema_validator import validate
from jsonschema.exceptions import _Error, ValidationError, SchemaError
from pprint import *
from scratch import response, schema

try:
    validate(response, schema)
except Exception as ex:
    indent = 20

    # print(ex.__class__)
    # print(ex.args)
    # if isinstance(ex, (ValidationError, SchemaError)):
    if isinstance(ex, _Error):
        attrs = [
            "message",
            "instance",
            "schema",
            "path",
            "schema_path",
            "validator",
        ]
    else:
        attrs = [a for a in dir(ex) if not a.startswith("_")]

    print(f"type:                {ex.__class__.__name__}")
    for attr in attrs:
        value = getattr(ex, attr)
        if not isinstance(value, str):
            value = pformat(value, compact=True)

        value = value.replace("\n", "\n".ljust(indent))

        # if len(value) > 400:
        #     value = value[0:397].strip() + "..."

        a = f"{attr}:"
        print(f"{a.ljust(indent)} {value}")
