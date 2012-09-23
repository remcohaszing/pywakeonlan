#!/usr/bin/python

import re
import socket

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

def send_magic_packet(mac_address, ip_address="255.255.255.255", port=7):
    """
    Wakes the computer with the given mac address if wake on lan is
    enabled on that host.
    
    Keyword arguments:
    mac_address -- the mac address of the host machine to wake
    ip_address -- the ip address of the host to send the magic packet to
            (default "255.255.255.255")
    port -- the port of the host to send the magic packet to (default 7)
    
    """
    hex = "[a-fA-F0-9]"
    if re.compile("^(%s{2}[:|\-]?){6}$" % hex).match(mac_address):
        regex = "%s{2}" % hex
    elif re.compile("^%s{12}$" % hex).match(mac_address):
        regex = ".."
    else:
        return False
    
    mac_address = re.findall(regex, mac_address)
    packet = "\xFF" * 6 +\
            "".join(map(lambda x: chr(int('0x%s' % x, 0)), mac_address)) * 16
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(packet, (ip_address, port))
    return True

def wake_multi(mac_addresses, ip_address="255.255.255.255", port=7):
    """
    Send the magic packet to multiple machines.
    
    Keyword arguments:
    mac_addresses -- the mac addresses of the machines to wake
    ip_address -- the ip address of the host to send the magic packet to
            (default "255.255.255.255")
    port -- the port of the host to send the magic packet to (default 7)
    
    """
    for mac_address in mac_addresses:
        send_magic_packet(macaddress, ip_address=ip_address, port=port)

if __name__ == "__main__":
    import sys
    args = sys.argv
    ip_address = "255.255.255.255"
    port = 7
    mac_address = ""
    for i in range(1, len(args), 2):
        if args[i] == "-i":
            ip_address = args[i + 1]
        elif args[i] == "-p":
            port = int(args[i + 1])
        elif i is len(args) - 1:
            mac_address = args[i]
        else:
            sys.exit(help_message)
    
    success = send_magic_packet(mac_address, ip_address=ip_address, port=port)
    print("Magic packet sent succesfully." if success else help_message)

