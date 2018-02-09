#!/usr/bin/python

import datetime
import os

from oslo_utils import timeutils

from lib.placement import *
from lib.glance import *
#    timestamp = datetime.datetime.utcnow()
#    timeutils.is_older_than()

# define the NAME and ID with lower case.
VENDOR_NAME_ID_MAPS = {"intel": "0x8086"}
VENDOR_ID_NAME_MAPS = dict(map(reversed, VENDOR_NAME_ID_MAPS.items()))
FGPA_IMGAGE_PATH = "./fpgas"

# local cache
ALL_IMAGES = {
    "images": {},
    "updated_at": "2000-01-01T00:00:00Z"}

def update_images():
    global ALL_IMAGES
    query = {"updated_at": "gt:%s" % ALL_IMAGES["updated_at"]}
    r = get_all_fpga_image(**query)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    ALL_IMAGES["updated_at"] = timestamp
    for i in r["images"]:
        if i["id"] not in ALL_IMAGES["images"]:
            ALL_IMAGES["images"].update({i["id"]: i})
    return not not r["images"]


def get_vendors():
    # vs get from drivers, can be a parameters.
    vs = ["0x8086"]
    ret = set()
    for v_id in vs:
        if v_id.lower() in VENDOR_ID_NAME_MAPS.keys():
            ret.add(v_id.upper())
        v_name = VENDOR_ID_NAME_MAPS.get(v_id.lower(), v_id)
        ret.add(v_name.upper())
    return ret


def vendor_id_to_name(v_id):
    if not v_id:
        return v_id
    vendor = VENDOR_ID_NAME_MAPS.get(v_id.lower(), v_id)
    vendor.upper()
    return vendor


def vendor_name_to_id(name):
    if not name:
        return name
    v_id = VENDOR_NAME_ID_MAPS.get(name.lower(), name)
    v_id.upper()
    return v_id


def gen_traits_and_resource_class(images):
    traits = set()
    # CUSTOM_FPGA_VENDOR_TYPE
    resource_classes = ["CUSTOM", "FPGA"]
    for i, img in images["images"].items():
        tags = set([x.upper() for x in img["tags"]])
        vendors = get_vendors()
        v_name = vendor_id_to_name(img.get("vendor"))
        if v_name and v_name in vendors:
            traits.update(tags)
            resource_classes.append(v_name)
        elif tags & vendors:
            traits.update(tags)
            v_name = vendor_id_to_name(list(tags & vendors)[0])
            resource_classes.append(v_name)
        fpga_type = img.get("type")
        if fpga_type:
            resource_classes.append(fpga_type.upper())
    return traits, resource_classes


def download_image(uuid):
    if not os.path.lexists(FGPA_IMGAGE_PATH):
        os.makedirs(FGPA_IMGAGE_PATH)
    image = os.path.join(FGPA_IMGAGE_PATH, uuid)
    if not os.path.lexists(image):
        # HTTP Download
        os.mknod(image)


def get_vendor_from_resource_name(name):
    return name.split("_")[2] if name.count("_") > 1 else None


def from_resource_name_uuid(name):
    if name.count("_") < 3:
        return
    infos = name.split("_")[2:]
    vend, typ = infos[:2]
    vend = vend.upper()
    typ = typ.upper()
    # img_info = dict(zip(["vendor", "type"], infos))
    for k, img in ALL_IMAGES["images"].items():
        i_vendor = img.get("vendor")
        i_typ = img.get("type")
        tags = set([x.upper() for x in img["tags"]])
        if typ == i_typ.upper():
            if vend == i_vendor.upper():
                return k
            v_id = vendor_name_to_id(vend)
            if v_id == i_vendor.upper():
                return k
            if v_id in tags or vend in tags:
                return k


if update_images():
    t, r = gen_traits_and_resource_class(ALL_IMAGES)
    print t, "_".join(r)

download_image("123456")
# if NONE, update images.
vendor = get_vendor_from_resource_name("CUSTOM_FPGA_INTEL_CRYPTO")
vendors = get_vendors()
print vendor, vendors, vendor in vendors
print from_resource_name_uuid("CUSTOM_FPGA_INTEL_CRYPTO")
