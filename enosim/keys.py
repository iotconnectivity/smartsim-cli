#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 PodGroup Ltd.
#
# Authors:
#   J. Félix Ontañón <felix.ontanon@podgroup.com>
#   Kostiantyn Chertov <kostiantyn.chertov@podgroup.com>

import string
import base64

from Crypto.Cipher import AES
from Crypto import Random
# from Crypto.Random import get_random_bytes
from Crypto.Random.random import choice

from enosim.iccid import iccid2bin

LEN_AES_BLOCK = 16
LEN_KCV = 3
LEN_ICCID_STR = 18

punctuation_without_colon = r"""!"#$%&'()*+,-./;<=>?@[\]^_`{|}~"""


# From https://bitbucket.org/podsystem/simapp-to-cloud-server/src/master/scripts/psk_generator.py
def pad(data):
    length = (LEN_AES_BLOCK - ((len(data)) % LEN_AES_BLOCK)) % LEN_AES_BLOCK
    return data + bytes(length)

# def unpad(data):
#     data = data[1:]
#     pad_start = 0
#     for i in range(0, len(data)):
#         pad_start = pad_start + 1
#         if data[i] == 0:
#             break
#     return data[:pad_start + 1]


def encrypt(message, key):
    IV = Random.new().read(LEN_AES_BLOCK)
    aes = AES.new(key, AES.MODE_CBC, IV)
    # print(len(pad(message)))
    return base64.b64encode(IV + aes.encrypt(pad(message)))


# def decrypt(encrypted, key):
#     encrypted = base64.b64decode(encrypted)
#     IV = encrypted[:LEN_AES_BLOCK]
#     aes = AES.new(key, AES.MODE_CBC, IV)
#     return unpad(aes.decrypt(encrypted[LEN_AES_BLOCK:]))
#
#
# From Kostiantyn script
def kcv(key):
    cipher = AES.new(key, AES.MODE_ECB)
    block = bytearray(LEN_AES_BLOCK)
    enc = cipher.encrypt(block)
    return enc[:LEN_KCV]


# Functions to export
def get_random_psk():
    chars = string.ascii_letters + string.digits + punctuation_without_colon
    ks = ''.join(choice(chars) for i in range(LEN_AES_BLOCK))
    key = bytes(ks, 'utf-8')
    return key.hex()


def get_encoded_psk(key_hex):
    key_bytes = bytes.fromhex(key_hex)
    check_value = kcv(key_bytes)
    return key_bytes.decode('utf-8'), check_value.hex()


def get_encrypted_psk(iccid, psk, key):
    enc_key = encrypt(str.encode(iccid + ":" + psk), str.encode(key))
    return enc_key.decode('utf-8')
