# Generated from ../../../fodtlmon/parser/FODTL.g4 by ANTLR 4.5.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FODTLParser import FODTLParser
else:
    from FODTLParser import FODTLParser

# This class defines a complete listener for a parse tree produced by FODTLParser.
class FODTLListener(ParseTreeListener):

    # Enter a parse tree produced by FODTLParser#h_lpar.
    def enterH_lpar(self, ctx:FODTLParser.H_lparContext):
        pass

    # Exit a parse tree produced by FODTLParser#h_lpar.
    def exitH_lpar(self, ctx:FODTLParser.H_lparContext):
        pass


    # Enter a parse tree produced by FODTLParser#h_rpar.
    def enterH_rpar(self, ctx:FODTLParser.H_rparContext):
        pass

    # Exit a parse tree produced by FODTLParser#h_rpar.
    def exitH_rpar(self, ctx:FODTLParser.H_rparContext):
        pass


    # Enter a parse tree produced by FODTLParser#h_lbar.
    def enterH_lbar(self, ctx:FODTLParser.H_lbarContext):
        pass

    # Exit a parse tree produced by FODTLParser#h_lbar.
    def exitH_lbar(self, ctx:FODTLParser.H_lbarContext):
        pass


    # Enter a parse tree produced by FODTLParser#h_rbar.
    def enterH_rbar(self, ctx:FODTLParser.H_rbarContext):
        pass

    # Exit a parse tree produced by FODTLParser#h_rbar.
    def exitH_rbar(self, ctx:FODTLParser.H_rbarContext):
        pass


    # Enter a parse tree produced by FODTLParser#h_dot.
    def enterH_dot(self, ctx:FODTLParser.H_dotContext):
        pass

    # Exit a parse tree produced by FODTLParser#h_dot.
    def exitH_dot(self, ctx:FODTLParser.H_dotContext):
        pass


    # Enter a parse tree produced by FODTLParser#h_colon.
    def enterH_colon(self, ctx:FODTLParser.H_colonContext):
        pass

    # Exit a parse tree produced by FODTLParser#h_colon.
    def exitH_colon(self, ctx:FODTLParser.H_colonContext):
        pass


    # Enter a parse tree produced by FODTLParser#h_equal.
    def enterH_equal(self, ctx:FODTLParser.H_equalContext):
        pass

    # Exit a parse tree produced by FODTLParser#h_equal.
    def exitH_equal(self, ctx:FODTLParser.H_equalContext):
        pass


    # Enter a parse tree produced by FODTLParser#formula.
    def enterFormula(self, ctx:FODTLParser.FormulaContext):
        pass

    # Exit a parse tree produced by FODTLParser#formula.
    def exitFormula(self, ctx:FODTLParser.FormulaContext):
        pass


    # Enter a parse tree produced by FODTLParser#atom.
    def enterAtom(self, ctx:FODTLParser.AtomContext):
        pass

    # Exit a parse tree produced by FODTLParser#atom.
    def exitAtom(self, ctx:FODTLParser.AtomContext):
        pass


    # Enter a parse tree produced by FODTLParser#predicate.
    def enterPredicate(self, ctx:FODTLParser.PredicateContext):
        pass

    # Exit a parse tree produced by FODTLParser#predicate.
    def exitPredicate(self, ctx:FODTLParser.PredicateContext):
        pass


    # Enter a parse tree produced by FODTLParser#variable.
    def enterVariable(self, ctx:FODTLParser.VariableContext):
        pass

    # Exit a parse tree produced by FODTLParser#variable.
    def exitVariable(self, ctx:FODTLParser.VariableContext):
        pass


    # Enter a parse tree produced by FODTLParser#constant.
    def enterConstant(self, ctx:FODTLParser.ConstantContext):
        pass

    # Exit a parse tree produced by FODTLParser#constant.
    def exitConstant(self, ctx:FODTLParser.ConstantContext):
        pass


    # Enter a parse tree produced by FODTLParser#true.
    def enterTrue(self, ctx:FODTLParser.TrueContext):
        pass

    # Exit a parse tree produced by FODTLParser#true.
    def exitTrue(self, ctx:FODTLParser.TrueContext):
        pass


    # Enter a parse tree produced by FODTLParser#false.
    def enterFalse(self, ctx:FODTLParser.FalseContext):
        pass

    # Exit a parse tree produced by FODTLParser#false.
    def exitFalse(self, ctx:FODTLParser.FalseContext):
        pass


    # Enter a parse tree produced by FODTLParser#negation.
    def enterNegation(self, ctx:FODTLParser.NegationContext):
        pass

    # Exit a parse tree produced by FODTLParser#negation.
    def exitNegation(self, ctx:FODTLParser.NegationContext):
        pass


    # Enter a parse tree produced by FODTLParser#conjunction.
    def enterConjunction(self, ctx:FODTLParser.ConjunctionContext):
        pass

    # Exit a parse tree produced by FODTLParser#conjunction.
    def exitConjunction(self, ctx:FODTLParser.ConjunctionContext):
        pass


    # Enter a parse tree produced by FODTLParser#disjunction.
    def enterDisjunction(self, ctx:FODTLParser.DisjunctionContext):
        pass

    # Exit a parse tree produced by FODTLParser#disjunction.
    def exitDisjunction(self, ctx:FODTLParser.DisjunctionContext):
        pass


    # Enter a parse tree produced by FODTLParser#implication.
    def enterImplication(self, ctx:FODTLParser.ImplicationContext):
        pass

    # Exit a parse tree produced by FODTLParser#implication.
    def exitImplication(self, ctx:FODTLParser.ImplicationContext):
        pass


    # Enter a parse tree produced by FODTLParser#equivalence.
    def enterEquivalence(self, ctx:FODTLParser.EquivalenceContext):
        pass

    # Exit a parse tree produced by FODTLParser#equivalence.
    def exitEquivalence(self, ctx:FODTLParser.EquivalenceContext):
        pass


    # Enter a parse tree produced by FODTLParser#variabledec.
    def enterVariabledec(self, ctx:FODTLParser.VariabledecContext):
        pass

    # Exit a parse tree produced by FODTLParser#variabledec.
    def exitVariabledec(self, ctx:FODTLParser.VariabledecContext):
        pass


    # Enter a parse tree produced by FODTLParser#uQuant.
    def enterUQuant(self, ctx:FODTLParser.UQuantContext):
        pass

    # Exit a parse tree produced by FODTLParser#uQuant.
    def exitUQuant(self, ctx:FODTLParser.UQuantContext):
        pass


    # Enter a parse tree produced by FODTLParser#eQuant.
    def enterEQuant(self, ctx:FODTLParser.EQuantContext):
        pass

    # Exit a parse tree produced by FODTLParser#eQuant.
    def exitEQuant(self, ctx:FODTLParser.EQuantContext):
        pass


    # Enter a parse tree produced by FODTLParser#utOperators.
    def enterUtOperators(self, ctx:FODTLParser.UtOperatorsContext):
        pass

    # Exit a parse tree produced by FODTLParser#utOperators.
    def exitUtOperators(self, ctx:FODTLParser.UtOperatorsContext):
        pass


    # Enter a parse tree produced by FODTLParser#btOperators.
    def enterBtOperators(self, ctx:FODTLParser.BtOperatorsContext):
        pass

    # Exit a parse tree produced by FODTLParser#btOperators.
    def exitBtOperators(self, ctx:FODTLParser.BtOperatorsContext):
        pass


    # Enter a parse tree produced by FODTLParser#always.
    def enterAlways(self, ctx:FODTLParser.AlwaysContext):
        pass

    # Exit a parse tree produced by FODTLParser#always.
    def exitAlways(self, ctx:FODTLParser.AlwaysContext):
        pass


    # Enter a parse tree produced by FODTLParser#snext.
    def enterSnext(self, ctx:FODTLParser.SnextContext):
        pass

    # Exit a parse tree produced by FODTLParser#snext.
    def exitSnext(self, ctx:FODTLParser.SnextContext):
        pass


    # Enter a parse tree produced by FODTLParser#sometime.
    def enterSometime(self, ctx:FODTLParser.SometimeContext):
        pass

    # Exit a parse tree produced by FODTLParser#sometime.
    def exitSometime(self, ctx:FODTLParser.SometimeContext):
        pass


    # Enter a parse tree produced by FODTLParser#until.
    def enterUntil(self, ctx:FODTLParser.UntilContext):
        pass

    # Exit a parse tree produced by FODTLParser#until.
    def exitUntil(self, ctx:FODTLParser.UntilContext):
        pass


    # Enter a parse tree produced by FODTLParser#release.
    def enterRelease(self, ctx:FODTLParser.ReleaseContext):
        pass

    # Exit a parse tree produced by FODTLParser#release.
    def exitRelease(self, ctx:FODTLParser.ReleaseContext):
        pass


