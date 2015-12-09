"""
test file
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
from ltl.ltlmon import *
import inspect
import imp
from random import random
import os

#
# a = G(And(Next("e"), false()))
# #print(Ltlmon(a).prg(a, "PHI"))
#
# d = P("send", [V("a"), V("b")])
# print(d)
# print(Event.parse("{P(a) | P(b)}"))
# print(Trace.parse("{P(a) | P(b,d)}; {O(c)}"))
# print(Boolean3.Bottom.value)
# print(Boolean3.Top.value)
# print(Boolean3.Unknown.value)
# print(Trace.parse("{data('d') | data('t') | read('d')}; {data('g')}"))
# print(Trace.parse("{P(o)}"))
# print(Trace.parse(""))
#print(Ltlmon().prg(G(true()), "PHI"))


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
    print(res)
    return res


class Fuzzer:
    """
    Monitors tester
    """
    def __init__(self, language, alphabet=None, constants=None):
        self.nodes = []
        self.language = language
        self.constants = [] if constants is None else constants
        self.alphabet = [] if alphabet is None else alphabet

    def init_fuzzer(self):
        ltl = imp.load_source("ltl", "ltl/ltl.py")
        for name, obj in inspect.getmembers(ltl.ltl):
            if inspect.isclass(obj):
                # Get only classes that are defined in ltl
                if obj.__module__ == "ltl.ltl":
                    # Get only classes inherit from Exp
                    if obj.__base__ is UExp or obj.__base__ is BExp or obj in (true, false, Predicate):
                        self.nodes.append(obj)

    def gen(self, depth):
        if depth == 0:
            i = int(random() * 100) % len(self.alphabet)
            j = int(random() * 100) % len(self.constants)
            return P(self.alphabet[i], [Constant(self.constants[j])])

        res = None
        n = int(random()*10)
        node = self.nodes[n % len(self.nodes)]
        if node.__base__ is UExp:
            res = node(self.gen(depth-1))
        elif node.__base__ is BExp:
            res = node(self.gen(depth-1), self.gen(depth-1))
        elif node in (true, false):
            res = node()
        elif node is Predicate:
            i = int(random() * 100) % len(self.alphabet)
            j = int(random() * 100) % len(self.constants)
            res = P(self.alphabet[i], [Constant(self.constants[j])])
        return res

    def gen_trace(self, length, max_depth=2, depth=0):
        trace = Trace()
        for x in range(length):
            i = int(random() * 10) % len(self.alphabet)
            j = int(random() * 10) % len(self.constants)
            dp = int(random() * 10) % max_depth if depth == 0 else depth
            e = Event()
            for y in range(dp):
                res = P(self.alphabet[i], [Constant(self.constants[j])])
                e.push_predicate(res)
            trace.push_event(e)
        return trace


###########################
# Main
###########################
def print2(*args, file=None):
    print(*args)
    if file is not None:
        file.write(*args)
        file.write("\n")

fuzzer = Fuzzer("ltl", alphabet=["P"], constants=["a", "b", "c"])
fuzzer.init_fuzzer()

with open("tests/logs.log", "w+") as f:
    for x in range(1):
        formula = fuzzer.gen(5)
        trace = fuzzer.gen_trace(3, depth=1)
        print2("\n============ LTLMON : ", file=f)
        print2("Formula   : %s\nFormula C : %s\nTrace     : %s" % (formula, formula.toCODE(), trace), file=f)
        res1 = Ltlmon(formula, trace).monitor(reduction=True)
        f.write(res1)

        print2("\n============ LTLFO2MON : ", file=f)
        fl = formula.toLTLFO()
        tr = trace.toLTLFO()
        print2("Formula : %s\nTrace   : %s" % (fl, tr), file=f)
        res2 = ltlfo2mon(fl, tr)
        f.write(res2)

        if res1 != res2:
            print2("\n## Result are different ! ", file=f)
            print2(res1, file=f)
            print2(res2, file=f)
            input("Press Enter to continue")

