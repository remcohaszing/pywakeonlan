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

    def test_invalid(self) -> None:
        """
        Test an invalid mac address.

        """
        with self.assertRaises(ValueError):
            create_magic_packet('invalid')


class TestSendMagicPacket(unittest.TestCase):
    """
    Test :ref:`send_magic_packet`.

    """

    @mock.patch('socket.socket')
    def test_send_magic_packet(self, sock: mock.Mock) -> None:
        """
        Test whether the magic packets are broadcasted to the specified network.

        """
        send_magic_packet(
            '133713371337', '00-00-00-00-00-00', ip_address='example.com', port=7
        )
        self.assertEqual(
            sock.mock_calls,
            [
                mock.call(socket.AF_INET, socket.SOCK_DGRAM),
                mock.call().__enter__(),
                mock.call()
                .__enter__()
                .setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
                mock.call().__enter__().connect(('example.com', 7)),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x137\x137\x137'
                ),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x00\x00\x00\x00\x00\x00'
                ),
                mock.call().__exit__(None, None, None),
            ],
        )

    @mock.patch('socket.socket')
    def test_send_magic_packet_default(self, sock: mock.Mock) -> None:
        """
        Test whether the magic packets are broadcasted using default values.

        """
        send_magic_packet('133713371337', '00-00-00-00-00-00')
        self.assertEqual(
            sock.mock_calls,
            [
                mock.call(socket.AF_INET, socket.SOCK_DGRAM),
                mock.call().__enter__(),
                mock.call()
                .__enter__()
                .setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
                mock.call().__enter__().connect(('255.255.255.255', 9)),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x137\x137\x137'
                ),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x00\x00\x00\x00\x00\x00'
                ),
                mock.call().__exit__(None, None, None),
            ],
        )

    @mock.patch('socket.socket')
    def test_send_magic_packet_interface(self, sock: mock.Mock) -> None:
        """
        Test whether the magic packets are broadcasted to the specified network via specified interface.

        """
        send_magic_packet(
            '133713371337',
            '00-00-00-00-00-00',
            ip_address='example.com',
            port=7,
            interface='192.168.0.2',
        )
        self.assertEqual(
            sock.mock_calls,
            [
                mock.call(socket.AF_INET, socket.SOCK_DGRAM),
                mock.call().__enter__(),
                mock.call().__enter__().bind(('192.168.0.2', 0)),
                mock.call()
                .__enter__()
                .setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
                mock.call().__enter__().connect(('example.com', 7)),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x137\x137\x137'
                ),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x00\x00\x00\x00\x00\x00'
                ),
                mock.call().__exit__(None, None, None),
            ],
        )

    @mock.patch('socket.socket')
    def test_send_correct_af_chosen_with_ipv6_address(self, sock: mock.Mock) -> None:
        """
        Test whether AF_INET6 automatically chosen when the `address_family` argument is not given.
        """
        send_magic_packet(
            '133713371337',
            '00-00-00-00-00-00',
            ip_address='fc00::',
            port=7,
        )
        self.assertEqual(
            sock.mock_calls,
            [
                mock.call(socket.AF_INET6, socket.SOCK_DGRAM),
                mock.call().__enter__(),
                mock.call()
                .__enter__()
                .setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
                mock.call().__enter__().connect(('fc00::', 7)),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x137\x137\x137'
                ),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x00\x00\x00\x00\x00\x00'
                ),
                mock.call().__exit__(None, None, None),
            ],
        )

    @mock.patch('socket.socket')
    def test_send_with_explicit_ipv6_address(self, sock: mock.Mock) -> None:
        """
        Test whether the given address family is used instead automatically it automatically.
        """
        send_magic_packet(
            '133713371337',
            '00-00-00-00-00-00',
            ip_address='example.com',
            port=7,
            address_family=socket.AF_INET6,
        )
        self.assertEqual(
            sock.mock_calls,
            [
                mock.call(socket.AF_INET6, socket.SOCK_DGRAM),
                mock.call().__enter__(),
                mock.call()
                .__enter__()
                .setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1),
                mock.call().__enter__().connect(('example.com', 7)),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x137\x137\x137'
                ),
                mock.call()
                .__enter__()
                .send(
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
                    b'\x00\x00\x00\x00\x00\x00'
                ),
                mock.call().__exit__(None, None, None),
            ],
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
