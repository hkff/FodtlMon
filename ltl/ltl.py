"""
ltl
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

from enum import Enum

#############################
# Abstract operators
#############################


class Exp:
    """
    Abstract expression
    """
    def toTSPASS(self):
        pass

    def reduce(self):
        pass

    def eval(self):
        return self

    def clos(self):
        pass

    def nnf(self):
        pass


class Atom(Exp):
    """
    Atom
    """
    symbol = ""

    def __str__(self):
        return str(self.symbol)


class true(Atom):
    """
    True
    """
    symbol = "true"

    def eval(self):
        return True


class false(Atom):
    """
    False
    """
    symbol = "false"

    def eval(self):
        return False


class Parameter(Exp):
    """
    Parameter
    """
    def __init__(self, name=""):
        self.name = name

    def __str__(self):
        return self.name

    def equal(self, o):
        return (o is not None) and isinstance(o, Parameter) and (o.name == self.name)


class Variable(Parameter):
    """
    Data variable
    """
    def equal(self, o):
        return (o is not None) and isinstance(o, Variable) and (o.name == self.name)

V = Variable


class Constant(Parameter):
    """
    Constant
    """
    def equal(self, o):
        return (o is not None) and isinstance(o, Constant) and (o.name == self.name)

C = Constant


class Predicate(Exp):
    """
    Predicate
    """
    def __init__(self, name="", args=[]):
        self.name = name
        self.args = args

    def __str__(self):
        args = ",".join([str(p) for p in self.args])
        return "%s(%s)" % (self.name, args)

    @staticmethod
    def parse(string: str):
        string = string.strip()
        if string.endswith(")"):
            name = string[0: string.find("(")]
            args = string[string.find("(")+1:-1].split(",")
            arguments = []
            [arguments.append(Variable(ar)) for ar in args]
        else:
            print("Invalid predicate format !")
            return
        return Predicate(name, arguments)

P = Predicate


class UExp(Exp):
    """
    Unary expression
    """
    symbol = ""

    def __init__(self, inner=None):
        self.inner = inner

    def __str__(self):
        return "%s(%s)" % (self.symbol, self.inner)


class BExp(Exp):
    """
    Binary expression
    """
    symbol = ""

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def __str__(self):
        return "(%s %s %s)" % (self.left, self.symbol, self.right)


#############################
# LTL Operators
#############################

##
# Propositional operators
##
class And(BExp):
    symbol = "and"

    def eval(self):
        if isinstance(self.left, true):
            if isinstance(self.right, true): return true()
            elif isinstance(self.right, false): return false()
            else: return self.right
        elif isinstance(self.left, false):
            return false()
        else:
            if isinstance(self.right, true): return self.left
            elif isinstance(self.right, false): return false()
            else: return self


class Or(BExp):
    symbol = "or"

    def eval(self):
        if isinstance(self.left, true):
            return true()
        elif isinstance(self.left, false):
            if isinstance(self.right, true): return true()
            elif isinstance(self.right, false): return false()
            else: return self.right
        else:
            if isinstance(self.right, true): return true()
            elif isinstance(self.right, false): return self.left
            else: return self


class Neg(UExp):
    symbol = "not"


##
# Temporal operators
##

# Always
class Always(UExp):
    symbol = "always"


class G(Always):
    symbol = "G"


# Future
class Future(UExp):
    symbol = "future"


class F(Future):
    symbol = "F"


# Next
class Next(UExp):
    symbol = "next"


class X(Next):
    symbol = "X"


# Until
class Until(BExp):
    symbol = "until"


class U(Until):
    symbol = "U"


# Release
class Release(BExp):
    symbol = "release"


class R(Release):
    symbol = "R"


#############################
# Trace / Events
#############################
class Event:
    def __init__(self, predicates=[]):
        self.predicates = predicates

    def __str__(self):
        return "{" + " | ".join([str(p) for p in self.predicates]) + "}"

    @staticmethod
    def parse(string):
        string = string.strip()
        predicates = []
        if string.startswith("{") and string.endswith("}"):
            prs = string[1:-1].split("|")
            [predicates.append(Predicate.parse(p)) for p in prs]
        else:
            print("Invalid event format ! A trace should be between {}")
            return
        return Event(predicates)

    def push_predicate(self, predicate):
        self.predicates.append(predicate)
        return self

    p = push_predicate


class Trace:
    def __init__(self, events=[]):
        self.events = events

    def __str__(self):
        return "[" + ";".join([str(e) for e in self.events]) + "]"

    @staticmethod
    def parse(string):
        string = string.strip()
        events = []
        evs = string.split(";")
        [events.append(Event.parse(e)) if e != "" else None for e in evs]
        return Trace(events)

    def push_event(self, event):
        self.events.append(event)
        return self

    e = push_event


class Boolean3(Enum):
    """
    Boolean3 values
    """
    Top = "\u22A4"
    Bottom = "\u22A5"
    Unknown = "?"


def B3(formula):
    """
    Rewrite formula eval result into Boolean3
    :param formula:
    :return: Boolean3
    """
    if isinstance(formula, true) or formula is True:
        return Boolean3.Top
    if isinstance(formula, false) or formula is False:
        return Boolean3.Bottom
    else:
        return Boolean3.Unknown

#############################
# Test
#############################
a = G( And(true(), false()))
aa = Always(True)

t = Trace()
