#!/usr/bin/python

import kstoken

import requests
import json
import os
import random
import uuid as uuidlib
import sys


HOST = "127.0.0.1"
HOSTURL = "http://%s" % HOST
BASEURL = "http://%s/image" % HOST

HEADERS = {"Content-Type": "application/json",
           "OpenStack-API-Version": "placement latest",
           "X-Auth-Token": kstoken.token}


def pretty_print(r):
    if not r.ok:
        print r.content
        return
    data = r.json()
    res = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    print res
    return data



# OP for glance
def get_all_fpga_image(**payload):
    """payload = {'tag': 'FPGA'}"""
    params = {'tag': 'FPGA'}
    params.update(payload)
    url = BASEURL + "/v2/images"
    r = requests.get(url, headers=HEADERS, params=payload)
    res = pretty_print(r)
    return res

# ********************************************************
