__author__ = 'hkff'

from ltl.ltl import *
from ltl.ltlmon import *

a = G(And(Next("e"), false()))
print(prg(a, "PHI"))

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