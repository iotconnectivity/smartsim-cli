#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 Pod Group Ltd.
#
# Authors:
#   - Kostiantyn Chertov <kostiantyn.chertov@podgroup.com>
#   - J. Félix Ontañón <felix.ontanon@podgroup.com>

import socket
import time
from tlspsk import TLSClientSession

from enosim.logger import logger
from enosim.iccid import iccid2bin


def __tlssession(server, port, sim_key, sim_iccid, request):
    quit = False
    sock = None

    def callback(data):
        nonlocal quit, sock
        logger.info(data)
        if data == b"bye\n":
            quit = True

    psk = bytes.fromhex(sim_key)
    session = TLSClientSession(
        server_names=server, psk=psk, psk_label=bytes.fromhex(sim_iccid), data_callback=callback, psk_only=True
    )

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, port))
    client_hello = session.pack_client_hello()
    logger.debug('client hello: {0}'.format(client_hello.hex()))
    sock.sendall(client_hello)

    parser = session.parser()
    step = 0
    logger.info('TLS1.3-PSK session established. Initialising operation.')

    while not quit:
        step += 1
        server_data = sock.recv(10*4096)
        if len(server_data) > 0:
            logger.debug("step {0}: {1}".format(step, server_data.hex()))
        parser.send(server_data)
        data = parser.read()
        if data:
            logger.debug("data: {0}".format(data.hex()))
            sock.sendall(data)
            quit = True

    data = bytes(request, 'utf-8')

    logger.debug('request: {0}'.format(data))
    app_data = session.pack_application_data(data)
    logger.debug('app_data: {0}'.format(app_data.hex()))

    sock.sendall(app_data)
    time.sleep(1)
    resp = sock.recv(4096)
    logger.debug('resp: {0}'.format(resp.hex()))
    parser.send(resp)

    time.sleep(0.5)
    resp = sock.recv(4096)
    logger.debug('resp: {0}'.format(resp.hex()))
    parser.send(resp)

    sock.sendall(session.pack_close())
    sock.close()
    logger.debug('done!')


def simulate_ztp(server, port, sim_key, sim_iccid, device_id):
    nibbled_iccid = iccid2bin(sim_iccid).hex()
    request = 'GET /v1/config/{0}?iccid={1} HTTP/1.1\x0d\x0a\x0d\x0a'.format(device_id, nibbled_iccid)
    logger.debug('request: {}'.format(request))

    return __tlssession(server, port, sim_key, nibbled_iccid, request)


def simulate_stc(server, port, sim_key, sim_iccid, device_id, json_data):
    data_length = len(json_data)
    nibbled_iccid = iccid2bin(sim_iccid).hex()
    request = 'POST /v1/data/{0}?iccid={1} HTTP/1.1\x0d\x0a'.format(device_id, nibbled_iccid) +\
        'Host: pod.iot.platform\x0d\x0a' +\
        'Content-Length: {0:d}\x0d\x0a\x0d\x0a{1}'.format(data_length, json_data)
    logger.debug('request: {}'.format(request))

    return __tlssession(server, port, sim_key, nibbled_iccid, request)
