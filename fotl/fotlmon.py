"""
fotlmon FOTL monitor
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
from ltl.ltlmon import *
from fotl.fotl import *


class Fotlmon(Ltlmon):
    """
    Fotl monitoring using progression technique
    """
    def prg(self, formula, event, valuation=None):
        if isinstance(formula, Forall):
            return self.prg(ForallConj(), event, valuation)
        else:
            return super().prg(formula, event, valuation)


class ForallConj(UExp):
    """
    Forall Conjunction (internal for monitor)
    """
    symbol = "\u2227"

    def __init__(self, var=None, inner=None):
        super().__init__(inner)
        self.var = [] if var is None else var
        if not isinstance(self.var, list):
            self.var = [self.var]


    def eval(self):
        return self

    def __str__(self):
        return "%s %s (%s)" % (self.symbol, ",".join([str(v) for v in self.var]), self.inner)