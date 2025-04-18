#! /usr/bin/env python3

import os
from io import StringIO, BufferedIOBase, BytesIO
from xml.etree.ElementTree import ElementTree, XML
# import xml.etree.cElementTree as ElementTree

# file = "/home/freddie/gitroot/upstream/opnsense/core/src/opnsense/mvc/app/models/OPNsense/Auth/Group.xml"
# model = ElementTree.parse(file)

# mount_path = None
# mount = model.find("mount")
# print(mount)
# if mount is not None:
#     mount_path = mount.text
#     if mount_path:
#         mount_path = f".{mount_path.replace("+", "")}"
# print(mount_path)

# file = "config-opnshut.xml"
# config = ElementTree.parse(file)
# e = config.findall(mount_path)
# print(e)


file = "/home/freddie/gitroot/upstream/opnsense/core/src/opnsense/mvc/app/models/OPNsense/Auth/Group.xml"
with open(file) as _file:
    content = _file.read()
# root = ElementTree.fromstring(content)
root = XML(content)
print(root)

for xpath in [
    ".//items/group/name/Mask",
    # ".//items/servers/server/gateway",
    # ".//items/servers/server/carp_depend_on",
    # ".//items/servers/server/peers/Model",
]:
    node = ElementTree(root.find(xpath))
    # stream = StringIO()
    stream = BytesIO()
    # print(stream.write("foo"))
    node.write(stream)
    stream.seek(0)
    print(stream.read().decode())

# source_folder = "/gitroot/upstream/opnsense/core/src/opnsense/"
# model_source_folder = None
# for root, _, files in os.walk(source_folder, topdown=True, followlinks=True):
#     path_segments = root.split("/")
#     if path_segments[-1] != "models" or path_segments[-3] == "tests": continue
#     model_source_folder = root

# if not model_source_folder:
#     raise FileNotFoundError(f"models not found in {source_folder}")


# for root, _, files in os.walk(source_folder, topdown=True, followlinks=True):
    # file = "/home/freddie/gitroot/upstream/opnsense/core/src/opnsense/mvc/app/models/OPNsense/Auth/Group.xml"
    # with open(file) as _file:
    #     content = _file.read()
    # root = ElementTree.fromstring(content)
    # print(root)
