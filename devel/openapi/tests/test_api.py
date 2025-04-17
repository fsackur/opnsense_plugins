#! /usr/bin/env python3

import sys
import os
from typing import Dict, Any, Literal, Hashable, Mapping, Tuple
import pytest
from pytest import mark, param
from unittest.mock import ANY
# import openapi_schema_validator
from openapi_schema_validator import validate
from referencing import Registry, Resource

from fixtures import *
from urls import urls

StrDict = Dict[str, Any]



# if "--yaml" in sys.argv:
#     _spec = load_spec_from_file.__wrapped__()
# else:
#     _config: Config = config.__wrapped__()
#     _spec = generate_spec.__wrapped__(_config["source_folder"])
# urls = list(_spec._paths.keys())
# urls = [u for u in urls if not "firmware" in u]

if "--url" in sys.argv:
    index = sys.argv.index("--url")
    url_arg = sys.argv[index + 1]
    filters = re.split(r",\s*|\s+", url_arg)
    _urls = []
    for f in filters:
        _urls.extend(u for u in urls if f in u)
    urls = sorted(set(_urls))

if "--slice" in sys.argv:
    index = sys.argv.index("--slice")
    _slice = sys.argv[index + 1]
    urls = eval(f"urls{_slice}")

# url_filters = [
#     "/auth/priv/getitem/",
#     "/auth/user/del/",
#     "/auth/group/del/",
#     "/captiveportal/settings/delzone/",
#     "/core/tunables/delitem/c5a7acc3-aef1-47d8-93f6-ebda09380936",
#     "/cron/settings/deljob/",
#     "/dhcrelay/settings/delrelay/",
#     "/dhcrelay/settings/deldest/",
#     "/diagnostics/lvtemplate/delitem/",
#     "/dnsmasq/settings/delhost/",
#     "/dnsmasq/settings/deldomain/",
#     "/dnsmasq/settings/deltag/",
#     "/dnsmasq/settings/delrange/",
#     "/dnsmasq/settings/deloption/",
#     "/dnsmasq/settings/delmatch/",
#     "/dnsmasq/settings/delboot/",
#     "/firewall/category/delitem/",
#     "/firewall/filter/delrule/",
#     "/firewall/group/delitem/",
#     "/firewall/npt/delrule/",
#     "/firewall/onetoone/delrule/",
#     "/firewall/sourcenat/delrule/",
#     "/firewall/alias/delitem/",
#     "/firewall/alias/getgeoip",
#     "/ids/settings/get",
#     "/ids/settings/deluserrule/",
#     "/ids/settings/delpolicy/",
#     "/ids/settings/delpolicyrule/",
#     "/ipsec/connections/getconnection/aa844964-35bd-4e6c-8bad-57df7aa5be8e",
#     "/ipsec/connections/delconnection/aa844964-35bd-4e6c-8bad-57df7aa5be8e",
#     "/ipsec/connections/dellocal/",
#     "/ipsec/connections/delremote/",
#     "/ipsec/connections/delchild/",
#     "/ipsec/keypairs/delitem/",
#     "/ipsec/manualspd/del/",
#     "/ipsec/pools/del/",
#     "/ipsec/presharedkeys/delitem/",
#     "/ipsec/vti/del/",
#     "/interfaces/gifsettings/delitem/",
#     "/interfaces/gresettings/delitem/",
#     "/interfaces/laggsettings/delitem/",
#     "/interfaces/loopbacksettings/delitem/",
#     "/interfaces/neighborsettings/delitem/",
#     "/interfaces/vipsettings/delitem/",
#     "/interfaces/vlansettings/delitem/",
#     "/interfaces/vxlansettings/delitem/",
#     "/kea/dhcpv4/get",
#     "/kea/dhcpv4/delsubnet/",
#     "/kea/dhcpv4/delreservation/",
#     "/kea/dhcpv4/delpeer/",
#     "/monit/settings/get",
#     "/monit/settings/dirty",
#     "/monit/settings/delalert/",
#     "/monit/settings/getservice/edd58d19-13a8-494e-8856-120ee7bb7536",
#     "/monit/settings/delservice/edd58d19-13a8-494e-8856-120ee7bb7536",
#     "/monit/settings/deltest/0387014d-5608-4ca7-a97a-f248a02736d4",
#     "/monit/settings/getgeneral",
#     "/openvpn/clientoverwrites/del/",
#     "/openvpn/instances/del/",
#     "/openvpn/instances/delstatickey/",
#     "/routes/routes/delroute/",
#     "/routing/settings/delgateway/43f2b5c4-171c-4b1f-a7f1-5779bce2220d",
#     "/syslog/settings/deldestination/",
#     "/trafficshaper/settings/getpipe/7b5dc65b-fe98-4ae7-b51d-f91a25e21ee1",
#     "/trafficshaper/settings/delpipe/7b5dc65b-fe98-4ae7-b51d-f91a25e21ee1",
#     "/trafficshaper/settings/delqueue/b8f3c20d-2ae5-4187-89c2-02f54b9cc502",
#     "/trafficshaper/settings/delrule/",
#     "/trust/ca/del/",
#     "/trust/cert/del/",
#     "/unbound/settings/delforward/",
#     "/unbound/settings/delhostoverride/",
#     "/unbound/settings/delhostalias/",
#     "/unbound/settings/delacl/",
#     "/wireguard/client/delclient/",
#     "/wireguard/server/delserver/"
# ]
# _urls = []
# for uf in url_filters:
#     _urls.extend(u for u in urls if uf in u)
# urls = _urls

log_path = f"{os.path.dirname(__file__)}/pytest.log"
try:
    os.remove(log_path)
except FileNotFoundError:
    pass
import logging
logger = logging.getLogger("api_tests")
handler = logging.FileHandler(log_path)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


@fixture
def registry(spec: APISpec) -> Registry:
    components = spec.components.schemas

    # priv = components["opnsense.auth.priv"]
    # print(priv)
    # reg = Registry().with_resource(f"opnsense.auth.priv", Resource.from_contents(priv, default_specification=DRAFT202012))

    # parent_schema = {"components": spec.components}
    parent_schema = {"components": {"schemas": spec.components.schemas}}
    # parent_schema = {"schemas": spec.components.schemas}

    schema = Resource(contents=parent_schema, specification=DRAFT202012)
    reg = Registry().with_resource(uri="/components", resource=schema)
    return reg


from pprint import pprint, pformat

@mark.parametrize("url", urls)
def test_endpoint(url, spec, api, get_node: ElementFetcher):
    method_op = spec._paths[url]
    for method, op in [(k, v) for k, v in method_op.items() if k in ("get", "post")]:
        schema = op["responses"]["200"]["content"]["application/json"]["schema"]
        # print(schema)
        # schema = {"$ref": '#/components/schemas/opnsense.auth.priv'}
        schema, model_name, model_path = resolve_schema(schema, spec.components.schemas)
        # print(model_name, model_path)

        params = op.get("parameters", [])
        nodes = []
        url_with_params = url
        if params:
            model = spec.components.schemas.get(model_name, {})
            xpath = model.get("x-config-xpath", None)
            if xpath:
                # print(xpath)
                if model_path:
                    x_model_path = model_path.replace("properties/", "").replace("items/", "")
                    xpath = f"{xpath}/{x_model_path}"
                nodes = get_node(xpath)
            attrib = nodes[0].attrib if nodes else {}
            for param in params:
                value = attrib.get(param["name"]) or param["schema"].get("default")
                if value:
                    # print(f"replaced {param["name"]} with {value} in {url} from {param}")
                    url_with_params = url_with_params.replace(f"{{{param["name"]}}}", str(value))

        response = api.call(method, url_with_params)
        response_body = response.json()

        # if "errorMessage" in response_body:
        #     return


        print(f"response = {response_body}")
        print(f"schema = {schema}")
        try:
            validate(response_body, schema)
            logger.info(f"{url}: pass")
        except Exception as ex:
            logger.error(f"{url}: {ex.__class__.__name__}: {ex.args[0]}")
            raise


def resolve_schema(schema: StrDict, components: StrDict): #-> Tuple[StrDict, str | None]:
    model_name = None
    model_path = None

    _schema = schema.copy()

    ref: str | None = _schema.pop("$ref", None)
    if ref is not None:
        model_parts = ref.replace("#/components/schemas/", "")
        if "/" in model_parts:
            model_name, model_path = model_parts.split("/", maxsplit=1)
        else:
            model_name, model_path = model_parts, None

        _schema = components[model_name]
        if model_path:
            breadcrumbs = model_path.split("/")
            for breadcrumb in breadcrumbs:
                try:
                    breadcrumb = int(breadcrumb)
                except: pass
                _schema = _schema[breadcrumb]

    for k, v in _schema.items():
        if isinstance(v, Mapping):
            v, _model_name, _model_path = resolve_schema(v, components)
            model_name = model_name or _model_name
            model_path = model_path or _model_path
        _schema[k] = v
    return _schema, model_name, model_path



# def get_expected_response(schema: StrDict, components: StrDict) -> StrDict:
#     schema = deepcopy(schema)
#     # while "$ref" not in expected:
#     ref: str = schema["$ref"].replace("#/components/schemas/", "")
#     print(ref)
#     if "/" in ref:
#         name, path = ref.split("/", maxsplit=1)
#     else:
#         name = ref
#         path = None

#     component = components[name]
#     if path:
#         breadcrumbs = path.split("/")
#         for breadcrumb in breadcrumbs:
#             component = component[breadcrumb]
#         # while breadcrumbs:
#         #     prop = breadcrumbs[0]
#         #     if "properties" in component:
#         #         component = component["properties"][prop]
#         #         breadcrumbs = breadcrumbs[1:]
#         #     elif "items" in component:
#         #         component = component["items"]
#         #         # still on the same breadcrumb; go round again
#         #     else:
#         #         raise KeyError(f"could not find {prop} in {component}")

#     return component["properties"]


# if __name__ == "__main__":
#     pytest.
