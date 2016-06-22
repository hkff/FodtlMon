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
__author__ = 'walid'

from fodtlmon.ltl.ltl import *
from fodtlmon.parser.Parser import *
import os
import copy
import time
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
        self.formula = FodtlParser.parse(formula) if isinstance(formula, str) else formula
        self.trace = trace
        self.counter = 0
        self.last = Boolean3.Unknown
        self.counter2 = 0
        self.rewrite = copy.deepcopy(self.formula)
        self.optimization = False

    def monitor(self, *args, **kargs):
        pass

    def prg(self, *args, **kargs):
        pass

    def push_event(self, event):
        self.trace.push_event(event)

    def reset(self):
        self.rewrite = copy.deepcopy(self.formula)


class Ltlmon(Mon):
    """
    LTL monitor using progression technique.
    """

    def monitor(self, once=False, debug=False, struct_res=False, optimization=False):
        self.optimization = optimization
        if debug:
            start_time = time.time()

        for e in self.trace.events[self.counter:]:
            if self.last == Boolean3.Top or self.last == Boolean3.Bottom:
                break
            else:
                self.counter += 1
                self.counter2 += 1
                self.rewrite = self.prg(self.rewrite, e)
                # Debug(self.rewrite)
                self.last = B3(self.rewrite.eval()) if isinstance(self.rewrite, Formula) else self.rewrite
                if once: break

        if struct_res:
            ret = {"result": self.last, "at": self.counter2, "step": self.counter}
        else:
            ret = "Result Progression: %s after %s events." % (self.last, self.counter)
        # print(ret)
        if debug:
            exec_time = time.time() - start_time
            print("Execution time : %5.4f ms" % (exec_time*1000))
        return ret

    def prg(self, formula, event, valuation=None):
        """
        Progression function
        :param formula:
        :param event:
        :param valuation:
        :return:
        """
        # print(formula)
        formula = self.optimize(formula)

        if isinstance(formula, Predicate):
            # Todo : Check if Predicate is in AP
            res = true() if event.contains(formula) else false()

        elif isinstance(formula, true):
            res = true()

        elif isinstance(formula, false):
            res = false()

        elif isinstance(formula, Neg):
            res = Neg(self.prg(formula.inner, event, valuation)).eval()

        elif isinstance(formula, Or):
            res = Or(self.prg(formula.left, event, valuation), self.prg(formula.right, event, valuation)).eval()

        elif isinstance(formula, And):
            res = And(self.prg(formula.left, event, valuation), self.prg(formula.right, event, valuation)).eval()

        elif isinstance(formula, Always):
            res = And(self.prg(formula.inner, event, valuation), G(formula.inner)).eval()

        elif isinstance(formula, Future):
            res = Or(self.prg(formula.inner, event, valuation), F(formula.inner)).eval()

        elif isinstance(formula, Until):
            res = Or(self.prg(formula.right, event, valuation),
                     And(self.prg(formula.left, event, valuation), U(formula.left, formula.right)).eval()).eval()

        elif isinstance(formula, Release):
            res = Or(self.prg(formula.left, event, valuation),
                     And(self.prg(formula.right, event, valuation), R(formula.left, formula.right)).eval()).eval()

        elif isinstance(formula, Next):
            res = formula.inner

        else:
            raise Exception("Error %s of type %s" % (formula, type(formula)))
        return res

    def optimize(self, formula):
        """
        Applying simplifications rules
        :param formula:
        :return:
        """
        if not self.optimization:
            return formula

        res = formula
        if isinstance(formula, Neg):
            # res = Neg(self.prg(formula.inner, event, valuation)).eval()
            pass

        elif isinstance(formula, Or):
            # p | ~p  ::=  true
            if isinstance(formula.right, Neg) and str(formula.right.inner) == str(formula.left):
                res = true()
            # (p U q) & q  ::=  p U q
            elif isinstance(formula.left, Until) and str(formula.left.right) == str(formula.right):
                res = formula.left

        elif isinstance(formula, And):
            # p & ~p  ::=  false
            if isinstance(formula.right, Neg) and str(formula.right.inner) == str(formula.left):
                res = false()
            # (p U q) & q  ::=  q
            elif isinstance(formula.left, Until) and str(formula.left.right) == str(formula.right):
                res = formula.right
            # F(p) & (F(p) & GF(p))  ::=  F(p) & GF(p)
            elif isinstance(formula.left, Future) and isinstance(formula.right, And) and \
                    str(formula.right.left) == str(formula.left) and isinstance(formula.right.right, Always):
                res = formula.right
            # p & (p & (p U q))  ::= p & (p U q)
            elif isinstance(formula.right, And)and isinstance(formula.right.right, Until) and \
                    str(formula.left) == str(formula.right.left) == str(formula.right.right.left):
                res = formula.right
            # (p U q) & q  ::= q
            elif isinstance(formula.left, Until) and str(formula.left.right) == str(formula.right):
                res = formula.right

        elif isinstance(formula, Always):
            res = Always(self.optimize(formula.inner))

        elif isinstance(formula, Future):
            tmp = self.optimize(formula.inner)
            if isinstance(tmp, false):
                res = tmp
            else:
                res = Future(tmp)

        elif isinstance(formula, Until):
            res = Until(self.optimize(formula.left), self.optimize(formula.right))

        elif isinstance(formula, Release):
            pass

        elif isinstance(formula, Next):
            res = self.optimize(formula.inner)

        return res


def ltlfo2mon(formula: Formula, trace: Trace, mon: str="-p"):
    """
    Run ltlfo2mon
    :param formula: Formula | ltlfo string formula
    :param trace: Trace | ltlfo string trace
    :param mon: str | monitoring technique p / sa / "" for sa-opt
    :return:
    """
    fl = formula.toLTLFO() if isinstance(formula, Formula) else formula
    tr = trace.toLTLFO() if isinstance(trace, Trace) else trace
    cmd = "echo \"%s\" | java -jar fodtlmon/tools/ltlfo2mon.jar %s \"%s\"" % (tr, mon, fl)
    p = os.popen(cmd)
    res = p.readline()[:-1]
    p.close()
    return res
