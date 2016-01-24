"""
fodtl parser
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
from parser.FODTLListener import *
from parser.FODTLLexer import *
from antlr4.InputStream import *
from antlr4.tree.Trees import Trees


class FodtlParser(ParseTreeListener):

    def __init__(self):
        self.formula = None
        self.formulas = []

    def exitMain(self, ctx:FODTLParser.MainContext):
        pass

    #############################
    # Classical logic
    #############################
    def exitTrue(self, ctx:FODTLParser.TrueContext):
        self.formulas.append(true())

    def exitFalse(self, ctx:FODTLParser.FalseContext):
        self.formulas.append(false())

    def exitConstant(self, ctx:FODTLParser.ConstantContext):
        self.formulas.append(Constant(""))

    def exitVariable(self, ctx:FODTLParser.VariableContext):
        self.formulas.append(Variable(""))

    def exitFormula(self, ctx:FODTLParser.FormulaContext):
        # Testing boolean operators
        con = ctx.O_and() or ctx.O_or() or ctx.O_imply()
        if con is not None:
            if len(self.formulas) > 1:
                f2 = self.formulas.pop()
                f1 = self.formulas.pop()
                if ctx.O_and() is not None: klass = And
                elif ctx.O_or() is not None: klass = Or
                elif ctx.O_imply() is not None: klass = Imply
                else: raise Exception("Type error")
                self.formulas.append(klass(f1, f2))
            else:
                raise Exception("Missing arguments")
        # Testing Unary temporal operators
        elif ctx.utOperators() is not None:
            if len(self.formulas) > 0:
                inner = self.formulas.pop()
                if ctx.utOperators().O_always() is not None: klass = Always
                elif ctx.utOperators().O_future() is not None: klass = Future
                elif ctx.utOperators().O_next() is not None: klass = Next
                else: raise Exception("Type error")
                self.formulas.append(klass(inner))
            else:
                raise Exception("Missing arguments")
        # Testing binary temporal operators
        elif ctx.btOperators() is not None:
            if len(self.formulas) > 1:
                f2 = self.formulas.pop()
                f1 = self.formulas.pop()
                if ctx.btOperators().O_until() is not None: klass = Until
                elif ctx.btOperators().O_release() is not None: klass = Release
                else: raise Exception("Type error")
                self.formulas.append(klass(f1, f2))
            else:
                raise Exception("Missing arguments")

    def exitNegation(self, ctx:FODTLParser.NegationContext):
        if len(self.formulas) > 0:
            inner = self.formulas.pop()
            self.formulas.append(Neg(inner))
        else:
            raise Exception("Missing arguments")

    def exitPredicate(self, ctx:FODTLParser.PredicateContext):
         if len(self.formulas) > 0:
            # inner = self.formulas.pop()
            # TODO handle args number
            self.formulas.append(Predicate("", []))

    def exitMain(self, ctx:FODTLParser.MainContext):
        if len(self.formulas) == 1:
            self.formula = self.formulas.pop()


    #######################
    # Parse
    #######################
    @staticmethod
    def parse(formula: str):
        f = InputStream(formula)
        lexer = FODTLLexer(f)
        stream = CommonTokenStream(lexer)
        parser = FODTLParser(stream)
        parser.addParseListener(FodtlParser())
        parser.buildParseTrees = True

        # TODO : important prediction mode optimization (we gain x5 speed up with SLL)
        # use SLL for the first pass, if an error detected we probably have to make a second pass
        # using LL mode (to check, see the doc)
        # parser._interp.predictionMode = PredictionMode.LL  # ~2.5
        parser._interp.predictionMode = PredictionMode.SLL  # ~0.4
        # parser._interp.predictionMode = PredictionMode.LL_EXACT_AMBIG_DETECTION  # ~2.5
        tr = parser.main()
        bt = Trees.toStringTree(tr, recog=parser)
        print(bt)
        l = parser.getParseListeners().pop(0)
        return l.formula

