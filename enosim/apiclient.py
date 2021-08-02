# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2020 PodGroup Ltd.
# 
# Authors : 
#   Kostiantyn Chertov <kostiantyn.chertov@podgroup.com>
#   J. Félix Ontañón <felix.ontanon@podgroup.com>

import json
import requests
import datetime

from enosim.iccid import iccid2bin

# HTTP OK standard response code
SERVER_OK = 200


# Decorator to check and cache auth token
def check_auth(f):
    def wrapper(*args, **kwargs):
        if not args[0].token:
            args[0].get_token()
        return f(*args)
    return wrapper


class IoTSIMServiceConn:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.token = ''

    def get_token(self):
        r = requests.get(self.hostname + '/admin/login/', 
            headers = {'username': self.username, 'password': self.password}
        )
        
        if r.status_code == SERVER_OK:
            res = r.json()
            self.token = res['token']
        else:
            r.raise_for_status()    

    @check_auth
    def update_psk(self, iccid, encrypted_key):
        r = requests.put(self.hostname + '/admin/psk', 
            data = json.dumps({'iccid': iccid, 'psk': encrypted_key}),
            headers = {
                'access-token': self.token,
                'Content-Type': 'application/json'
            }
        )

        return r

    @check_auth
    def create_config(self, device_id, sim_iccid, jsondata):
        nibbled_iccid = iccid2bin(sim_iccid).hex()

        payload = {"configuration": {
            "version": datetime.datetime.now().strftime(format='%Y-%m-%d'),
            "config": json.loads(jsondata)
        }}

        r = requests.post(self.hostname + '/config/' + device_id + '?iccid=' + nibbled_iccid, 
            data = json.dumps(payload),
            headers = {
                'access-token': self.token,
                'Content-Type': 'application/json'
            }
        )

        return r

    @check_auth
    def get_data(self, device_id):
        return requests.get(self.hostname + '/data/' + device_id,
            headers = {
                'access-token': self.token,
                'accept': 'application/json'
            }
        )
