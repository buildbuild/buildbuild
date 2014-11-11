from __future__ import absolute_import

from keystoneclient.v2_0 import client
from keystoneclient.exceptions import AuthSystemNotFound
from celery import shared_task

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