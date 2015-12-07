__author__ = 'hkff'

from ltl.ltl import *
from ltl.ltlmon import *

a = G(F(True))
aa = Always(True)
print(prg(a, None))
