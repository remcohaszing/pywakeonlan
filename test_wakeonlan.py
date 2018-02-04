"""
Tests for wakeonlan.

"""
import socket

import pytest
from mock import call
from mock import patch

from wakeonlan import create_magic_packet
from wakeonlan import main
from wakeonlan import send_magic_packet


@pytest.mark.parametrize('mac,packet', [
    ('000000000000',
     b'\xff\xff\xff\xff\xff\xff'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'
     b'\x00\x00\x00\x00\x00\x00'),
    ('01:23:45:67:89:ab',
     b'\xff\xff\xff\xff\xff\xff'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'
     b'\x01#Eg\x89\xab'),
    ('ff-ff-ff-ff-ff-ff',
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'
     b'\xff\xff\xff\xff\xff\xff'),
], ids=['no separator', 'colons', 'hyphens'])
def test_create_magic_packet(mac, packet):
    """
    Test whether a correct magic packet is created.

    """
    result = create_magic_packet(mac)
    assert result == packet


@patch('socket.socket')
def test_send_magic_packet(sock):
    """
    Test whether the magic packets are broadcasted to the specified network.

    """
    send_magic_packet(
        '133713371337', '00-00-00-00-00-00', ip_address='example.com', port=7)
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().connect(('example.com', 7)),
        call().send(
            b'\xff\xff\xff\xff\xff\xff'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'),
        call().send(
            b'\xff\xff\xff\xff\xff\xff'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'),
        call().close(),
    ]


@patch('socket.socket')
def test_send_magic_packet_default(sock):
    """
    Test whether the magic packets are broadcasted using default values.

    """
    send_magic_packet('133713371337', '00-00-00-00-00-00')
    assert sock.mock_calls == [
        call(socket.AF_INET, socket.SOCK_DGRAM),
        call().setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
        call().connect(('255.255.255.255', 9)),
        call().send(
            b'\xff\xff\xff\xff\xff\xff'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'
            b'\x137\x137\x137'),
        call().send(
            b'\xff\xff\xff\xff\xff\xff'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00'),
        call().close(),
    ]


@patch('wakeonlan.send_magic_packet')
def test_main(send_magic_packet):
    """
    Test if processed arguments are passed to send_magic_packet.

    """
    main(['00:11:22:33:44:55', '-i', 'host.example', '-p', '1337'])
    assert send_magic_packet.mock_calls == [call(
        '00:11:22:33:44:55',
        ip_address='host.example',
        port=1337,
    )]
