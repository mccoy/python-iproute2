# coding=utf-8
#
# NAME:         cmd.py
#
# AUTHOR:       Nick Whalen <nickw@mindstorm-networks.net>
# COPYRIGHT:    2014 by Nick Whalen
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
#   Interface to iproute2 via the command-line
#

import subprocess

class IPCommandError(Exception):
    def __init__(self, message, code):
        super(IPCommandError, self).__init__(message)
        self.code = code


def ip(ip_args, path_to_ip='/sbin/ip'):
    """
    Runs iproute2 on the command-line.

    """
    ip_cmd = '{} {}'.format(path_to_ip, ip_args)

    try:
        return subprocess.check_output(ip_cmd, shell=False)
    except subprocess.CalledProcessError as e:
        raise IPCommandError(e.message, e.returncode)


def route(params = ''):
    """
    Fetches the routing table

    """
    return ip('route {}'.format(params))
