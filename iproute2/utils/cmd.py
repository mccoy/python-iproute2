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

class IPCommandError(Exception): pass

def ip(command, path_to_ip='/sbin/ip'):
    """
    Runs iproute2 on the command-line.

    """
    ip_cmd = "%s %s" % (path_to_ip,command)
    proc = subprocess.Popen(ip_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = proc.communicate()
    return_code = subprocess.Popen.poll(proc)

    return {'stdout': stdout, 'stderr': stderr, 'return_code': return_code}


def route(params = ''):
    """
    Fetches the routing table

    """
    route_info = ip('route %s' % params)

    if route_info['stderr'] or route_info['return_code']:
        raise IPCommandError(route_info['stderr'])

    return route_info['stdout']