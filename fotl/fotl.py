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
        # self.var = [] if var is None else var
        # if not isinstance(self.var, list):
        #     self.var = [self.var]
        self.var = var

    def toTSPASS(self):
        # return "![%s](%s)" % (",".join([v.toTSPASS() for v in self.var]), self.inner.toTSPASS())
        return "![%s](%s)" % (self.var.toTSPASS(), self.inner.toTSPASS())

    def toLTLFO(self):
        # return "A %s. (%s)" % (",".join([v.toLTLFO() for v in self.var]), self.inner.toLTLFO())
        return "A %s. (%s)" % (self.var.toLTLFO(), self.inner.toLTLFO())

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        # return "%s([%s], %s)" % (self.__class__.__name__, ",".join([v.toCODE() for v in self.var]), self.inner.toCODE())
        return "%s(%s, %s)" % (self.__class__.__name__, self.var.toCODE(), self.inner.toCODE())

    def eval(self):
        return self

    def __str__(self):
        # return "%s %s (%s)" % (self.symbol, ",".join([str(v) for v in self.var]), self.inner)
        return "%s %s (%s)" % (self.symbol, str(self.var), self.inner)


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
        # return "?[%s](%s)" % (",".join([v.toTSPASS() for v in self.var]), self.inner.toTSPASS())
        return "?[%s](%s)" % (self.var.toTSPASS(), self.inner.toTSPASS())

    def toLTLFO(self):
        # return "E %s. (%s)" % (",".join([v.toLTLFO() for v in self.var]), self.inner.toLTLFO())
        return "E %s. (%s)" % (self.var.toLTLFO(), self.inner.toLTLFO())


class VarDec(Exp):
    """
    Variable declaration
    """
    def __init__(self, name="", vtype=""):
        self.name = name
        self.vtype = vtype

    def toTSPASS(self):
        return "%s:%s" % (self.name, self.vtype)

    def toLTLFO(self):
        return "%s:%s" % (self.name, self.vtype)

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return "%s('%s', '%s')" % (self.__class__.__name__, self.name, self.vtype)

    def eval(self):
        return self

    def __str__(self):
        return "%s:%s" % (self.name, self.vtype)

VD = VarDec


class Valuation:
    """
    Valuation links between value and var name
    """
    def __init__(self, value=None, var=None):
        self.value = value
        self.var = var

    def __str__(self):
        return "%s<-%s" % (self.value, self.var)
