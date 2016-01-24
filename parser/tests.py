"""
fodtl parser tests
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

from fodtl.fodtl import *
from parser.Parser import *


def test(res, _type):
    if isinstance(res, _type):
        print("=== OK : %s %s" % (res, _type))
    else:
        print("=== KO : %s %s" % (res, _type))

"""
G a
F a
X a
a U b
a R b
Forall VD('l', 'type')
Exists
@()
"""

# true
test(FodtlParser.parse("true"), true)

# false
test(FodtlParser.parse("false"), false)

# Constant
#test(FodtlParser.parse("'s'"), Constant)

# Variable
#test(FodtlParser.parse("v"), Variable)

# Predicate
#test(FodtlParser.parse("P('s')"), Predicate)

# And
test(FodtlParser.parse("true & false"), And)

# Or
test(FodtlParser.parse("true | false"), Or)

# Imply
test(FodtlParser.parse("true => false"), Imply)


# Neg
test(FodtlParser.parse("~ true"), Neg)

# Next
test(FodtlParser.parse("X(true)"), Next)

# Always
test(FodtlParser.parse("G(true)"), Always)

# Future
test(FodtlParser.parse("F(true)"), Future)

# Until
test(FodtlParser.parse("true U false"), Until)

# Release
test(FodtlParser.parse("true R false"), Release)

print((FodtlParser.parse("ARG('y', 'secret') ")))
exit()
print((FodtlParser.parse("In(2, [1,2])")))
