#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This project is hosted on https://github.com/Trollhammaren/pywakeonlan
#
# Copyright (c) 2012 Remco Haszing
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# Except as contained in this notice, the name(s) of the above
# copyright holders shall not be used in advertising or otherwise
# to promote the sale, use or other dealings in this Software
# without prior written authorization.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import re
import socket

BROADCAST_IP_ADDRESS = "255.255.255.255"
DEFAULT_PORT = 9
help_message = \
"""
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
    
    mac_address -- the mac address that should be parsed into a magic
            packet
    
    """
    hex = "[a-fA-F0-9]"
    if re.compile("^(%s{2}[:|\-]?){6}$" % hex).match(mac_address):
        regex = "%s{2}" % hex
    elif re.compile("^%s{12}$" % hex).match(mac_address):
        regex = ".."
    else:
        print("Invalid mac address: %s" % str(mac_address))
        return False
    
    mac_address = re.findall(regex, mac_address)
    return "\xFF" * 6 + "".join(map(lambda x: chr(int('0x%s' % x, 0)), mac_address)) * 16

def send_magic_packet(mac_address, ip_address=BROADCAST_IP_ADDRESS, port=DEFAULT_PORT):
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
    if type(mac_address) == str:
        packet = create_magic_packet(mac_address)
        if packet:
            packets += [packet]
    elif type(mac_address) == list:
        for mac in mac_address:
            packet = create_magic_packet(mac_address)
            if packet:
                packets += [packet]
    
    if not len(packets):
        return False
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip_address, port))
    for packet in packets:
        sock.send(packet)
    sock.close()
    return True

if __name__ == "__main__":
    import sys
    args = sys.argv
    ip_address = BROADCAST_IP_ADDRESS
    port = DEFAULT_PORT
    mac_address = ""
    for i in range(1, len(args), 2):
        if args[i] == "-i":
            ip_address = args[i + 1]
        elif args[i] == "-p":
            port = int(args[i + 1])
        elif i is len(args) - 1:
            mac_address = args[i]
        else:
            sys.exit(help_message % args[0])
    
    success = send_magic_packet(mac_address, ip_address=ip_address, port=port)
    print("Magic packet sent succesfully." if success else help_message % args[0])

