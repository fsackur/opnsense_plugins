#! /usr/bin/env python3

"""
Find XML model files and parse into intermediate DTOs.
"""

import json
import os
import argparse
import pathlib
from typing import List, Dict
from xml.etree import ElementTree
from xml.etree.ElementTree import Element as XmlElement

from pydantic import BaseModel


_DEFAULT_SOURCE_FOLDER = "/usr/local/opnsense/mvc/app"
_DEFAULT_OUTPUT_FILE = "xml_models.json"

EXCLUDE_MODEL = "mvc/app/models/OPNsense/iperf/FakeInstance.xml"


def get_openapi_schema_path(vendor: str, module: str, name: str) -> str:
    """Component path in the OpenApi schema; API ops will $ref to it."""
    return f"{vendor}.{module}.{name}".lower()


#region Intermediate DTOs
# for validation and to smooth over XML child/attribute distinctions
class XmlNode(BaseModel):
    name: str
    type: str | None
    value: str | None
    children: List["XmlNode"]

    def __repr__(self):
        return f"XmlNode({self.name})"

# To save passing path recursively, only the root node gets it
class XmlModel(XmlNode):
    schema_path: str
    mount: str | None

    def __repr__(self):
        return f"XmlModel({self.schema_path})"
#endregion Intermediate DTOs


def _walk_xml(element: XmlElement) -> XmlNode:
    attrib = element.attrib.copy()
    field_type = attrib.pop("type", None)
    if field_type and field_type.startswith(".\\"):
        field_type = field_type[2:]

    name = attrib.pop("value", element.tag)

    # _ = attrib.pop("volatile", None)
    # if attrib:
    #     raise ValueError(f"Unexpected attribute {attrib} in {element}")

    value = element.text
    value = value.strip() if value else value

    children = []
    for child_element in element:
        child = _walk_xml(child_element)
        children.append(child)

    return XmlNode(
        type=field_type,
        name=name,
        value=value,
        children=children
    )


def parse_xml_file(xml_file: str) -> XmlModel:
    path_without_ext = xml_file[0:-4]
    vendor, module, name = path_without_ext.split("/")[-3:]
    schema_path = get_openapi_schema_path(vendor, module, name)

    tree = ElementTree.parse(xml_file)
    items = tree.find("items")
    if items is None:
        raise ValueError("items tag not found")  # never happens; just appeases the linter

    mount = tree.find("mount")
    mount_path = ""
    if mount is not None:
        mount_path = mount.text or ""
        if mount_path and mount_path != ":memory:":
            mount_path = f".{mount_path.replace("+", "")}"

    xml_model = _walk_xml(items, xml_path=".")
    return XmlModel(**xml_model.dict(), schema_path=schema_path)


def get_model_xml_files(source_folder: str) -> List[str]:
    """Finds paths of model XML files within mvc/app/models"""
    source_folder = os.path.normpath(source_folder)
    found = []
    if os.path.isdir(source_folder):
        for root, _, files in os.walk(source_folder, topdown=True, followlinks=True):
            path_segments = root.split("/")
            if path_segments[-3] != "models":  # seems consistent as of v25.1
                continue
            xml_files = [os.path.join(root, f) for f in files if f.endswith(".xml")]
            found.extend(xml_files)
    elif os.path.isfile(source_folder) and source_folder.endswith(".xml"):
        found.append(source_folder)
    else:
        raise ValueError(f"{source_folder} is not a directory or XML file. Specify a source folder containing XML model files.")
    return found


def get_models(
    source_folder: str = _DEFAULT_SOURCE_FOLDER,
    json_path: str | None = None,
) -> List[XmlModel]:
    if json_path and os.path.isfile(json_path):
        with open(json_path) as file:
            model_json = file.read()
        _models = json.loads(model_json)
        models = [XmlModel(**m) for m in _models]
        return models

    xml_files = get_model_xml_files(source_folder)

    models = []
    for xml_file in xml_files:
        model = parse_xml_file(xml_file)
        models.append(model)

    if json_path:
        model_json = json.dumps([m.dict() for m in models])
        pathlib.Path(json_path).parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, mode="w") as file:
            file.write(model_json)

    return models


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="parse XML models")
    parser.add_argument("-s", "--source-folder", default=_DEFAULT_SOURCE_FOLDER)
    parser.add_argument("-o", "--output-file", default=None)
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args()

    source_folder = args.source_folder
    output_file = os.path.realpath(args.output_file) if args.output_file else None
    quiet = args.quiet

    models = get_models(source_folder, json_path=output_file)

    if not quiet:
        from pprint import pprint
        pprint(models)
