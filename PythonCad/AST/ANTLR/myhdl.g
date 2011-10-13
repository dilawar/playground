parser grammar myhdl;
options {
	language = Python;
	output = AST;
	ASTLabelType=CommonTree;
	// We're going to use the tokens defined in 
	toekenVocab = myhdlLexer;
}

tokens {
	COMBINE;
	DEFINE;
	DERIVATIVE;
	FUNCTION;
	POLYNOMIAL;
	TERM;
}

prog		: ( stat {print $stat.tree.toStringTree()} )+;


stat		: 	expr NEWLINE		-> expr
		|	ID  '=' expr NEWLINE -> ^('=' ID expr)
		|	NEWLINE			->
		;
		
expr		: 	multExpr (('+'^|'-'^) multExpr)*
		;

multExpr	:	atom('*' ^ atom)*
		;

atom 	:	INT
		| 	ID
		|	'('  !expr ')'!
		;
		
ID 		: 	('a'..'z' | 'A'..'Z')+
		;

INT		: 	'0'..'9'+
		;

NEWLINE	:	'\r' ? '\n'
		;

WS		:	(' '|'\t'|'\n'|'\r')+{self.skip()}
		;
