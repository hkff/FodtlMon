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


a = G(And(Next("e"), false()))
#print(Ltlmon(a).prg(a, "PHI"))

d = P("send", [V("a"), V("b")])
print(d)
print(Event.parse("{P(a) | P(b)}"))
print(Trace.parse("{P(a) | P(b,d)}; {O(c)}"))
print(Boolean3.Bottom.value)
print(Boolean3.Top.value)
print(Boolean3.Unknown.value)
print(Trace.parse("{data('d') | data('t') | read('d')}; {data('g')}"))
print(Trace.parse("{P(o)}"))
print(Trace.parse(""))
#print(Ltlmon().prg(G(true()), "PHI"))


class Fuzzer:
    """
    Monitors tester
    """
    def __init__(self, language, alphabet=[], constants=[]):
        self.nodes = []
        self.language = language
        self.constants = constants
        self.alphabet = alphabet

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
        if depth < 0:
            return
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
        print(res)
        #print(node)
        print(self.gen_trace(2))
        #Ltlmon(res, Trace()).monitor(reduction=False)
        return res

    def gen_trace(self, length):
        trace = Trace()
        for x in range(length):
            print("x " + str(x) + " " + str(trace))
            i = int(random() * 10) % len(self.alphabet)
            j = int(random() * 10) % len(self.constants)
            res = P(self.alphabet[i], [Constant(self.constants[j])])
            print(res)
            e = Event()#.push_predicate(res)
            trace.push_event(e)
        return trace

f = Fuzzer("ltl", alphabet=["P", "F"], constants=["a", "b", "c"])
f.init_fuzzer()
f.gen(5)
