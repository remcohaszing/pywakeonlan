"""
Tests for wakeonlan.

"""

import socket
import unittest
from unittest import mock

from wakeonlan import create_magic_packet, main, send_magic_packet


class TestCreateMagicPacket(unittest.TestCase):
    """
    Test :ref:`create_magic_packet`.

    """

    def test_no_separators(self) -> None:
        """
        Test without separators.

        """
        result = create_magic_packet('000000000000')
        self.assertEqual(
            result,
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
            b'\x00\x00\x00\x00\x00\x00',
        )

    def test_colon(self) -> None:
        """
        Test with a colon as separator.

        """
        result = create_magic_packet('01:23:45:67:89:ab')
        self.assertEqual(
            result,
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
            b'\x01#Eg\x89\xab',
        )

    def test_hyphen(self) -> None:
        """
        Test with a hyphen as separator.

        """
        result = create_magic_packet('ff-ff-ff-ff-ff-ff')
        self.assertEqual(
            result,
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
            b'\xff\xff\xff\xff\xff\xff',
        )

    def test_dot(self) -> None:
        """
        Test with a dot as separator.

        """
        result = create_magic_packet('ffff.ffff.ffff')
        self.assertEqual(
            result,
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
            b'\xff\xff\xff\xff\xff\xff',
        )

    def test_invalid_mac(self) -> None:
        """
        Test an invalid mac address.

        """
        with self.assertRaises(ValueError, msg='Incorrect MAC address format'):
            create_magic_packet('invalid')

    def test_mac_secureon_no_separators(self) -> None:
        """
        Test with an additional SecureON password without separators.

        """
        result = create_magic_packet('01:23:45:67:89:ab/ffffffffffff')
        self.assertEqual(
            result,
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
            b'\x01#Eg\x89\xab'
            b'\xff\xff\xff\xff\xff\xff',
        )

    def test_mac_secureon_colon(self) -> None:
        """
        Test with an additional SecureON password with colons as separators.

        """
        result = create_magic_packet('01:23:45:67:89:ab/ff:ff:ff:ff:ff:ff')
        self.assertEqual(
            result,
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
            b'\x01#Eg\x89\xab'
            b'\xff\xff\xff\xff\xff\xff',
        )

    def test_mac_secureon_hyphen(self) -> None:
        """
        Test with an additional SecureON password with hyphens as separators.

        """
        result = create_magic_packet('01:23:45:67:89:ab/ff-ff-ff-ff-ff-ff')
        self.assertEqual(
            result,
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
            b'\x01#Eg\x89\xab'
            b'\xff\xff\xff\xff\xff\xff',
        )

    def test_mac_secureon_dot(self) -> None:
        """
        Test with an additional SecureON password with dots as separators.

        """
        result = create_magic_packet('01:23:45:67:89:ab/ffff.ffff.ffff')
        self.assertEqual(
            result,
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
            b'\x01#Eg\x89\xab'
            b'\xff\xff\xff\xff\xff\xff',
        )

    def test_invalid_secureon(self) -> None:
        """
        Test an invalid SecureON password.

        """
        with self.assertRaises(ValueError, msg='Incorrect SecureOn password format'):
            create_magic_packet('01:23:45:67:89:ab/invalid')


class TestSendMagicPacket(unittest.TestCase):
    """
    Test :ref:`send_magic_packet`.

    """

    def test_specific_network(self) -> None:
        """
        Test whether the magic packets are broadcasted to the specified network.

        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('127.0.0.255', 1234))
            send_magic_packet(
                '133713371337', '00-00-00-00-00-00', ip_address='127.0.0.255', port=1234
            )
            data, addr = sock.recvfrom(1024)
            self.assertEqual(addr[0], '127.0.0.1')
            self.assertEqual(
                data,
                b'\xff\xff\xff\xff\xff\xff'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37',
            )

    def test_default_network(self) -> None:
        """
        Test whether the magic packets are broadcasted using default values.

        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 1234))
            send_magic_packet('133713371337', port=1234)
            data, addr = sock.recvfrom(1024)
            self.assertEqual(addr[0], socket.gethostbyname(socket.gethostname()))
            self.assertEqual(
                data,
                b'\xff\xff\xff\xff\xff\xff'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37',
            )

    def test_multiple_packets(self) -> None:
        """
        Test whether multiple packets can be sent.

        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 1234))
            send_magic_packet('133713371337', '000000000000', port=1234)
            data = sock.recv(1024)
            self.assertEqual(
                data,
                b'\xff\xff\xff\xff\xff\xff'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37',
            )
            data = sock.recv(1024)
            self.assertEqual(
                data,
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
                b'\x00\x00\x00\x00\x00\x00',
            )

    def test_send_magic_packet_interface(self) -> None:
        """
        Test whether the magic packets are broadcasted to the specified network via specified interface.

        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('<broadcast>', 1234))
            send_magic_packet(
                '133713371337',
                interface='127.0.0.1',
                port=1234,
            )
            data, addr = sock.recvfrom(1024)
            self.assertEqual(addr[0], '127.0.0.1')
            self.assertEqual(
                data,
                b'\xff\xff\xff\xff\xff\xff'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37',
            )

    def test_send_with_explicit_ipv6_address(self) -> None:
        """
        Test whether the given address family is used instead automatically it automatically.
        """
        with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 1234))
            send_magic_packet(
                '133713371337',
                ip_address='localhost',
                port=1234,
                address_family=socket.AF_INET6,
            )
            data, addr = sock.recvfrom(1024)
            self.assertEqual(addr[0], '::1')
            self.assertEqual(
                data,
                b'\xff\xff\xff\xff\xff\xff'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37'
                b'\x13\x37\x13\x37\x13\x37',
            )

    def test_send_magic_packet_secureon(self) -> None:
        """
        Test whether the magic packets are broadcasted using default values with a SecureOn password.

        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 1234))
            send_magic_packet(
                '01:23:45:67:89:ab/00:00:00:00:00:00',
                port=1234,
            )
            data, addr = sock.recvfrom(1024)
            self.assertEqual(addr[0], socket.gethostbyname(socket.gethostname()))
            self.assertEqual(
                data,
                b'\xff\xff\xff\xff\xff\xff'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x01\x23\x45\x67\x89\xab'
                b'\x00\x00\x00\x00\x00\x00',
            )


class TestMain(unittest.TestCase):
    """
    Test :ref:`main`.

    """

    @mock.patch('wakeonlan.send_magic_packet')
    def test_main(self, send_magic_packet: mock.Mock) -> None:
        """
        Test if processed arguments are passed to send_magic_packet.

        """
        main(['00:11:22:33:44:55', '-i', 'host.example', '-p', '1337'])
        main(
            [
                '00:11:22:33:44:55',
                '-i',
                'host.example',
                '-p',
                '1337',
                '-n',
                '192.168.0.2',
            ]
        )
        main(['00:11:22:33:44:55', '-i', 'host.example', '-p', '1337', '-6'])
        self.assertEqual(
            send_magic_packet.mock_calls,
            [
                mock.call(
                    '00:11:22:33:44:55',
                    ip_address='host.example',
                    port=1337,
                    interface=None,
                    address_family=None,
                ),
                mock.call(
                    '00:11:22:33:44:55',
                    ip_address='host.example',
                    port=1337,
                    interface='192.168.0.2',
                    address_family=None,
                ),
                mock.call(
                    '00:11:22:33:44:55',
                    ip_address='host.example',
                    port=1337,
                    interface=None,
                    address_family=socket.AF_INET6,
                ),
            ],
        )


if __name__ == '__main__':
    unittest.main()
