"""
Tests for wakeonlan.

"""
import socket
from typing import List
from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import patch

import pytest

from wakeonlan import create_magic_packet
from wakeonlan import main
from wakeonlan import send_magic_packet


@pytest.mark.parametrize(
    "mac,packet",
    [
        (
            "000000000000",
            b"\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00",
        ),
        (
            "01:23:45:67:89:ab",
            b"\xff\xff\xff\xff\xff\xff"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab"
            b"\x01#Eg\x89\xab",
        ),
        (
            "ff-ff-ff-ff-ff-ff",
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff",
        ),
        (
            "ffff.ffff.ffff",
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff"
            b"\xff\xff\xff\xff\xff\xff",
        ),

    ],
    ids=["no separator", "colons", "hyphens"],
)
def test_create_magic_packet(mac: str, packet: List[int]) -> None:
    """
    Test whether a correct magic packet is created.

    """
    result = create_magic_packet(mac)
    assert result == packet


@patch("socket.socket")
def test_send_magic_packet(sock: Mock) -> None:
    """
    Test whether the magic packets are broadcasted to the specified network.

    """
    send_magic_packet(
        "133713371337", "00-00-00-00-00-00", ip_address="example.com", port=7
    )
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("example.com", 7)),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
        ),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
        ),
        call().__exit__(None, None, None),
    ]


@patch("socket.socket")
def test_send_magic_packet_default(sock: Mock) -> None:
    """
    Test whether the magic packets are broadcasted using default values.

    """
    send_magic_packet("133713371337", "00-00-00-00-00-00")
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("255.255.255.255", 9)),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
        ),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
        ),
        call().__exit__(None, None, None),
    ]


@patch("socket.socket")
def test_send_magic_packet_interface(sock: Mock) -> None:
    """
    Test whether the magic packets are broadcasted to the specified network via specified interface.

    """
    send_magic_packet(
        "133713371337",
        "00-00-00-00-00-00",
        ip_address="example.com",
        port=7,
        interface="192.168.0.2",
    )
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().__enter__(),
        call().__enter__().bind(("192.168.0.2", 0)),
        call().__enter__().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().__enter__().connect(("example.com", 7)),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
            b"\x137\x137\x137"
        ),
        call()
        .__enter__()
        .send(
            b"\xff\xff\xff\xff\xff\xff"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
        ),
        call().__exit__(None, None, None),
    ]


@patch("wakeonlan.send_magic_packet")
def test_main(send_magic_packet: Mock) -> None:
    """
    Test if processed arguments are passed to send_magic_packet.

    """
    main(["00:11:22:33:44:55", "-i", "host.example", "-p", "1337"])
    main(["00:11:22:33:44:55", "-i", "host.example", "-p", "1337", "-n", "192.168.0.2"])
    assert send_magic_packet.mock_calls == [
        call("00:11:22:33:44:55", ip_address="host.example", port=1337, interface=None),
        call(
            "00:11:22:33:44:55",
            ip_address="host.example",
            port=1337,
            interface="192.168.0.2",
        ),
    ]
