wakeonlan
=========

A small python module for wake on lan. It has been tested both locally and
externally using Python 2.7.3 and Python 3.2.3.

The project is hosted on GitHub_. For more information on the wake on lan
protocol please take a look at Wikipedia_.

Usage
-----

To wake up a computer using wake on lan it must first be enabled in the BIOS
settings. Please note the computer you are trying to power on does not have an
ip address, but it does have a mac address. The package needs to be sent as a
broadcast package.

As a python module
------------------

- Import the module

>>> from wakeonlan import wol


- Wake up a single computer by its mac address

>>> wol.send_magic_packet('ff.ff.ff.ff.ff.ff')


- Wake up multiple computers by their mac addresses.

>>> wol.send_magic_packet('ff.ff.ff.ff.ff.ff', '00-00-00-00-00-00',
...                       'FFFFFFFFFFFF')


- An external host may be specified. Do note that port forwarding on that host
  is required. The default ip address is 255.255.255.255 and the default port
  is 9.

>>> wol.send_magic_packet('ff.ff.ff.ff.ff.ff',
...                       ip_address='example.com',
...                       port=1337)


As a standalone script
----------------------

::

    usage: wol [-h] [-i ip] [-p port] mac addresses [mac addresses ...]

    Wake one or more computers using the wake on lan protocol

    positional arguments:
      mac addresses  The mac addresses or of the computers you are trying to wake.

    optional arguments:
      -h, --help     show this help message and exit
      -i ip          The ip address of the host to send the magic packet to.
                     (default 255.255.255.255)
      -p port        The port of the host to send the magic packet to (default 9)


Dependencies
------------

- Python2.x or Python3.x


Licence
-------

WTFPL


.. _GitHub: https://github.com/remcohaszing/pywakeonlan
.. _Wikipedia: http://en.wikipedia.org/wiki/Wake-on-LAN
