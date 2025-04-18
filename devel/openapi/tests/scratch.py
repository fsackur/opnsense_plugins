response = {
    "server": {
        "enabled": "1",
        "name": "",
        "instance": "0",
        "pubkey": "",
        "privkey": "",
        "port": "",
        "mtu": "",
        "dns": {"": {"value": "", "selected": 1}},
        "tunneladdress": {"": {"value": "", "selected": 1}},
        "disableroutes": "0",
        "gateway": "",
        "carp_depend_on": {"": {"value": "None", "selected": 1}},
        "peers": [],
        "endpoint": "",
        "peer_dns": "",
    }
}
schema = {
    "type": "object",
    "properties": {
        "server": {
            "type": "object",
            "properties": {
                "enabled": {"type": "string"},
                "name": {"type": "string"},
                "instance": {"type": "string"},
                "pubkey": {"type": "string"},
                "privkey": {"type": "string"},
                "port": {"type": "string"},
                "mtu": {"type": "string"},
                "dns": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string"},
                            "selected": {"type": "integer", "enum": [0, 1]},
                        },
                        "required": ["value", "selected"],
                    },
                },
                "tunneladdress": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string"},
                            "selected": {"type": "integer", "enum": [0, 1]},
                        },
                        "required": ["value", "selected"],
                    },
                },
                "disableroutes": {"type": "string"},
                "gateway": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string"},
                            "selected": {"type": "integer", "enum": [0, 1]},
                        },
                        "required": ["value", "selected"],
                    },
                },
                "carp_depend_on": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "key": {"type": "string"},
                    },
                    "additionalProperties": False,
                },
                "peers": {
                    "type": "object",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "value": {"type": "string"},
                            "selected": {"type": "integer"},
                        },
                        "additionalProperties": False,
                    },
                },
                "endpoint": {"type": "string"},
                "peer_dns": {"type": "string"},
            },
            "additionalProperties": False,
        }
    },
}
