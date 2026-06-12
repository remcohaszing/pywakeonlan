#!/usr/bin/env python3
"""
Small module for use with the wake on lan protocol.

"""

import argparse
import socket


BROADCAST_IP = '255.255.255.255'
DEFAULT_PORT = 9


def create_magic_packet(macaddress: str) -> bytes:
    """
    Create a magic packet.

    A magic packet is a packet that can be used with the for wake on lan
    protocol to wake up a computer. The packet is constructed from the
    mac address given as a parameter.

    Args:
        macaddress: the mac address or a "mac address/secureon password" tuple
            that should be parsed into a magic packet.

    """
    secureon = ''
    if '/' in macaddress:
        (macaddress, secureon) = macaddress.split('/')

    if len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    elif len(macaddress) == 14:
        sep = macaddress[4]
        macaddress = macaddress.replace(sep, '')
    if len(macaddress) != 12:
        raise ValueError('Incorrect MAC address format')

    if secureon:
        if len(secureon) == 17:
            sep = secureon[2]
            secureon = secureon.replace(sep, '')
        elif len(secureon) == 14:
            sep = secureon[4]
            secureon = secureon.replace(sep, '')
        if len(secureon) != 12:
            raise ValueError('Incorrect SecureOn password format')

    return bytes.fromhex('F' * 12 + macaddress * 16 + secureon)


def create_socket(
    *,
    ip_address: str = BROADCAST_IP,
    port: int = DEFAULT_PORT,
    interface: str | None = None,
    address_family: socket.AddressFamily = socket.AF_UNSPEC,
) -> socket.socket:
    """
    Create a socket that’s suitable for sending magic packets.

    Args:
        ip_address: The hostname to connect to.
        port: The port to connect to.
        interface: The IP address of the network adapter to use.
        address_family: The address family to send the magic packet to.
            Use this to force the use of IPv4 or IPv6. The default is
            to auto detect.

    Returns:
        A socket you can use for sending magic packets.

    """
    # This is based on the example for a connection that supports both IPv4
    # and IPv6 in https://docs.python.org/3/library/socket.html#example
    # This also matches the getaddrinfo man page, which states applications
    # should try using the addresses in order.
    # https://man7.org/linux/man-pages/man3/getaddrinfo.3.html
    address_infos = socket.getaddrinfo(
        ip_address, port, address_family, socket.SOCK_DGRAM
    )
    sock: socket.socket | None = None
    for index, (family, type, proto, canonname, addr) in enumerate(address_infos, 1):
        try:  # pragma: nocover
            sock = socket.socket(family, type, proto)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            if interface:
                sock.bind((interface, 0))
            sock.connect(addr)
            break
        except OSError:  # pragma: nocover
            if sock:
                sock.close()
            sock = None
            if index == len(address_infos):
                raise
    assert sock, 'sock should be defined at this point'
    return sock


def send_magic_packet(
    *macs: str,
    ip_address: str = BROADCAST_IP,
    port: int = DEFAULT_PORT,
    interface: str | None = None,
    address_family: socket.AddressFamily = socket.AF_UNSPEC,
) -> None:
    """
    Wake up computers having any of the given mac addresses.

    Wake on lan must be enabled on the host device.

    Args:
        macs: One or more mac addresses or "mac address/secureon password"
            tuples of machines to wake.

    Keyword Args:
        ip_address: the ip address of the host to send the magic packet
            to.
        port: the port of the host to send the magic packet to.
        interface: the ip address of the network adapter to route the
            magic packet through.
        address_family: the address family of the ip address to initiate
            connection with. When not specificied, chosen automatically
            between IPv4 and IPv6.

    """
    packets = [create_magic_packet(mac) for mac in macs]

    with create_socket(
        ip_address=ip_address,
        port=port,
        interface=interface,
        address_family=address_family,
    ) as sock:
        for packet in packets:
            sock.send(packet)


def main(argv: list[str] | None = None) -> None:
    """
    Run wake on lan as a CLI application.

    """
    parser = argparse.ArgumentParser(
        description='Wake one or more computers using the wake on lan protocol.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'macs',
        metavar='mac address',
        nargs='+',
        help='The mac addresses or "mac address/secureon password" tuples of the computers you are trying to wake.',
    )
    parser.add_argument(
        '-4',
        '--ipv4',
        action='store_true',
        help='To indicate ipv4 should be used.',
    )
    parser.add_argument(
        '-6',
        '--ipv6',
        action='store_true',
        help='To indicate ipv6 should be used.',
    )
    parser.add_argument(
        '-i',
        '--ip',
        default=BROADCAST_IP,
        help='The ip address of the host to send the magic packet to.',
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=DEFAULT_PORT,
        help='The port of the host to send the magic packet to.',
    )
    parser.add_argument(
        '-n',
        '--interface',
        help='The ip address of the network adapter to route the magic packet through.',
    )
    args = parser.parse_args(argv)
    if args.ipv4 is args.ipv6:
        address_family = socket.AF_UNSPEC
    elif args.ipv4:
        address_family = socket.AF_INET
    elif args.ipv6:
        address_family = socket.AF_INET6
    send_magic_packet(
        *args.macs,
        ip_address=args.ip,
        port=args.port,
        interface=args.interface,
        address_family=address_family,
    )


if __name__ == '__main__':  # pragma: nocover
    main()
