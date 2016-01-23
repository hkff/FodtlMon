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


# Next
test(FodtlParser.parse("'s'"), Constant)

# Next
test(FodtlParser.parse("X(s)"), Next)

