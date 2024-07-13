#!/usr/bin/env python3
"""
Small module for use with the wake on lan protocol.

"""
import argparse
import ipaddress
import socket
import typing


BROADCAST_IP: str = '255.255.255.255'
DEFAULT_PORT: int = 9
DEFAULT_TTL: int = 128


def create_magic_packet(mac_address: str) -> bytes:
    """
    Create a magic packet.

    A magic packet is a packet that can be used with the for wake on lan
    protocol to wake up a computer. The packet is constructed from the
    mac address given as a parameter.

    Args:
        mac_address: the mac address that should be parsed into a magic packet.

    """
    if len(mac_address) == 17:
        sep = mac_address[2]
        mac_address = mac_address.replace(sep, '')
    elif len(mac_address) == 14:
        sep = mac_address[4]
        mac_address = mac_address.replace(sep, '')
    if len(mac_address) != 12:
        raise ValueError('Incorrect MAC address format')

    return bytes.fromhex('F' * 12 + mac_address * 16)


def send_magic_packet(
        *macs: str,
        ip_address: str = BROADCAST_IP,
        port: int = DEFAULT_PORT,
        ttl: int = DEFAULT_TTL,
        interface: typing.Optional[str] = None,
        address_family: typing.Optional[socket.AddressFamily] = None,
        ) -> None:
    """
    Wake up computers having any of the given mac addresses.

    Wake on lan must be enabled on the host device.

    Args:
        macs: One or more mac-addresses of machines to wake.

    Keyword Args:
        ip_address: the ip address of the host to send the magic packet
            to.
        port: the port of the host to send the magic packet to.
        ttl: the ttl value to be set in the broadcast packet
        interface: the ip address of the network adapter to route the
            magic packet through.
        address_family: the address family of the ip address to initiate
            connection with. When not specified, chosen automatically
            between IPv4 and IPv6.

    """
    packets: list[bytes] = [create_magic_packet(mac_address=mac) for mac in macs]

    if address_family is None:
        address_family = (
            socket.AF_INET6 if _is_ipv6_address(ip_address) else socket.AF_INET
        )

    with socket.socket(address_family, socket.SOCK_DGRAM) as sock:
        if interface is not None:
            sock.bind((interface, 0))

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, ttl)
        sock.connect((ip_address, port))

        for packet in packets:
            sock.send(packet)


def _is_ipv6_address(ip_address: str) -> bool:
    try:
        return isinstance(ipaddress.ip_address(ip_address), ipaddress.IPv6Address)

    except ValueError:
        return False


def ttl_validator(ttl_value: str) -> int:
    try:
        result: int = int(ttl_value)
        if not (1 <= result <= 255):
            raise argparse.ArgumentTypeError("TTL value must be between 1 and 255")

        return result

    except ValueError:
        raise argparse.ArgumentTypeError("TTL value must be an integer")


def main(argv: typing.Optional[typing.List[str]] = None) -> None:
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
        help='The mac addresses of the computers you are trying to wake.',
    )
    parser.add_argument(
        '-6',
        '--ipv6',
        action='store_true',
        help='To indicate if ipv6 should be used by default instead of ipv4.',
    )
    parser.add_argument(
        '-i',
        '--ip',
        default=BROADCAST_IP,
        help='The ip address of the host to send the magic packet to. (default: 255.255.255.255)',
    )
    parser.add_argument(
        '-p',
        '--port',
        type=int,
        default=DEFAULT_PORT,
        help='The port of the host to send the magic packet to. (default: 9)',
    )
    parser.add_argument(
        '-n',
        '--interface',
        help='The ip address of the network adapter to route the magic packet through.',
    )
    parser.add_argument(
        '-t',
        '--ttl',
        type=ttl_validator,
        default=DEFAULT_TTL,
        help='The TTL (time-to-live) value of the broadcast packet. (min: 1, max: 255, default: 128)',
    )
    args = parser.parse_args(argv)
    send_magic_packet(
        *args.macs,
        ip_address=args.ip,
        port=args.port,
        ttl=args.ttl,
        interface=args.interface,
        address_family=socket.AF_INET6 if args.ipv6 else None,
    )


if __name__ == '__main__':  # pragma: nocover
    main()
