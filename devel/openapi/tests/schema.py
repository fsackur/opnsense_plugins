#! /usr/bin/env python3

from typing import *
import json
import yaml
from apispec import APISpec
from jsf import JSF


def load_openapi_spec(path: str) -> APISpec:
    with open(path) as file:
        content = file.read()
    _spec = yaml.load(content, Loader=yaml.CLoader)

    info = _spec.pop("info")
    version = _spec.pop("openapi")
    paths = _spec.pop("paths")
    components = _spec.pop("components")["schemas"]

    spec = APISpec(openapi_version=version, **info)

    for path, op in paths.items():
        description = op.pop("description")
        spec.path(path=path, description=description, operations=op)

    for ref, c in components.items():
        spec.components.schema(ref, c)

    return spec


def generate(spec: APISpec, models: str | Container[str] | None = None) -> Dict[str, Any]:
    faker_kwargs = {
        "allow_none_optionals": 0.0,
        "max_recursive_depth": 20,
    }

    schemas = spec.components.schemas

    if isinstance(models, str):
        schemas = {models: schemas[models]}
    elif models is not None:
        schemas = {m: s for m, s in schemas.items() if m in models}

    output = {}
    for model_name, schema in schemas.items():
        faker = JSF(schema, **faker_kwargs)
        data = faker.generate()
        output[model_name] = data

    return output


def export(path: str, data: Dict[str, Any]):
    json_data = json.dumps(data)
    with open(path, "w") as file:
        file.write(json_data)


if __name__ == "__main__":
    path = "/gitroot/upstream/opnsense/plugins/devel/openapi/src/opnsense/scripts/OPNsense/OpenApi/openapi.yml"
    spec = load_openapi_spec(path)

    model_name = "opnsense.firewall.alias"
    mock_models = generate(spec, model_name)

    output_file = "mock_models.json"
    export(output_file, mock_models)
