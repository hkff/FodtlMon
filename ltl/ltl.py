__author__ = 'hkff'

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
        pass

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


class false(Atom):
    """
    False
    """
    symbol = "false"


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


class Or(BExp):
    symbol = "or"


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

    def push_predicate(self, predicate):
        self.predicates.append(predicate)
        return self

    p = push_predicate


class Trace:
    def __init__(self, events=[]):
        self.events = events

    def __str__(self):
        return "[" + ",".join([str(e) for e in self.events]) + "]"

    def push_event(self, event):
        self.events.append(event)
        return self

    e = push_event

#############################
# Test
#############################
a = G( And(true(), false()))
aa = Always(True)

t = Trace()
