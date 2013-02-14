#!/usr/bin/python

"""
Small module for use with the wake on lan protocol.

"""

from __future__ import unicode_literals

import re
import socket
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


def create_magic_packet(mac_address):
    """
    Create a magic packet which can be used for wake on lan using the
    mac address given as a parameter.

    Keyword arguments:
    mac_address -- the mac address that should be parsed into a magic
            packet

    """
    hex = '[a-fA-F0-9]'
    if re.compile('^(%s{2}[:|\-]?){5}(%s{2})$' % ((hex,) * 2)).match(
                                                                mac_address):
        regex = '%s{2}' % hex
    elif re.compile('^%s{12}$' % hex).match(mac_address):
        regex = '..'
    else:
        print('Invalid mac address: %s' % mac_address)
        return False

    mac_address = re.findall(regex, mac_address)
    return '\xFF' * 6 +\
                ''.join([chr(int('0x%s' % x, 0)) for x in mac_address]) * 16


def send_magic_packet(mac_address, ip_address=BROADCAST_IP, port=DEFAULT_PORT):
    """
    Wakes the computer with the given mac address if wake on lan is
    enabled on that host.

    Keyword arguments:
    mac_address -- either the mac address of the host machine to wake
            as a string or a list of mac addresses
    ip_address -- the ip address of the host to send the magic packet
            to (default "255.255.255.255")
    port -- the port of the host to send the magic packet to
            (default 9)

    """
    packets = []

    def add_packet(packets, mac_address):
        packet = create_magic_packet(mac_address)
        if packet:
            # Required for Python 3.x
            if sys.version_info[0] == 3:
                packet = bytes(packet, 'UTF-8')
            packets += [packet]

    if type(mac_address) in [str, unicode]:
        add_packet(packets, mac_address)
    elif type(mac_address) == list:
        for mac in mac_address:
            add_packet(packets, mac)

    if not packets:
        return False

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip_address, port))
    for packet in packets:
        sock.send(packet)
    sock.close()
    return True


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
