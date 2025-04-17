#! /usr/bin/env python3

# import libxml2
import xml.etree.cElementTree as ET

# file = "/home/freddie/gitroot/upstream/opnsense/core/src/opnsense/mvc/app/models/OPNsense/Auth/Group.xml"
# model = ET.parse(file)

# mount_path = None
# mount = model.find("mount")
# print(mount)
# if mount is not None:
#     mount_path = mount.text
#     if mount_path:
#         mount_path = f".{mount_path.replace("+", "")}"
# print(mount_path)

# file = "config-opnshut.xml"
# config = ET.parse(file)
# e = config.findall(mount_path)
# print(e)


file = "/home/freddie/gitroot/upstream/opnsense/core/src/opnsense/mvc/app/models/OPNsense/Auth/Group.xml"
with open(file) as _file:
    content = _file.read()

# print(content)
model = ET.fromstring(content)
print(model)

# mount_path = None
# mount = model.find("mount")



# paths = [
#     "./system/group",
#     "./system/user",
#     ".//OPNsense/captiveportal",
#     ".//system/firmware",
#     ".//hasync",
#     ".//sysctl",
#     ".//OPNsense/cron",
#     ".//OPNsense/DHCRelay",
#     ".//OPNsense/Firewall/Lvtemplate",
#     ".//OPNsense/Netflow",
#     "./dnsmasq",
#     ".//OPNsense/Firewall/Alias",
#     ".//OPNsense/Firewall/Category",
#     ".//OPNsense/Firewall/Filter",
#     "./ifgroups",
#     ".//OPNsense/IDS",
#     ".//OPNsense/IPsec",
#     ".//OPNsense/Swanctl",
#     "./gifs",
#     "./gres",
#     "./laggs",
#     ".//OPNsense/Interfaces/loopbacks",
#     ".//OPNsense/Interfaces/neighbors",
#     "./virtualip",
#     "./vlans",
#     ".//OPNsense/Interfaces/vxlans",
#     ".//OPNsense/Kea/ctrl_agent",
#     ".//OPNsense/Kea/dhcp4",
#     ".//OPNsense/monit",
#     ".//OPNsense/OpenVPNExport",
#     ".//OPNsense/OpenVPN",
#     ".//staticroutes",
#     ".//OPNsense/Gateways",
#     ".//OPNsense/Syslog",
#     ".//OPNsense/TrafficShaper",
#     "./ca",
#     "./cert",
#     ".//OPNsense/trust/general",
#     ".//OPNsense/unboundplus",
#     ".//OPNsense/wireguard/client",
#     ".//OPNsense/wireguard/general",
#     ".//OPNsense/wireguard/server"
# ]

# file = "config-opnshut.xml"
# config = ET.parse(file)

# for path in paths:
#     e = config.findall(path)
#     print(e)
