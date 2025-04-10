#! /usr/bin/env python3

import sys
import importlib.util
from pathlib import Path


plugin_base = Path(__file__).parents[1]
script_base = plugin_base.joinpath("src/opnsense/scripts/OPNsense/OpenApi")
scripts = [
    "parse_xml_models.py",
    "parse_endpoints.py",
    "generate_openapi_spec.py",
]

for script in scripts:
    script_file = script_base.joinpath(script)

    name = script_file.stem
    spec = importlib.util.spec_from_file_location(name, script_file)

    if not spec or not spec.loader:
        raise ValueError(f"Script not found at {script_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

generate_openapi_spec = sys.modules["generate_openapi_spec"].generate_openapi_spec
