#
# $Id: interface.py 6 2012-05-28 18:43:14Z nickw $
#
# NAME:         interface.py
#
# AUTHOR:       Nick Whalen <nickw@mindstorm-networks.net>
# COPYRIGHT:    2012 by Nick Whalen
# LICENSE:
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# DESCRIPTION:
#   Defines a network interface and methods to work with it.  Currently
#   only works on Linux; Windows functionality is planned.
#

from __future__ import print_function

import logging
from utils import cmd

IP_V4 = 4
IP_V6 = 6

INT_GBPS = 0x4
INT_MBPS = 0x3
INT_KBPS = 0x2
INT_BPS = 0x1


# Exceptions
class InterfaceError(Exception):
    pass
class ConfigError(InterfaceError):
    """Raised when there is a problem with the config dictionary."""
    pass
class RequiresEscalationError(InterfaceError):
    pass
class AddressError(InterfaceError):
    pass


# Interface Class
class Interface(object):
    """
    Defines a network interface.
    """
    name = None             # Interface name as per the OS
    display_name = None
    units = INT_MBPS
    bandwidth_in = 0
    bandwidth_out = 0
    addresses = {'v4':[], 'v6':[], 'mac': None}


    def __init__(self, name):
        """
        Constructor
        """
        try:
            cmd.ip('link show "{}"'.format(name))
        except cmd.IPCommandError as err:
            if err.code == 255:
                raise InterfaceError('Invalid interface name: {}'.format(name))
            else:
                errmsg = 'Unexpected error ({}): {}'.format(err.code, err.message)
                logging.error(errmsg)
                raise InterfaceError(errmsg)
        else:
            self.name = name


    def getAddresses(self):
        """
        Fetches the interface's addresses (and caches them locally).

        :return: Dictionary of interface's v4 and v6 addresses.
        """
        v4 = []
        v6 = []
        ip_cmd_output = cmd.ip('address show dev "{}"'.format(self.name))
        for cmd_line in ip_cmd_output:
            split_line = cmd_line.decode('utf-8').strip().split()

            # MAC address
            if split_line[0] == 'link/ether':
                self.addresses['mac'] = split_line[1]
            # IPv4 address
            elif split_line[0] == 'inet':
                v4.append(tuple(split_line[1].split('/')))
            # IPv6 address
            elif split_line[0] == 'inet6':
                v6.append(tuple(split_line[1].split('/')))

        self.addresses['v4'] = v4
        self.addresses['v6'] = v6

        return self.addresses
    #---


    def addAddress(self, address):
        """
        Adds an IP address to an interface.

        :param address: String containing IP address and subnet in CIDR notation.
        """
        try:
            cmd.ip('address add "{}" dev "{}"'.format(address, self.name))
        except cmd.IPCommandError as err:
            if err.code == 254:
                raise AddressError("{} already exists on {}".format(address, self.name))
            else:
                raise InterfaceError("Unexpected error ({}): {}".format(err.code, err.message))
        else:
            self.getAddresses()     # Update the IP address cache
    #---


    def delAddress(self, address):
        """
        Removes an IP address from an interface.

        :param address: String containing IP address and subnet in CIDR notation.
        """
        try:
            cmd.cmd.ip('address del "{}" dev "{}"'.format(address, self.name))
        except cmd.IPCommmandError as err:
            if err.code == 254:
                raise AddressError('{} does not exist on {}'.format(address, self.name))
            else:
                raise InterfaceError('Unexpected error ({}): {}'.format(err.code, err.message))
        self.getAddresses()     # Update the IP address cache


    def up(self):
        """
        Brings the interface up.
        """
        try:
            cmd.ip_cmd('link set "{}" up'.format(self.name))
        except cmd.IPCommandError as err:
            if err.code == 2:
                errmsg = 'Altering interface state requires escalated privileges.'
                raise RequiresEscalationError(errmsg)
            else:
                raise InterfaceError('Unexpected error: {}'.format(err.message))


    def down(self):
        """
        Disables the interface.
        """
        try:
            cmd.ip_cmd('link set "{}" down'.format(self.name))
        except cmd.IPCommandError as err:
            if err.code == 2:
                errmsg = 'Altering interface state requires escalated privileges.'
                raise RequiresEscalationError(errmsg)
            else:
                raise InterfaceError('Unexpected error: {}'.format(err.message))


    def status(self, simple=False):
        """
        Fetches the status of the interface, according to iproute.

        :param simple: Return only the status, no additional information if ``True``.
        :return: Simple status string if param:simple is ``True``, otherwise,
                 full iproute status string.
        """
        try:
            iproute = cmd.ip('show "{}"'.format(self.name))
        except cmd.IPCommandError as err:
            raise InterfaceError("Unexpected error ({}): {}".format(err.code, err.message))

        if simple:
            return iproute.split('state')[1].split()[0]
        else:
            return iproute
    #---
