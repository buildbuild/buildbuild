from __future__ import absolute_import

from keystoneclient.v2_0 import client
from keystoneclient.exceptions import AuthSystemNotFound, InternalServerError

from swiftclient import client as swift_client
from celery import shared_task

# NOTES
# These tasks are only used in internal server. keystone service is only suitable in internal servert

@shared_task
def login_keystone_with_bypass():
    # For out_network access, this will be deprecated, because we will use this app in intranet.
    auth_url = 'http://61.43.139.143:5000/v2.0'
    token = '0120b90111df48feb5c727081afb859f'
    endpoint = 'http://61.43.139.143:35357/v2.0'

    # This information will be used real.
    #auth_url = 'http://172.16.100.169:5000/v2.0'
    #token = '0120b90111df48feb5c727081afb859f'
    #endpoint = 'http://172.16.100.169:35357/v2.0'

    keystone = client.Client(
                    auth_url = auth_url,
                    token = token,
                    endpoint = endpoint
                )

    if keystone is None:
        raise AuthSystemNotFound("With this information, we can not use keystone service, check information")

    return keystone


@shared_task
def create_keystone_account(keystone, user, password, project_name):

    # for user custom object tenant, some steps maybe need
    # 1. create tenant.
    # 2. get tenant_id
    # 3. user creation
    # 4. user role add to this tenant. this tenant will be used for uploading user custom files

    # project name is equal to tenant name in swift, keystone
    tenant_name = user + "__" + project_name

    tenant = keystone.tenants.create(tenant_name=tenant_name,
                                 description=tenant_name +
                                             "tenant name consists of user name and project name", enabled=True)

    # Getting tenant_id
    tenant_id = tenant.id
    tenant_id = tenant_id.encode('ascii', 'ignore')

    # user creation
    user = keystone.users.create(name = user,
                             password = password,
                             tenant_id = tenant_id
                            )

    # get member role in role list
    member_role = None

    for token in keystone.roles.list():
        if token.name == 'member':
            member_role = token

    keystone.roles.add_user_role(user = user,
                             role = member_role,
                             tenant = tenant)

    if user is None:
        raise InternalServerError("User creation failed, check your user name and project name are not duplicated.")

    return user


def create_container_swift(user_name, user_pass, tenant_name):
    #This will be deprecated.
    swift_auth_url = "http://61.43.139.143:5000/v2.0"
    # This info will be used in real
    # swift_auth_url = "http://172.16.100.169:5000/v2.0"
    swift_conn = swift_client.Connection(authurl=swift_auth_url,
                                     user=user_name,
                                     key=user_pass,
                                     tenant_name=tenant_name,
                                     auth_version=2)

    pass


def list_objects_in_container_swift():
    # Not implemented
    pass


def store_object_into_container_swift():
    # Not implemented
    pass


def get_object_from_container_swift():
    # Not implemented
    pass