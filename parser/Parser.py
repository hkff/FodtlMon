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

   # Enter a parse tree produced by FODTLParser#constants.
    def enterConstant(self, ctx:FODTLParser.ConstantContext):
        pass

    # Exit a parse tree produced by FODTLParser#constants.
    def exitConstant(self, ctx:FODTLParser.ConstantContext):
        self.formula = Constant()

    # Exit a parse tree produced by FODTLParser#x.
    def exitSnext(self, ctx):
        self.formula = X(ctx)

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
        tr = parser.formula()
        bt = Trees.toStringTree(tr, recog=parser)
        print(bt)
        l = parser.getParseListeners().pop(0)
        return l.formula

