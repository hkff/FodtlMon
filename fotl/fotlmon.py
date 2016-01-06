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
            print("%s %s" % (formula, valuation))
            # for a in formula.args:
            #     if isinstance(a, Variable):
            # TODO review
            for v in valuation:
                for a in formula.args:
                    print("p test %s %s" % (a.name, v.var))
                    if a.name == v.var:
                        # TODO check type
                        print("true")
                        return true()
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
                    [print(x) for x in valuation2]
            print(elems)
            return self.prg(ForallConj(elems), event, valuation)

        elif isinstance(formula, ForallConj):
            print(formula)
            e = []
            for x in formula.inner:
                # Eval all nodes with their eval2
                e.append(ForallConjNode(self.prg(x.formula, event, x.valuation), valuation))
            res = ForallConj(e).eval()
            print("ret %s " % res)
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
