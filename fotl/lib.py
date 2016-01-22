"""
lib LTL monitor
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

from fotl.fotl import *
import re


class Eq(IP):
    """
    Equality operator
    """
    def __init__(self, *args):
        super().__init__(args)

    def eval(self, valuation=None):
        args2 = super().eval(valuation=valuation)
        return str(args2[0]) == str(args2[1])


class Gt(IP):
    """
    Greater than
    """
    def __init__(self, *args):
        super().__init__(args)

    def eval(self, valuation=None):
        args2 = super().eval(valuation=valuation)
        return int(args2[0].name) > int(args2[1].name)


class Lt(IP):
    """
    Greater than
    """
    def __init__(self, *args):
        super().__init__(args)

    def eval(self, valuation=None):
        args2 = super().eval(valuation=valuation)
        return int(args2[0].name) < int(args2[1].name)


class Regex(IP):
    """
    Regular expression
    """
    def __init__(self, *args):
        super().__init__(args)

    def eval(self, valuation=None):
        args2 = super().eval(valuation=valuation)
        p = re.compile(args2[1].name)
        return False if p.match(args2[0].name) is None else True


####################
# Math functions
####################
class Add(FX):
    def __init__(self, *args):
        super().__init__(args)

    def eval(self, valuation=None):
        args2 = super().eval(valuation=valuation)
        return int(args2[0].name) + int(args2[1].name)

