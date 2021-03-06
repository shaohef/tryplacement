#!/usr/bin/python

from lib.placement import *

# get_sub_resources("resource_classes")
create_resource_providers("NFS Share")
uuid = get_resource_provider_uuid("NFS Share")
get_resource_provider(uuid)
delete_resource_provider(uuid)
# get_sub_resources("resource_providers")
name = "CUSTOM_FPGA"
create_resource_classe(name)
get_resource_classe(name)
get_usages(project_id=kstoken.project_id)
uuid = get_resource_provider_uuid("just a test")
get_resource_provider_inventories(uuid)
update_resource_provider_inventories(uuid)
get_resource_provider_inventories(uuid)
update_resource_provider_inventories_resource_class(uuid, name)
get_resource_provider_inventories_resource_class(uuid, name)
user_uuid = str(uuidlib.uuid4())
update_allocations(user_uuid, uuid, name) 
get_allocations(user_uuid)
get_resource_provider_allocations(uuid)
print "=" * 80
get_allocation_candidates()
get_resource_provider_usages(uuid)
get_usages(project_id=kstoken.project_id)
delete_allocations(user_uuid)
get_usages(project_id=kstoken.project_id)
get_allocations(user_uuid)
delete_resource_provider_inventories_resource_class(uuid, name)
get_usages(project_id=kstoken.project_id)
get_resource_provider_inventories_resource_class(uuid, name)
delete_resource_provider_inventories(uuid)
get_usages(project_id=kstoken.project_id)
get_resource_provider_inventories(uuid)
delete_resource_classe(name)
get_usages(project_id=kstoken.project_id)
# get_sub_resources("resource_classes")
uuid = ramdom_shuffle(get_resource_provider_uuids())
print uuid
get_resource_provider_aggregates(uuid)
update_resource_provider_aggregates(uuid)
get_resource_provider_aggregates(uuid)
# get_resource_provider_inventories(uuid)

print get_resource_provider_uuids()

get_traits()
# NOTE trait must be upper, and starts with CUSTOM_
create_trait("CUSTOM_TEST")
create_trait("STOM_test")
show_trait("CUSTOM_TEST")
get_resource_provider_traits(uuid)
update_resource_provider_traits(uuid)
get_resource_provider_traits(uuid)
delete_resource_provider_traits(uuid)
get_resource_provider_traits(uuid)
delete_trait("CUSTOM_TEST")
get_traits()
