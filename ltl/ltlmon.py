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

DEBUG = False


def Debug(*args):
    if DEBUG:
        print(*args)


class Mon:
    """
    Abstract monitor
    """
    AP = []

    def __init__(self, formula, trace):
        self.formula = formula
        self.trace = trace
        self.counter = 0

    def monitor(self, *args, **kargs):
        pass

    def prg(self, *args, **kargs):
        pass

    def push_event(self, event):
        self.trace.push_event(event)


class Ltlmon(Mon):
    """
    LTL monitor using progression technique
    """

    def monitor(self):
        # counter = 0
        b3 = Boolean3.Unknown
        res = self.formula
        for e in self.trace.events[self.counter:]:
            self.counter += 1
            res = self.prg(res, e)
            Debug(res)
            b3 = B3(res.eval()) if isinstance(res, Formula) else res
            if b3 == Boolean3.Top or b3 == Boolean3.Bottom: break
        ret = "Result Progression: %s after %s events." % (b3, self.counter)
        # print(ret)
        return ret

    def prg(self, formula, trace):
        # print(formula)
        if isinstance(formula, Predicate):
            # Todo : Check if Predicate is in AP
            res = true() if trace.contains(formula) else false()

        elif isinstance(formula, true):
            res = true()

        elif isinstance(formula, false):
            res = false()

        elif isinstance(formula, Neg):
            res = Neg(self.prg(formula.inner, trace)).eval()

        elif isinstance(formula, Or):
            res = Or(self.prg(formula.left, trace), self.prg(formula.right, trace)).eval()

        elif isinstance(formula, And):
            res = And(self.prg(formula.left, trace), self.prg(formula.right, trace)).eval()

        elif isinstance(formula, Always):
            res = And(self.prg(formula.inner, trace), G(formula.inner)).eval()

        elif isinstance(formula, Future):
            res = Or(self.prg(formula.inner, trace), F(formula.inner)).eval()

        elif isinstance(formula, Until):
            res = Or(self.prg(formula.right, trace),
                     And(self.prg(formula.left, trace), U(formula.left, formula.right)).eval()).eval()

        elif isinstance(formula, Release):
            res = Or(self.prg(formula.left, trace),
                     And(self.prg(formula.right, trace), R(formula.left, formula.right)).eval()).eval()

        elif isinstance(formula, Next):
            res = formula.inner#.eval()  # TODO check

        else:
            print("Error " + str(formula))
            return None

        return res
