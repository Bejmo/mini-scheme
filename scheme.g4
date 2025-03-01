// Gramàtica per expressions senzilles
grammar scheme;

// Root
root : expr+ ;

// Expression
expr : '(' expr* ')'                                                  # llistaEval
     | '\'' '(' expr* ')'                                              # llista
     | ('+' | '-' | '*' | '/' | '<' | '>' | '>=' | '<=' | '=' | '<>') # opBinari
     | NUM                                                            # numero
     | WORD                                                           # variable
     | BOOL                                                           # boolea
     | STRING                                                         # string
     ;

// Tokens
WORD : [a-zA-Z\u0080-\u00FF?][a-zA-Z0-9\u0080-\u00FF?-]* ;
STRING : '"' (~["])* '"' ;
BOOL : ('#t'|'#f') ;
NUM : '-'?[0-9]+ ;
WS  : [ \t\n\r]+ -> skip ;

COMMENTS : ';' (~[\n])* ('\n' | EOF) -> skip ;