#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Small module for use with the wake on lan protocol.

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import re
import socket
import struct
import sys

__author__ = 'Remco Haszing'
__license__ = 'WTFPL'
__email__ = 'remcohaszing@gmail.com'
__website__ = 'https://github.com/Trollhammaren/pywakeonlan'

BROADCAST_IP = '255.255.255.255'
DEFAULT_PORT = 9
help_message = """
Usage:
    %s [-i ip_address] [-p port] mac_address

  Options:
    -h              Show this help message.

    -i ip address   The broadcast ip address the magic packet should be
                    sent to.

    -p port         The port to which the package should be sent.

    mac_address     The mac address or hardware address of the computer
                    you are trying to wake.
"""


def create_magic_packet(macaddress):
    """
    Create a magic packet which can be used for wake on lan using the
    mac address given as a parameter.

    Keyword arguments:
    mac_address -- the mac address that should be parsed into a magic
            packet

    """
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream
    data = b'FFFFFFFFFFFF' + (macaddress * 20).encode()
    send_data = b''

    # Split up the hex values in pack
    for i in range(0, len(data), 2):
        send_data += struct.pack(b'B', int(data[i: i + 2], 16))
    return send_data


def send_magic_packet(*macs, **kwargs):
    """
    Wakes the computer with the given mac address if wake on lan is
    enabled on that host.

    Keyword arguments:
    :arguments macs: One or more macaddresses of machines to wake.
    :key ip_address: the ip address of the host to send the magic packet
                     to (default "255.255.255.255")
    :key port: the port of the host to send the magic packet to
               (default 9)

    """
    packets = []
    ip = kwargs.get('ip_address', BROADCAST_IP)
    port = kwargs.get('port', DEFAULT_PORT)
    for k in kwargs:
        raise TypeError('send_magic_packet() got an unexpected keyword '
                        'argument {!r}'.format(k))

    for mac in macs:
        packet = create_magic_packet(mac)
        packets.append(packet)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip, port))
    for packet in packets:
        sock.send(packet)
    sock.close()


if __name__ == '__main__':
    args = sys.argv
    ip_address = BROADCAST_IP
    port = DEFAULT_PORT
    mac_address = ''
    for i in range(1, len(args), 2):
        if args[i] == '-i':
            ip_address = args[i + 1]
        elif args[i] == '-p':
            port = int(args[i + 1])
        elif i is len(args) - 1:
            mac_address = args[i]
        else:
            sys.exit(help_message % args[0])

    if mac_address and send_magic_packet(mac_address, ip_address=ip_address,
                                                                    port=port):
        print('Magic packet sent succesfully.')
    else:
        print(help_message % args[0])
