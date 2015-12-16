"""
fotl
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


#############################
# FO Operators
#############################
class Forall(UExp):
    """
    Forall operator
    """
    symbol = "\u2200"

    def __init__(self, var=None, inner=None):
        super().__init__(inner)
        self.var = [] if var is None else var
        if not isinstance(self.var, list):
            self.var = [self.var]

    def toTSPASS(self):
        return "![%s](%s)" % (",".join([v.toTSPASS() for v in self.var]), self.inner.toTSPASS())

    def toLTLFO(self):
        return "A(%s)(%s)" % (",".join([v.toLTLFO() for v in self.var]), self.inner.toLTLFO())

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return "%s(%s,%s)" % (self.__class__.__name__, self.var, self.inner.toCODE())

    def eval(self):
        return self

    def __str__(self):
        return "%s %s (%s)" % (self.symbol, ",".join([str(v) for v in self.var]), self.inner)


class Exists(Neg, Forall):
    """
    Exsits operator
    """
    symbol = "\u2203"

    def __init__(self, var=None, inner=None):
        Neg.__init__(self, inner=Forall(var=var, inner=Neg(inner)))
        Forall.__init__(self, var=var, inner=inner)

    def __str__(self):
        return Forall.__str__(self)

    def toTSPASS(self):
        return "?[%s](%s)" % (",".join([v.toTSPASS() for v in self.var]), self.inner.toTSPASS())

    def toLTLFO(self):
        return "E(%s)(%s)" % (",".join([v.toLTLFO() for v in self.var]), self.inner.toLTLFO())
