===============
python-iproute2
===============

iproute2 helper library for Python.

More description to come as I develop this thing.

===============
Dependencies
===============
:`cidrize <http://pypi.python.org/pypi/cidrize/>`_: Parses IPv4/IPv6 addresses, CIDRs, ranges, and wildcard matches & attempts return a valid list of IP addresses


===============
Examples
===============
These are just some basic examples of what you can do with the routingtable module (currently the only one that's
ready for public consumption).

.. raw:: python

route = """
default via 172.16.0.1 dev eth0  metric 100
172.16.0.0/24 dev eth0  proto kernel  scope link  src 172.16.0.200
172.32.0.0/16 proto static via 172.33.1.1 dev as0t1
"""

from iproute2 import routingtable

table = routingtable.RoutingTable()
# NOTE: load() with no arguments will load the machine's routing table, provided you're running on Linux
table.load(route)

# Now for some quick examples. Note that keywords like 'proto', 'static', 'dev', etc may be used directly off a ROUTE
# object (the RoutingTable object returns ROUTE objects when you use it like a dictionary). The backend objects are
# structured exactly like the iproute2 grammar (see 'ip route help'), including the case.  As a result you can do
# something like this (though I wouldn't recommend it, it's rather ugly):
print(table['172.29.0.0/16']['NODE_SPEC'].proto)
# or this:
print(table['172.29.0.0/16']['INFO_SPEC']['NH'].via)
# It's far easier to let the library do the heavy lifting for you, and use the keywords off the main ROUTE object
# (as shown below).


# Fetch a route via it's network (CIDR-less)
# Currently this only works in small networks.  If you have multiple networks defined as 172.29.0.0/xx the library will
# return the first one it encounters.  This should be fixed in a coming release.
print(table['172.29.0.0'])

# Fetch a route via it's network (with CIDR)
print(table['172.29.0.0/16'])

# Determine how a route is routed
print(table['default'].via)
print(table['default'].dev)

# Note that the default route may also be entered as it's netaddr format 0.0.0.0/0
print(table['0.0.0.0/0'].via)

# Find the protocol of a route
print(table['172.32.0.0/16'].dev)

# Scope
print(table['172.16.0.0/24'].scope)


===============
License
===============
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.