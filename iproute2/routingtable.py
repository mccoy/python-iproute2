#
# $Id: routingtable.py 9 2012-06-05 04:56:36Z nickw $
#
# NAME:         routingtable.py
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
#   Defines a routing table.
#

from iproute2.utils import cmd
from iproute2.route import routegrammar


# Exceptions
class RoutingTableError(Exception):
    pass
class InvalidRouteError(RoutingTableError):
    pass


# RoutingTable
class RoutingTable(object):
    """
    Defines a routing table.

    """
    def __init__(self, table_txt=None, description=None):
        """
        Constructor

        """
        self.tokenized_table = self.tokenize_table(table_txt) if table_txt else None
        self.description = description
        self.table = None
        self.table_no_cidr = None
    #---


    def __str__(self):
        """
        Converts table to a string that looks like the standard iproute2 output.

        :returns: str
        """
        if not self.tokenized_table:
            return None

        table = (' '.join(route) for route in self.tokenized_table)
        text_table = '\n'.join(table)

        return text_table
    #---


    def __getitem__(self, item):
        """
        Getter for dictionary style operation.  Operates off routes as keys.

        :param item: String

        :returns: route.routegrammar.ROUTE object
        """
        # 'Default' needs to be switched to a proper netaddr
        if item == 'default':
            item = '0.0.0.0/0'

        try:
            return self.__dict__[item]
        # If the item doesn't exist, see if it matches a prefix
        except KeyError:
            if item in self.table:
                return self.table[item]
            elif item in self.table_no_cidr:
                return self.table_no_cidr[item]
            else:
                raise
    #---


    @staticmethod
    def tokenize_table(table_txt):
        """
        Simply tokenizes the output of 'ip route'

        :param table_txt: Text output from 'ip route'
        :type table_txt: str

        :returns: list of lists - list of tokenized routing lines

        """
        output_tokens = table_txt.strip().split('\n')
        table = [token.split() for token in output_tokens]

        return table
    #---

    def load(self, table_txt=None):
        """
        Loads a routing table from the provided text.  If text is not provided then the system routing table is loaded.

        :param table_txt: Text output from 'ip route'
        :type table_txt: str

        """
        if not table_txt:
            table_txt = cmd.route()

        self.tokenized_table = self.tokenize_table(table_txt)
        self.parse()
    #---


    def parse(self):
        """
        Uses the routing grammar to parse the tokens into route objects.

        """
        route_objs = (routegrammar.ROUTE(route) for route in self.tokenized_table)
        self.table = {str(route_obj.PREFIX):route_obj for route_obj in route_objs}
        self.table_no_cidr = {key.split('/')[0]:value for key, value in self.table.iteritems()}

    #---

#---
