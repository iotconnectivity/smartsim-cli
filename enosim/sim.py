# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2020 PodGroup Ltd.
# 
# Authors : 
#   Kostiantyn Chertov <kostiantyn.chertov@podgroup.com>
#   J. Félix Ontañón <felix.ontanon@podgroup.com>

# Refer to MultiProtocol Sender SIM App Tech Spec:
# https://docs.google.com/document/d/1sLmI1XxmRJ90C2WDd0YI7A4YYt42d-DHn_lH6KzcZ5w

import os
import sys

import asterix

from enosim.logger import logger


# Pod Sender Applet AID
AID = 'f0706f6467730101ff'

# APDU response codes
OK = 0x9000


# Decorator to prevent asterix to populate the stdout with traces
def noprint(func):
    def inner(*args, **kwargs):
        sys.stdout = open(os.devnull, "w")
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            sys.stdout = sys.__stdout__
            raise e
        sys.stdout = sys.__stdout__
        return result
    return inner


# Decorator to check there's asterix connection made and cache it on the SIMCardManager object.
def check_conn(f):
    def wrapper(*args, **kwargs):
        if not args[0].conn:
            if not args[0].connect_card():
                return
        return f(*args)
    return wrapper


class SIMCardManager:
    def __init__(self):
        self.conn = None

    @noprint
    def connect_card(self):
        try:
            self.conn = asterix.mycard.connectCard()
        except:
            logger.error('Cannot read card, is it inserted?')
            return False

        if not self.conn:
            logger.error('Cannot connect with usb sim reader, is it plugged?')
            return False

        return True

    @check_conn
    @noprint
    def get_iccid(self):
        apdu = asterix.APDU

        self.conn.send('00A40004023F00')
        self.conn.send('00A40004022FE2')

        response = apdu.readBinary(self.conn, 0x0A)
        iccid = apdu.swapNibbles(response).hex().strip('f')
        return iccid.strip('f')

    @check_conn
    @noprint
    def put_psk(self, psk_hex, kcv_hex):
        # SELECT[applet]
        p1, p2 = self.conn.send('00a40400{0:02x}{1}'.format(len(AID) // 2, AID))

        if p2 != OK:
            logger.error('Cannot select Sender APPLET. Is the applet installed? APDU Response Code (int): %s' % p2)
            return False
        else:
            # PUT KEY (KVN | Key Type | Key Length | Key Value | KCV Length)
            p1, p2 = self.conn.send('80d80000 14 01 88 10 {} 00'.format(psk_hex))

            if p2 != OK:
                logger.error('PUT KEY command failed with. APDU Response Code (int): %s' % p2)
            else:
                if kcv_hex not in p1.hex():
                    logger.error('KCV verification failed. Preshared Key (PSK) might be installed incorrectly. Expected KVC: {0} | PUT KEY Respond: {1}'.format(kcv_hex, p1.hex()))
                    return False
        
        return True


if __name__ == '__main__':
    simcard = SIMCardManager()
    logger.info(simcard.get_iccid())
    simcard.put_psk('2aa9fd98d4888250036b24dfcd4368da', '36dc28')