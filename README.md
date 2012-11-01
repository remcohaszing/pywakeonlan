pywakeonlan
===========

A small python module for wake on lan.  
It has been tested both locally and externally using Python 2.7.3 and
Python 3.2.3  

The project is hosted on https://github.com/Trollhammaren/pywakeonlan  

This module is licensed under the WTFPL

Usage
-----

    wakeonlan.py [-i ip_address] [-p port] mac_address

        -h              Show this help message.

        -i ip address   The broadcast ip address the magic packet should be
                        sent to.

        -p port         The port to which the package should be sent.

        mac_address     The mac address or hardware address of the computer
                        you are trying to wake.

Dependencies
------------
- Python2.x or Python3.x

