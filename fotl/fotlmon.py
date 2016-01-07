"""
fotlmon FOTL monitor
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
from ltl.ltlmon import *
from fotl.fotl import *


class Fotlmon(Ltlmon):
    """
    Fotl monitoring using progression technique
    """
    def prg(self, formula, event, valuation=None):
        if isinstance(formula, Predicate):
            # Overrides the Predicate test of Ltlmon
            # 1. Check if args are vars of P
            for a in formula.args:
                # 2. Check in trace if event contains P with for all linked vars
                for v in valuation:
                    z = Predicate(formula.name, [Constant(str(v.value))])
                    res = event.contains(z)
                    if res:
                        return true()
            # TODO optimize
            return true() if event.contains(formula) else false()

        if isinstance(formula, Forall):
            elems = []
            if valuation is None:
                valuation = []

            for p in event.predicates:
                if p.name == formula.var.vtype:
                    valuation2 = []
                    valuation2.extend(valuation)
                    for v in p.args:
                        # Bind the value of the variable in the predicate
                        # with the variable name in the VarDec
                        valuation2.append(Valuation(v, formula.var.name))
                    # Add the formula with the valuation for the variable
                    elems.append(ForallConjNode(formula.inner, valuation2))
            return self.prg(ForallConj(elems), event, valuation)

        elif isinstance(formula, ForallConj):
            e = []
            for x in formula.inner:
                # Eval all nodes with their eval2
                e.append(ForallConjNode(self.prg(x.formula, event, x.valuation), valuation))
            res = ForallConj(e).eval()
            return res

        else:
            return super().prg(formula, event, valuation)


class ForallConj(UExp):
    """
    Forall Conjunction (internal for monitor)
    """
    symbol = "\u2227"

    def __init__(self, inner=None):
        super().__init__(inner)

    def eval(self):
        elems2 = list(filter(lambda x: not isinstance(x.formula, true), self.inner))
        if len(elems2) == 0:
            return Boolean3.Top
        elif len(list(filter(lambda x: isinstance(x.formula, false), self.inner))) > 0:
            return Boolean3.Bottom
        else:
            return ForallConj(elems2)

    def __str__(self):
        return "%s (%s)" % (self.symbol, ", ".join([str(x) for x in self.inner]))


class ForallConjNode:
    """
    Forall conjunction node contains formula -> evaluation
    """
    def __init__(self, formula=None, valuation=None):
        self.formula = formula
        self.valuation = valuation

    def __str__(self):
        return "(%s : %s)" % (self.formula, ",".join([str(x) for x in self.valuation]))
