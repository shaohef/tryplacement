#!/usr/bin/python

import kstoken

import requests
import json
import os
import random
import uuid as uuidlib
import sys

resource = sys.argv[1] if len(sys.argv) > 1 else "resource_classes"

INVENTORIES_DATA = {
    "inventories": {
        "DISK_GB": {
            "allocation_ratio": 1.0,
            "max_unit": 38,
            "min_unit": 1,
            "reserved": 0,
            "step_size": 1,
            "total": 38
        },
        "MEMORY_MB": {
            "allocation_ratio": 1.5,
            "max_unit": 16046,
            "min_unit": 1,
            "reserved": 512,
            "step_size": 1,
            "total": 16046
        },
        "VCPU": {
            "allocation_ratio": 16.0,
            "max_unit": 8,
            "min_unit": 1,
            "reserved": 0,
            "step_size": 1,
            "total": 8
        }
    }
}

INVENTORIES_RESOURCE = {
    "allocation_ratio": 1,
    "max_unit": 32,
    "min_unit": 1,
    "reserved": 0,
    "step_size": 1,
    "total": 20000
}

AGGREGATES_SET = ["42896e0d-205d-4fe3-bd1e-100924931787"]

TRAITS_DATA = {
    "traits": [
        "CUSTOM_TEST"
    ]
}

ALLOCATIONS_DATA = {
    "allocations": [
        {
            "resource_provider": {
                "uuid": "6e3b2ce9-9175-4830-a862-b9de690bdceb"
            },
            "resources": {
                "CUSTOM_FPGA": 2,
            }
        },
    ],
    # "project_id": "07e4536ce6234eaa9f6ae23698ddb941",
    # "user_id": "81c516e3-5e0e-4dcb-9a38-4473d229a950"
}

USAGES_DATA = {"project_id", kstoken.project_id, "user_id", kstoken.user_id}


HOST = "127.0.0.1"
HOSTURL = "http://%s" % HOST
BASEURL = "http://%s/placement/" % HOST
VER = 'OpenStack-API-Version:"placement 1.2"'

HEADERS = {"Content-Type": "application/json",
           "OpenStack-API-Version": "placement latest",
           "X-Auth-Token": kstoken.token}
resources = ["resource_providers", "resource_classes", "inventories"]

def get_uuid():
    return str(uuidlib.uuid4())

def ramdom_shuffle(l):
    i = random.randint(1, len(l)-1)
    return l[i].values()[0]

# for r in resources:
#    print "*" * 10 + "Get Resource: " + r + "*" * 10
def check_error(r):
    if not r.ok:
        print r.content
        print "Error, exit"
        sys.exit(1)

def pretty_print(r):
    if not r.ok:
        print r.content
        return
    data = r.json()
    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def sanity_pretty(rp):
    if rp.get("generation"):
        print "Generation: " + str(rp["generation"])
    name = ""
    if rp.get("name"):
        name = "Name: " + rp["name"]
    if rp.get("uuid"):
        uuid = "UUID: " + rp["uuid"]
        name = name + "\t" + uuid if name else uuid
    if name:
        print name

def get_sub_resources(res_type):
    """res_type can be resource_providers or resource_classes"""
    print "*" * 10 + res_type.capitalize()  + "*" * 10
    url = BASEURL +  res_type
    r = requests.get(url, headers=HEADERS)
    check_error(r)
    pretty_print(r)

    for rp in r.json()[res_type]:
        sanity_pretty(rp)
        for sub in rp["links"]:
            if sub["rel"] == "self":
               continue
            print "*" * 10 + " Get Resource: " + sub["rel"] + "*" * 10
            url = HOSTURL + sub["href"]
            r = requests.get(url, headers=HEADERS)
            check_error(r)
            pretty_print(r)

def _create_resource(res_type, name):
    url = BASEURL + res_type
    data = {"name": name}
    r = requests.post(url, data=json.dumps(data), headers=HEADERS)
    print "Create a " + res_type + ", and return: " + str(r.status_code)

def _update_resource(url, data):
    r = requests.put(url, data=json.dumps(data), headers=HEADERS)
    print "Update a resource:" + url + ", and return: " + str(r.status_code)
    if not r.ok:
        print r.content

# OP for version
def get_versions():
    url = BASEURL
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

# OP for resources providers
def _print_sub_resources_of_providers(rp):
        sanity_pretty(rp)
        for sub in rp["links"]:
            if sub["rel"] == "self":
               continue
            print "*" * 10 + " Get Resource: " + sub["rel"] + "*" * 10
            url = HOSTURL + sub["href"]
            r = requests.get(url, headers=HEADERS)
            check_error(r)
            pretty_print(r)

def create_resource_providers(name):
    _create_resource("resource_providers", name)

def get_resource_provider_uuid(name):
    res_type = "resource_providers"
    url = BASEURL +  res_type
    r = requests.get(url, headers=HEADERS)
    check_error(r)
    for rp in r.json()[res_type]:
        if rp.get("name") == name:
            return rp.get("uuid")

def get_resource_provider_uuids():
    res_type = "resource_providers"
    url = BASEURL +  res_type
    r = requests.get(url, headers=HEADERS)
    check_error(r)
    l = []
    for rp in r.json()[res_type]:
        d = {}
        d[rp["name"]] = rp["uuid"]
        l.append(d)
    return l

def get_resource_provider(uuid):
    url = BASEURL + "resource_providers/" + uuid
    r = requests.get(url, headers=HEADERS)
    _print_sub_resources_of_providers(r.json())

def delete_resource_provider(uuid):
    url = BASEURL + "resource_providers/" + uuid
    r = requests.delete(url, headers=HEADERS)

# OP for resource_providers inventories
def get_resource_provider_inventories(uuid):
    url = BASEURL + "resource_providers/" + uuid + "/inventories"
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

def delete_resource_provider_inventories(uuid):
    url = BASEURL + "resource_providers/" + uuid +"/inventories"
    r = requests.delete(url, headers=HEADERS)
    print "Delete all inventorie resource classes, and return: " + str(r.status_code)

def update_resource_provider_inventories(uuid, payload=None):
    url = BASEURL + "resource_providers/" + uuid +"/inventories"
    r = requests.get(url, headers=HEADERS)
    generation = r.json()["resource_provider_generation"]
    data = payload if payload is not None else {
        "inventories": {
            "CUSTOM_FPGA": {
                "max_unit": 16,
                "step_size": 1,
                "total": 6
            },
        },
        "resource_provider_generation": generation
    }
    if "resource_provider_generation" not in data:
        data["resource_provider_generation"] = generation
    _update_resource(url, data)

# OP for resource_providers inventories resource_classes
def get_resource_provider_inventories_resource_class(uuid, name):
    url = BASEURL + "resource_providers/" + uuid + "/inventories/" + name
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

def delete_resource_provider_inventories_resource_class(uuid, name):
    url = BASEURL + "resource_providers/" + uuid +"/inventories/" + name
    r = requests.delete(url, headers=HEADERS)
    print "Delete a inventorie resource class: " + name + ", and return: " + str(r.status_code)

def update_resource_provider_inventories_resource_class(uuid, name, payload=None):
    url = BASEURL + "resource_providers/" + uuid + "/inventories/" + name
    r = requests.get(url, headers=HEADERS)

    generation = r.json()["resource_provider_generation"] if r.ok else 0
    data = payload if payload is not None else {
        "max_unit": 32,
        "step_size": 1,
        "total": 20000
    }
    # NOTE generation must can not less or bigger than the current value.
    if "resource_provider_generation" not in data:
        data["resource_provider_generation"] = generation
    elif generation:
        data["resource_provider_generation"] =  generation
    _update_resource(url, data)

# OP for resource_providers aggregates
def get_resource_provider_aggregates(uuid):
    url = BASEURL + "resource_providers/" + uuid + "/aggregates"
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

# no this method
def delete_resource_provider_aggregates(uuid):
    url = BASEURL + "resource_providers/" + uuid +"/aggregates"
    r = requests.delete(url, headers=HEADERS)
    print "Delete a aggregate, and return: " + str(r.status_code)

def update_resource_provider_aggregates(uuid, payload=None):
    url = BASEURL + "resource_providers/" + uuid + "/aggregates"
    r = requests.get(url, headers=HEADERS)
    # NOTE aggregates can be everything, even not exist.
    data = payload if payload is not None else [
        "42896e0d-205d-4fe3-bd1e-100924931787",
        "5e08ea53-c4c6-448e-9334-ac4953de3cfa"
    ]
    _update_resource(url, data)

# OP for resource_classes
def create_resource_classe(name):
    _create_resource("resource_classes", name)

def delete_resource_classe(name):
    url = BASEURL + "resource_classes/" + name
    r = requests.delete(url, headers=HEADERS)
    print "Delete a resource_classes, and return: " + str(r.status_code)

def get_resource_classe(name):
    url = BASEURL + "resource_classes/" + name
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

# OP for traits
def create_trait(name):
    url = BASEURL + "traits/" + name
    r = requests.put(url, headers=HEADERS)
    if r.ok:
        print "Create trait with name: " + name + ", and return: " + str(r.status_code)
    else:
        print "Failed to create trait with name: " + name + ", and return: " + str(r.status_code)


def delete_trait(name):
    url = BASEURL + "traits/" + name
    r = requests.delete(url, headers=HEADERS)
    if r.ok:
        print "Delete trait with name: " + name + ", and return: " + str(r.status_code)
    else:
        print "Failed to delete trait with name: " + name + ", and return: " + str(r.status_code)

def get_traits():
    url = BASEURL + "traits"
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

def show_trait(name):
    url = BASEURL + "traits/" + name
    r = requests.get(url, headers=HEADERS)
    if r.ok:
        print "Get trait with name: " + name + ", and return: " + str(r.status_code)
    else:
        print "Failed to get trait with name: " + name + ", and return: " + str(r.status_code)

# OP for resource_providers traits
def get_resource_provider_traits(uuid):
    url = BASEURL + "resource_providers/" + uuid + "/traits"
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

def delete_resource_provider_traits(uuid):
    url = BASEURL + "resource_providers/" + uuid +"/traits"
    r = requests.delete(url, headers=HEADERS)
    print "Delete all traits, and return: " + str(r.status_code)

def update_resource_provider_traits(uuid, payload=None):
    url = BASEURL + "resource_providers/" + uuid +"/traits"
    r = requests.get(url, headers=HEADERS)
    generation = r.json()["resource_provider_generation"]
    data = payload if payload is not None else {
        "traits": [
            "CUSTOM_TEST"
        ]
    }
    if "resource_provider_generation" not in data:
        data["resource_provider_generation"] = generation
    _update_resource(url, data)

# OP for allocations
def update_allocations(uuid, res_uuid, res_name, payload=None):
    url = BASEURL + "allocations/" + uuid
    # NOTE allocations do not need generation
    # NOTE project_id and user_id can be arbitrary
    # NOTE resource number must be less than the amount
    # NOTE consumer_uuid can be arbitrary
    data = payload if payload is not None else {
        "allocations": [
            {
                "resource_provider": {
                    "uuid": res_uuid
                },
                "resources": {
                    res_name: 2,
                }
            },
        ],
        # "project_id": "6e3b2ce9-9175-4830-a862-b9de690bdceb",
        # "user_id": "81c516e3-5e0e-4dcb-9a38-4473d229a950"
    }
    _update_resource(url, data)

def delete_allocations(uuid):
    url = BASEURL + "allocations/" + uuid
    r = requests.delete(url, headers=HEADERS)
    print "Delete a allocations, and return: " + str(r.status_code)

def get_allocations(uuid):
    url = BASEURL + "allocations/" + uuid
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

# OP for resource_providers allocations
def get_resource_provider_allocations(uuid):
    url = BASEURL + "resource_providers/" + uuid + "/allocations"
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)


# OP for usages
def get_usages(**payload):
    """ payload params:
       project_id:
       user_id:
       payload = {"project_id", project_id}
    """
    # NOTE project_id and user_id can be in query.
    url = BASEURL + "usages"
    # url = url + "?project_id="+project_id
    # r = requests.get(url, headers=HEADERS)
    if "project_id" not in payload:
        payload["project_id"] = kstoken.project_id
    r = requests.get(url, headers=HEADERS, params=payload)
    if not r.ok:
        print r.content
    pretty_print(r)

# OP for resource_providers usages
def get_resource_provider_usages(uuid):
    url = BASEURL + "resource_providers/" + uuid + "/usages"
    r = requests.get(url, headers=HEADERS)
    pretty_print(r)

# OP for allocation_candidates
def get_allocation_candidates(**payload):
    """payload = {'resources': 'VCPU:4,DISK_GB:64,MEMORY_MB:2048'}"""
    url = BASEURL + "allocation_candidates"
    r = requests.get(url, headers=HEADERS, params=payload)
    pretty_print(r)

# ********************************************************
