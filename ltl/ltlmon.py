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
import os
import copy
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
        self.last = Boolean3.Unknown
        self.rewrite = copy.deepcopy(self.formula)

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

    def monitor(self, once=False):
        for e in self.trace.events[self.counter:]:
            self.counter += 1
            self.rewrite = self.prg(self.rewrite, e)
            Debug(self.rewrite)
            self.last = B3(self.rewrite.eval()) if isinstance(self.rewrite, Formula) else self.rewrite
            if self.last == Boolean3.Top or self.last == Boolean3.Bottom or once: break
        ret = "Result Progression: %s after %s events." % (self.last, self.counter)
        # print(ret)
        return ret

    def prg(self, formula, trace, valuation=None):
        # print(formula)
        if isinstance(formula, Predicate):
            # Todo : Check if Predicate is in AP
            res = true() if trace.contains(formula) else false()

        elif isinstance(formula, true):
            res = true()

        elif isinstance(formula, false):
            res = false()

        elif isinstance(formula, Neg):
            res = Neg(self.prg(formula.inner, trace, valuation)).eval()

        elif isinstance(formula, Or):
            res = Or(self.prg(formula.left, trace, valuation), self.prg(formula.right, trace, valuation)).eval()

        elif isinstance(formula, And):
            res = And(self.prg(formula.left, trace, valuation), self.prg(formula.right, trace, valuation)).eval()

        elif isinstance(formula, Always):
            res = And(self.prg(formula.inner, trace, valuation), G(formula.inner)).eval()

        elif isinstance(formula, Future):
            res = Or(self.prg(formula.inner, trace, valuation), F(formula.inner)).eval()

        elif isinstance(formula, Until):
            res = Or(self.prg(formula.right, trace, valuation),
                     And(self.prg(formula.left, trace, valuation), U(formula.left, formula.right)).eval()).eval()

        elif isinstance(formula, Release):
            res = Or(self.prg(formula.left, trace, valuation),
                     And(self.prg(formula.right, trace, valuation), R(formula.left, formula.right)).eval()).eval()

        elif isinstance(formula, Next):
            res = formula.inner

        else:
            print("Error " + str(formula))
            return None
        return res


def ltlfo2mon(formula:Formula, trace:Trace):
    """
    Run ltlfo2mon
    :param formula: Formula | ltlfo string formula
    :param trace: Trace | ltlfo string trace
    :return:
    """
    fl = formula.toLTLFO() if isinstance(formula, Formula) else formula
    tr = trace.toLTLFO() if isinstance(trace, Trace) else trace
    cmd = "echo \"%s\" | java -jar tools/ltlfo2mon.jar -p \"%s\"" % (tr, fl)
    p = os.popen(cmd)
    res = p.readline()[:-1]
    p.close()
    # print(res)
    return res