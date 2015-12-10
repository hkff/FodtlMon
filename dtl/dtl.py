"""
dtl
Copyright (C) 2015 Walid Benghabrit

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = 'hkff'
from ltl.ltl import *


class At(UExp):
    """
    Localisation operator
    """
    symbol = "@"

    def __init__(self, agent, inner):
        super().__init__(inner)
        self.agent = agent

    def toTSPASS(self):
        raise Exception("Not compatible with TSPASS !")

    def toLTLFO(self):
        raise Exception("Not compatible with TSPASS !")

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return "%s(%s,%s)" % (self.__class__.__name__, self.agent, self.inner.toCODE())

    def eval(self):
        return self

    def __str__(self):
        return "@_{%s}(%s)" % (self.agent, self.inner)
