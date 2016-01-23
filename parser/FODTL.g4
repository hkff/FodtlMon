
grammar FODTL;

//-------------------------------------------------------//
//----------------- Lexer rules ------------------------//
//------------------------------------------------------//
ID        : (('a'..'z')|('A'..'Z')) (('a'..'z')|('A'..'Z')| INT | '_')*;
INT       : '0'..'9'+;
NEWLINE   : '\r'?'\n' -> channel(HIDDEN);
WS        : (' '|'\t'|'\n'|'\r')+ -> skip;
BLANK     : (' ')+;
STRING    : '"' (.)*? '"';
COMMENT   : '%' (.)*? '\n' -> channel(HIDDEN);

h_lpar    : '(';
h_rpar    : ')';
h_lbar    : '[';
h_rbar    : ']';
h_dot     : '.';
h_colon   : ':';
h_equal   : '=';

/*
true
false

Valriable  v
Constant   's'
Predicate p(Var / cts)
a And b
a Or b
Neg a
a Imply b
G a
F a
X a
a U b
a R b
Forall VD('l', 'type')
Exists
@()
*/
formula : variable NEWLINE* | constant NEWLINE* | atom NEWLINE* | true | false
        atom NEWLINE*
        | formula NEWLINE* (conjunction | disjunction | implication | equivalence) NEWLINE* formula NEWLINE*
        | negation formula NEWLINE*
        | uQuant formula NEWLINE* | eQuant formula NEWLINE*
        | formula btOperators formula NEWLINE* | utOperators formula NEWLINE*
        | h_lpar formula h_rpar NEWLINE*
        | formula NEWLINE* formula;

atom        : predicate (h_lpar (variable | constant) (',' (variable | constant))* h_rpar)?;
predicate   : ID;
variable    : ID;
constant    : '\'' ID '\'';
true        : 'true';
false       : 'false';
negation    : '~' | 'not';
conjunction : '&';
disjunction : '|';
implication : '->' |'=>';
equivalence :'<->' | '<=>';

variabledec : ID h_colon ID;
uQuant : '!' '[' variabledec ']';
eQuant : '?' '[' variabledec ']';

utOperators : always | snext | sometime;
btOperators : until | release;

always   : 'G';
snext    : 'X';
sometime : 'F';
until    : 'U';
release  : 'R';
