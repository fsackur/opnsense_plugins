# Sequence diagram

```mermaid
sequenceDiagram
    participant g as generate_openapi_spec.py
    participant x as parse_xml_models.py
    g->>x: get_models
    note right of x: not really parsing, approximately raw XML
    destroy x
    x->>g: models.json

    create participant e as parse_endpoints.py
    g->>e: get_endpoints
    create participant php as ParseControllers.php
    e->>php: ParseControllers
    destroy php
    php->>e: controllers.json
    destroy e
    e->>g: endpoints.json

    create participant get_component_spec
    g->>get_component_spec: models.json
    note right of get_component_spec: real parsing of XML
    destroy get_component_spec
    get_component_spec->>g: OpenApi components

    create participant get_operation_spec
    g->>get_operation_spec: endpoints.json
    destroy get_operation_spec
    get_operation_spec->>g: OpenApi operations
```

I stress that, to put together PRs, I've ripped apart my PoC and I am currently non-functional. This json is massaged to demonstrate intent.

controllers.json (output from PHP reflection):

```json
{
    "OPNsense\\Auth\\Api\\GroupController": {
        "name": "OPNsense\\Auth\\Api\\GroupController",
        "parent": "OPNsense\\Base\\ApiMutableModelControllerBase",
        "methods": [
            {
                "name": "get",
                "method": "GET",
                "parameters": [
                    {
                        "name": "uuid",
                        "has_default": true,
                        "default": null
                    }
                ],
                "doc": "Retrieve model settings"
            }
        ],
        "model": "OPNsense\\Auth\\Group",
        "is_abstract": false,
        "doc": "Class GroupController"
    },
```

endpoints.json:

```json
[
    {
        "description": "Retrieve model settings",
        "path": "/auth/group/get",
        "method": "GET",
        "parameters": [
            {
                "name": "uuid",
                "has_default": true,
                "default": null
            }
        ],
        "model": "opnsense.auth.group"
    },
```

OpenApi spec:

```json

```
