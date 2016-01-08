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
__author__ = 'walid'
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
        self.var = var

    def toTSPASS(self):
        return "![%s](%s)" % (self.var.toTSPASS(), self.inner.toTSPASS())

    def toLTLFO(self):
        return "A %s. (%s)" % (self.var.toLTLFO(), self.inner.toLTLFO())

    def prefix_print(self):
        return str(self)

    def toCODE(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.var.toCODE(), self.inner.toCODE())

    def eval(self):
        return self

    def __str__(self):
        return "%s %s (%s)" % (self.symbol, str(self.var), self.inner)


class Exists(Neg):
    """
    Exsits operator
    """
    symbol = "\u2203"

    def __init__(self, var=None, inner=None):
        self.var = var
        self.inner2 = inner
        super().__init__(inner=Forall(var=var, inner=Neg(inner)))

    def __str__(self):
        return "%s %s (%s)" % (self.symbol, str(self.var), self.inner2)

    def prefix_print(self):
        return "(%s %s %s)" % (self.symbol, self.var, self.inner2.prefix_print())

    def toCODE(self):
        return "%s(%s, %s)" % (self.__class__.__name__, self.var.toCODE(), self.inner2.toCODE())

    def toTSPASS(self):
        return "?[%s](%s)" % (self.var.toTSPASS(), self.inner2.toTSPASS())

    def toLTLFO(self):
        return "E %s. (%s)" % (self.var.toLTLFO(), self.inner2.toLTLFO())


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
