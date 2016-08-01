"""
LTL proof tree monitor
Copyright (C) 2016 Walid Benghabrit

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
from fodtlmon.ltl.ltlmon import *


class Node:
    def __init__(self, value=None, next=None, children=None):
        self.value = value
        self.next = next
        self.children = [] if children is None else children

    def print(self, level=0):
        if isinstance(self.value, list):
            res = "- %s" % " , ".join([str(x) for x in self.value])
        else:
            res = "- %s" % self.value
        for x in self.children:
            res += "\n%s|---%s" % (level*"   ", x.print(level+1))
        return res

    @staticmethod
    def tex_wrapper(el):
        res = el
        if isinstance(el, list):
            res = " , ".join([str(x) for x in el])
        return str(res).replace("|", "$\\vee$").replace("&", "$\\wedge$")

    def tex(self):
        res = ""
        if len(self.children) == 3:
            res += self.children[0].tex()
            res += self.children[1].tex()
            res += self.children[2].tex()
            res += "\n\\TrinaryInfC{%s}" % self.tex_wrapper(self.value)
        if len(self.children) == 2:
            res += self.children[0].tex()
            res += self.children[1].tex()
            res += "\n\\BinaryInfC{%s}" % self.tex_wrapper(self.value)
        elif len(self.children) == 1:
            res += self.children[0].tex()
            res += "\n\\UnaryInfC{%s}" % self.tex_wrapper(self.value)
        elif len(self.children) == 0:
            res += "\n\\AxiomC{%s}" % self.tex_wrapper(self.value)
        return res

    @staticmethod
    def to_tex(node, output="gen.tex"):
        with open(output, "w+") as f:
            f.write("\\documentclass{article}\n\\usepackage{bussproofs}\n\\begin{document}\n\\begin{prooftree}\n"
                    "%s\n\\end{prooftree}\n\\end{document}\n" % node.tex())

        p = Popen(['pdflatex', output], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        p.stdout.read().decode("utf-8")
        os.remove(output.replace(".tex", ".aux"))
        os.remove(output.replace(".tex", ".log"))

"""
    A
-----------
 B       C
--     ------
 D      E  F
"""
# A = Node(value="A")
# B = Node(value="B")
# C = Node(value="C")
# D = Node(value="D")
# E = Node(value="E")
# F = Node(value="F")
# A.children.append(B)
# A.children.append(C)
# B.children.append(D)
# C.children.append(E)
# C.children.append(F)
# print(A.print())
# Node.to_tex(A)


class LtlproofMon(Mon):
    """
    LTL monitor using sequences technique.
    """

    def __init__(self, formula, trace):
        super().__init__(formula, trace)
        self.struct = self.build(self.formula)

    def monitor(self, once=False, debug=False, struct_res=False, optimization=Optimzation.NONE, output=None):
        if debug:
            start_time = time.time()

        for e in self.trace.events[self.counter:]:
            if self.last == Boolean3.Top or self.last == Boolean3.Bottom:
                break
            else:
                self.counter += 1
                self.counter2 += 1
                self.rewrite = self.prg(self.rewrite, e)
                self.last = B3(self.rewrite.eval()) if isinstance(self.rewrite, Formula) else self.rewrite
                if once: break

        if struct_res:
            ret = {"result": self.last, "at": self.counter2, "step": self.counter}
        else:
            ret = "Result Progression: %s after %s events." % (self.last, self.counter)
        # print(ret)
        if debug:
            exec_time = time.time() - start_time
            print("Execution time : %5.4f ms" % (exec_time*1000))
        return ret

    def prg(self, formula, event, valuation=None):
        return true()

    def build(self, formula, struct=None):
        """
        :param formula:
        :param event:
        :param valuation:
        :return:
        """
        if struct is None:
            struct = Node()

        if isinstance(formula, Predicate):
            struct.value = formula

        elif isinstance(formula, true):
            struct.value = true()

        elif isinstance(formula, false):
            struct.value = false()

        # elif isinstance(formula, Neg):
        #     res = Neg(self.prg(formula.inner, event, valuation)).eval()

        elif isinstance(formula, Or):
            """
                    Gamma ⊢  Delta, phi_1, phi_2
            [Or]  --------------------------------
                    Gamma ⊢ Delta, phi_1 ∨ phi_2
            """
            struct.value = formula
            # TODO
            n = Node(value=[formula.left, formula.right])

            n1 = self.build(formula.left).children
            n2 = self.build(formula.right).children
            n1.extend(n2)
            n.children.extend(n1)
            struct.children.append(n)

        elif isinstance(formula, And):
            """
                     Gamma ⊢ Delta, ph_1   Gamma ⊢ Delta, phi_2
            [And]  ---------------------------------------------
                       Gamma ⊢ Delta, phi_1 ∧ phi_2
            """
            struct.value = formula
            n1 = Node(value=formula.left)
            n1.children.extend(self.build(formula.left).children)
            struct.children.append(n1)

            n2 = Node(value=formula.right)
            n2.children.extend(self.build(formula.right).children)
            struct.children.append(n2)

        elif isinstance(formula, Always):
            """
                      Gamma ⊢ Delta, phi     Gamma ⊢ Delta, X (G phi)
            [Always] -------------------------------------------------
                                 Gamma ⊢ Delta, G phi
            """
            struct.value = formula
            struct.children.append(Node(value=formula.inner))
            struct.children.append(Node(value=X(formula)))

        elif isinstance(formula, Future):
            """
                        Gamma ⊢ Delta, phi, X (F phi)
            [Future]  --------------------------------
                           Gamma ⊢ Delta, F phi
            """
            struct.value = formula
            struct.children.append(Node(value=[formula.inner, X(formula)]))

        # elif isinstance(formula, Next):
        #     res = formula.inner

        else:
            raise Exception("Error %s of type %s" % (formula, type(formula)))

        return struct

tr = Trace().parse("{};{};{}")
fl = FodtlParser.parse("(G(p('x'))) | (F(G(h('x'))))")
mon = LtlproofMon(fl, tr)
res = mon.monitor()
print(res)
print(mon.struct.print())
Node.to_tex(mon.struct)

