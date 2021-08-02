# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2020 PodGroup Ltd.
# 
# Authors : 
#   Kostiantyn Chertov <kostiantyn.chertov@podgroup.com>
#   J. Félix Ontañón <felix.ontanon@podgroup.com>

def swapNibbles(s):
    """ Swap nibbles of string s. """
    # return ''.join([chr((ord(x) >> 4) | ((ord(x) & 0x0F) << 4)) for x in s])
    sb = bytes.fromhex(s)
    return bytes([(x >> 4) | ((x & 0x0F) << 4) for x in sb])


def luhn_checksum(number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(number)
    odd_digits = digits[0::2]
    even_digits = digits[1::2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return 10 - (checksum % 10)


def iccid2bin(print_iccid):
    # ignore check digit if any and re-calculate it
    d = luhn_checksum(print_iccid[:18])
    # return binary encoding of ICCID
    return swapNibbles(print_iccid[:18] + chr(0x30 + d) + 'f')


if __name__ == '__main__':
    print_iccid = '8944503006204160204'
    bin_iccid = iccid2bin(print_iccid)
    assert bin_iccid == b'\x98\x44\x05\x03\x60\x02\x14\x06\x02\xf4'
    print('OK')