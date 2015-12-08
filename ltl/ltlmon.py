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
from ltl.ltl import *


class Mon:
    """
    Abstract monitor
    """
    pass


class Ltlmon(Mon):
    """
    LTL monitor using progression technique
    """
    def prg(self, formula, trace):
        # print(formula)
        if isinstance(formula, Predicate):
            return true() if formula in AP else false()

        if isinstance(formula, true):
            return true()

        if isinstance(formula, false):
            return false()

        if isinstance(formula, Neg):
            return Neg(self.prg(formula.inner, trace))

        elif isinstance(formula, Or):
            return Or(self.prg(formula.left, trace), self.prg(formula.right, trace))

        elif isinstance(formula, And):
            return And(self.prg(formula.left, trace), self.prg(formula.right, trace))

        elif isinstance(formula, Always):
            return And(self.prg(formula.inner, trace), G(formula.inner))

        elif isinstance(formula, Future):
            return Or(self.prg(formula.inner, trace), F(formula.inner))

        elif isinstance(formula, Until):
            return Or(self.prg(formula.right, trace), And(self.prg(formula.left, trace), U(formula.left, formula.right)))

        elif isinstance(formula, Release):
            return Or(self.prg(formula.left, trace), And(self.prg(formula.right, trace), R(formula.left, formula.right)))

        elif isinstance(formula, Next):
            return formula.inner

        else:
            print("Error " + formula)
            return None
