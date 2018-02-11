#!/usr/bin/python

import datetime
import hashlib
import os

from oslo_utils import timeutils
from oslo_utils import units

from lib.placement import *
from lib.glance import *
#    timestamp = datetime.datetime.utcnow()
#    timeutils.is_older_than()

# define the NAME and ID with lower case.
VENDOR_NAME_ID_MAPS = {"intel": "0x8086"}
VENDOR_ID_NAME_MAPS = dict(map(reversed, VENDOR_NAME_ID_MAPS.items()))
FGPA_IMGAGE_PATH = "./fpgas"
TEST_FILE = "/home/ubuntu/api_tests/token.json"

# glance image API usage example: ref nova/virt/libvirt/utils.py
# from nova.virt import images
# nova/virt/images.py
# IMAGE_API = image.API()
# glance image conf example: ref nova/conf/glance.py
# local cache
ALL_IMAGES = {
    # should it be image object list? ref: nova/objects/image_meta.py
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


def download_image(uuid, md5):
    if not os.path.lexists(FGPA_IMGAGE_PATH):
        os.makedirs(FGPA_IMGAGE_PATH)
    image = os.path.join(FGPA_IMGAGE_PATH, uuid)
    if not os.path.lexists(image):
        # HTTP Download
        os.mknod(image)
        image_md5 = hash_for_file(TEST_FILE)
        if md5 != image_md5:
            raise Exception("Download an incomplete image.")
        md5_file = image + "_md5"
        with open(md5_file, 'w') as f:
            f.write(image_md5)


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


def hash_for_file(path, algorithm=hashlib.algorithms[0],
                  block_size= 64 * units.Mi, human_readable=True):
    """
    Block size directly depends on the block size of your filesystem
    to avoid performances issues
    NTFS has blocks of 4096 octets by default.

    Linux Ext4 block size
    sudo tune2fs -l /dev/sda5 | grep -i 'block size'
    > Block size:               4096

    Input:
        path: a path
        algorithm: an algorithm in hashlib.algorithms
                   ATM: ('md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512')
        block_size: a multiple of 128 corresponding to the block size of your
                    filesystem. Here keep the same value of glance by default.
        human_readable: switch between digest() or hexdigest() output,
                        default hexdigest()
    Output:
        hash
    """
    if algorithm not in hashlib.algorithms:
        raise NameError('The algorithm "{algorithm}" you specified is '
                        'not a member of "hashlib.algorithms"'
                        ''.format(algorithm=algorithm))

    # According to hashlib documentation using new()
    # will be slower then calling using named
    # constructors, ex.: hashlib.md5()
    hash_algo = hashlib.new(algorithm)

    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
             hash_algo.update(chunk)
    if human_readable:
        file_hash = hash_algo.hexdigest()
    else:
        file_hash = hash_algo.digest()
    return file_hash


if update_images():
    t, r = gen_traits_and_resource_class(ALL_IMAGES)
    print t, "_".join(r)

md5 = hash_for_file(TEST_FILE)
download_image("123456", md5)
# if NONE, update images.
vendor = get_vendor_from_resource_name("CUSTOM_FPGA_INTEL_CRYPTO")
vendors = get_vendors()
print vendor, vendors, vendor in vendors
print from_resource_name_uuid("CUSTOM_FPGA_INTEL_CRYPTO")
