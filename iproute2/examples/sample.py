# coding=utf-8
#
# NAME:         .py
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
#   ATM, this particular file is more for me to remind myself how the grammar works, so I don't have to re-learn the
# damn thing again.
#

# coding=utf-8
from iproute2.route import routegrammar


route = """
default via 216.244.91.33 dev eth0
10.64.0.0/16 via 10.65.1.1 dev tun0  metric 101
10.65.0.1 via 10.65.1.1 dev tun0  metric 101
10.65.1.0/25 dev tun0  proto kernel  scope link  src 10.65.1.6
10.65.1.0/24 via 10.65.1.1 dev tun0  metric 101
50.135.108.0/22 dev eth3  proto kernel  scope link  src 50.135.109.113
172.27.224.0/23 dev as0t0  proto kernel  scope link  src 172.27.224.1
172.27.226.0/23 dev as0t1  proto kernel  scope link  src 172.27.226.1
172.27.228.0/23 dev as0t2  proto kernel  scope link  src 172.27.228.1
172.27.230.0/23 dev as0t3  proto kernel  scope link  src 172.27.230.1
172.27.232.0/23 dev as0t4  proto kernel  scope link  src 172.27.232.1
172.27.234.0/23 dev as0t5  proto kernel  scope link  src 172.27.234.1
172.29.20.0/24 dev eth2  proto kernel  scope link  src 172.29.20.1
192.168.100.0/24 dev eth3  proto kernel  scope link  src 192.168.100.100
216.244.91.32/27 via 10.65.1.1 dev tun0  metric 101
216.244.91.34 via 50.135.108.1 dev eth3
"""

routes = []

for line in route.strip().split('\n'):
  tokens = line.split()

  routes.append(routegrammar.ROUTE(tokens, raw_includes_children=True))

print(routes[0]['NODE_SPEC']['PREFIX'])

print(routes[0].via)