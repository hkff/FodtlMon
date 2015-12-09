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

DEBUG = True


def debug(*args):
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

    def monitor(self, *args, **kargs):
        pass

    def prg(self, *args, **kargs):
        pass


class Ltlmon(Mon):
    """
    LTL monitor using progression technique
    """

    def monitor(self, reduction=False):
        counter = 0
        b3 = Boolean3.Unknown
        res = self.formula
        for e in self.trace.events:
            counter += 1
            res = self.prg(res, e, red=reduction)
            debug(res)
            b3 = B3(res.eval())
            if b3 == Boolean3.Top or b3 == Boolean3.Bottom: break
        ret = "Result Progression: %s after %s events." % (b3, counter)
        print(ret)
        return ret

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


class runtime_monitor(Ltlmon):

    def __init__(self, formula, trace):
        super().__init__(formula, trace)
        self.previous = []
        self.counter = 0

    def monitor(self, reduction=False):
        #      for e in self.trace.events[self.counter:]:
        #     self.formula = res
        #    return res
        b3 = Boolean3.Unknown
        res = Boolean3.Unknown
        for e in self.trace.events[self.counter:]:
            self.counter += 1
            res = self.prg(self.formula, e, red=reduction)
            self.formula = res
            b3 = B3(res.eval())
            if b3 == Boolean3.Top or b3 == Boolean3.Bottom: break
        print("Result Progression: %s after %s events." % (b3, self.counter))
        return res

    def push_event(self, event):
        self.trace.push_event(event)
