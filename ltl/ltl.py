__author__ = 'hkff'

class Token(object):
    def __str__(self):
        return self.__class__.__name__


class Exp:
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

class Atom(Exp): pass


#############################
# LTL Operators
#############################

##
# Always
##
class Always(Exp):
    def __init__(self, inner=None):
        self.inner = inner

    def __str__(self):
        return "Always(" + str(self.inner) + ")"


class G(Always):
    def __str__(self):
        return "G(" + str(self.inner) + ")"


class Future(Exp):
    def __init__(self, inner=None):
        self.inner = inner

    def __str__(self):
        return "Future(" + str(self.inner) + ")"


class F(Future):
    def __str__(self):
        return "F(" + str(self.inner) + ")"


a = G(F(True))
print(a)
