from ltl.ltl import *


def prg(formula, trace):

    if isinstance(formula, Predicate):
        return true() if formula in AP else false()

    if isinstance(formula, true):
        return true()

    if isinstance(formula, false):
        return false()

    if isinstance(formula, Neg):
        return Neg(prg(formula.inner, trace))

    elif isinstance(formula, Or):
        return Or(prg(formula.left, trace), prg(formula.right, trace))

    elif isinstance(formula, And):
        return And(prg(formula.left, trace), prg(formula.right, trace))

    elif isinstance(formula, Always):
        return And(prg(formula.inner, trace), G(formula.inner))

    elif isinstance(formula, Future):
        return Or(prg(formula.inner, trace), F(formula.inner))

    elif isinstance(formula, Until):
        return Or(prg(formula.right, trace), And(prg(formula.left, trace), U(formula.left, formula.right)))

    elif isinstance(formula, Release):
        return Or(prg(formula.left, trace), And(prg(formula.right, trace), R(formula.left, formula.right)))

    elif isinstance(formula, Next):
        return formula.inner

a = G(F(True))

