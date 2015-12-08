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

a = G(And(Next("e"), false()))
print(Ltlmon().prg(a, "PHI"))

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
print(Ltlmon().prg(G(true()), "PHI"))
