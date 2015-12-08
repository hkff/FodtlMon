"""
ltlmon LTL monitor
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
from ltl.ltl import *


class Mon:
    """
    Abstract monitor
    """
    AP = []


class Ltlmon(Mon):
    """
    LTL monitor using progression technique
    """

    def monitor(self, formula, trace, reduction=False):
        counter = 0
        b3 = Boolean3.Unknown
        res = Boolean3.Unknown
        for e in trace.events:
            counter += 1
            res = self.prg(formula, e, red=reduction)
            b3 = B3(res.eval())
            if b3 == Boolean3.Top or b3 == Boolean3.Bottom: break
        print("%s after %s events" % (b3, counter))
        return res.eval()

    def prg(self, formula, trace, red=False):
        # print(formula)
        if isinstance(formula, Predicate):
            # Todo : Check if Predicate is in AP
            res = true() if trace.contains(formula) else false()

        elif isinstance(formula, true):
            res = true()

        elif isinstance(formula, false):
            res = false()

        elif isinstance(formula, Neg):
            res = Neg(self.prg(formula.inner, trace, red=red))

        elif isinstance(formula, Or):
            res = Or(self.prg(formula.left, trace, red=red), self.prg(formula.right, trace, red=red))

        elif isinstance(formula, And):
            res = And(self.prg(formula.left, trace, red=red), self.prg(formula.right, trace, red=red))

        elif isinstance(formula, Always):
            res = And(self.prg(formula.inner, trace, red=red), G(formula.inner))

        elif isinstance(formula, Future):
            res = Or(self.prg(formula.inner, trace, red=red), F(formula.inner))

        elif isinstance(formula, Until):
            res = Or(self.prg(formula.right, trace, red=red),
                     And(self.prg(formula.left, trace, red=red), U(formula.left, formula.right)))

        elif isinstance(formula, Release):
            res = Or(self.prg(formula.left, trace, red=red),
                     And(self.prg(formula.right, trace, red=red), R(formula.left, formula.right)))

        elif isinstance(formula, Next):
            res = formula.inner

        else:
            print("Error " + str(formula))
            return None

        if res is not None:
            return res.eval() if red else res
