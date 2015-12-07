__author__ = 'hkff'

from ltl.ltl import *
from ltl.ltlmon import *

a = G(And(Next("e"), false()))
print(prg(a, "PHI"))

d = P("send", [V("a"), V("b")])
print(d)
