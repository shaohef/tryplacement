#!/usr/bin/python
import requests
import json
import os

OS_USERNAME = os.environ.get("OS_USERNAME") if os.environ.get("OS_USERNAME") else "admin"
OS_PASSWORD = os.environ.get("OS_PASSWORD") if os.environ.get("OS_PASSWORD") else "123"
OS_PROJECT_NAME = os.getenv("OS_PROJECT_NAME") if os.getenv("OS_PROJECT_NAME") else "admin" 
OS_AUTH_URL = os.getenv("OS_AUTH_URL")

OS_PROJECT_DOMAIN_ID = os.getenv("OS_PROJECT_DOMAIN_ID") if os.getenv("OS_PROJECT_DOMAIN_ID") else "Default"
OS_USER_DOMAIN_ID = os.getenv("OS_USER_DOMAIN_ID") if os.getenv("OS_USER_DOMAIN_ID") else "Default"
OS_REGION_NAME = os.getenv("OS_REGION_NAME") if os.getenv("OS_REGION_NAME") else "RegionOne"

HOST = "127.0.0.1"

auth = {
    "auth": {
        "identity": {
            "methods": [
                "password"
            ],
            "password": {
                "user": {
                    "name": OS_USERNAME,
                    "domain": {
                        "name": OS_USER_DOMAIN_ID
                    },
                    "password": OS_PASSWORD 
                }
            }
        },
        "scope": {
            "project": {
                "name": OS_PROJECT_NAME,
               "domain": {
                   "name": OS_PROJECT_DOMAIN_ID 
               }
            }
        }
    }
}

# NOTE hardcode.
url = OS_AUTH_URL if OS_AUTH_URL else "http://%s/identity/v3/auth/tokens" % HOST
headers = {"Content-Type": "application/json"}
r = requests.post(url, data=json.dumps(auth), headers=headers)
data = r.json()
print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
project_id = data["token"]["project"]["id"] 
print project_id
token = r.headers['X-Subject-Token']
print token
