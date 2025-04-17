response = {
    "route": {
        "route": {
            "1c23606b-4647-4718-b180-35e6d7d4470b": {
                "network": "7.7.7.0/24",
                "gateway": {
                    "FakeGW": {"value": "FakeGW - 7.7.7.7", "selected": 1},
                    "Null4": {"value": "Null4 - 127.0.0.1", "selected": 0},
                    "Null6": {"value": "Null6 - ::1", "selected": 0},
                    "WAN_DHCP": {"value": "WAN_DHCP - 192.168.124.1", "selected": 0},
                    "WAN_DHCP6": {"value": "WAN_DHCP6 - inet6", "selected": 0},
                    "WAN_GW": {"value": "WAN_GW - 192.168.124.1", "selected": 0},
                },
                "descr": "FooRoute",
                "disabled": "0",
            }
        }
    }
}
schema = {
    "type": "object",
    "properties": {
        "route": {
            "oneOf": [
                {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {},
                    },
                },
                {
                    "type": "object",
                    "additionalProperties": {},
                }
            ],
            "x-config-xpath": ".//staticroutes",
        }
    },
}
