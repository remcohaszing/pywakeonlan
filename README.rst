#########
wakeonlan
#########

.. image:: https://img.shields.io/pypi/v/wakeonlan.svg
   :target: https://pypi.org/project/wakeonlan/
   :alt: Pypi version

.. image:: https://img.shields.io/pypi/pyversions/wakeonlan.svg
   :target: https://pypi.org/project/wakeonlan/#files
   :alt: Supported Python versions

.. image:: https://github.com/remcohaszing/pywakeonlan/actions/workflows/ci.yaml/badge.svg
   :target: https://github.com/remcohaszing/pywakeonlan/actions/workflows/ci.yaml
   :alt: Build Status

.. image:: https://readthedocs.org/projects/pywakeonlan/badge/?version=latest
   :target: https://pywakeonlan.readthedocs.io/en/latest
   :alt: Documentation Status

.. image:: https://codecov.io/gh/remcohaszing/pywakeonlan/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/remcohaszing/pywakeonlan
   :alt: Code coverage

A small python module for wake on lan.

For more information on the wake on lan protocol please take a look at
`Wikipedia <http://en.wikipedia.org/wiki/Wake-on-LAN>`_.

************
Installation
************

::

    pip install wakeonlan


*****
Usage
*****

To wake up a computer using wake on lan it must first be enabled in the BIOS
settings. Please note the computer you are trying to power on does not have an
ip address, but it does have a mac address. The package needs to be sent as a
broadcast package.


As a python module
==================

Import the module

>>> from wakeonlan import send_magic_packet


Wake up a single computer by its mac address

>>> send_magic_packet('ff.ff.ff.ff.ff.ff')


Wake up multiple computers by their mac addresses.

>>> send_magic_packet('ff.ff.ff.ff.ff.ff',
...                   '00-00-00-00-00-00',
...                   'FFFFFFFFFFFF')


An external host may be specified. Do note that port forwarding on that host is
required. The default ip address is 255.255.255.255 and the default port is 9.

>>> send_magic_packet('ff.ff.ff.ff.ff.ff',
...                   ip_address='example.com',
...                   port=1337)


A network adapter may be specified. The magic packet will be routed through this interface.

>>> send_magic_packet('ff.ff.ff.ff.ff.ff',
...                   interface='192.168.0.2')


As a standalone script
======================

::

    usage: wakeonlan [-h] [-6] [-i IP] [-p PORT] [-n INTERFACE] mac address [mac address ...]

    Wake one or more computers using the wake on lan protocol.

    positional arguments:
      mac address           The mac addresses of the computers you are trying to wake.

    options:
      -h, --help            show this help message and exit
      -6, --ipv6            To indicate if ipv6 should be used by default instead of ipv4. (default: False)
      -i IP, --ip IP        The ip address of the host to send the magic packet to. (default: 255.255.255.255)
      -p PORT, --port PORT  The port of the host to send the magic packet to. (default: 9)
      -n INTERFACE, --interface INTERFACE
                            The ip address of the network adapter to route the magic packet through. (default: None)


************
Dependencies
************

- Python 3.x


*******
License
*******

`MIT <https://github.com/remcohaszing/pywakeonlan/blob/main/LICENSE.rst>`_ © `Remco Haszing <https://github.com/remcohaszing>`_
