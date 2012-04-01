%    construct_bdd.snw
%    
%    Description:  This is a stand-alone program to construct a
%    Reduced order Binary Decision diagram. It is written in
%    literate style. 
%    
%    Version:  1.0
%    Created:  Wednesday 03 August 2011 08:26:02  IST
%   Revision:  none
%   Compiler:  gcc
%
%     Author:  (c) 2011, Dilawar Singh, dilawar@ee.iitb.ac.in
%  Institute:  Indian Institute of Technology Bombay
% 
%% RELEASED UNDER GNU-GPL

\title{Binary Decision Diagrams}
\author{Dilawar Singh}
\maketitle

\paragraph{1}

Reduced Order Binary  Decision  Diagrams  (ROBDD),  usually  called  Binary
decision Diagrams  (BDD),  is  a  propotional  directed  acyclic  graph  (a
data-structure) which can be used to represent a boolean function.   For  a
given ordering of variables, representation of a boolean function in  terms
of a BDD is guarenteed to be unique \ref{Byrant}

In this implementation, we want to create a BDD. The expression or function
or propotional logic is given to  us  in  a  txt  file  with  a  particular
ordering on variables.  The ordering of variables in very  important  since
size of the BDD for a  given  function  depends  on  the  ordering  of  the
variables.  We should  read  this  file  and  save  it  in  an  appropriate
data-structure.


\paragraph{2}

Binary Decision Diagram (BDD) essentially are \textbf{binary decision dag},
a binary tree with shared binary tree, a directed acyclic graph (dag) in
which exactly two distinguished arcs emanate from every non-sink node.

In computer memory, a bdd node can is represented like following.

\begin{verbatim}
        --------------------------------------
        |            |           |           |
        |    V       |   LO      |    HI     |
        |            |           |           |
        --------------------------------------
\end{verbatim}
where 'V' holds the name (or index) of the variable, 'LO' and 'HI' are
pointer to another node or sink.

BDD has two properties. It is \textbf{ordered} i.e. if a LO or HI node from
\textcircled{i} points to another node \textcircled{j} then $i \le j$.
Thus, in particular, no variable $x_j$ will ever be queried twice when
function is evaluted.  Also BDD must be \textbf{reduced} in the sense that
it does not waste space. This means that branch node's LO and HI must never
be equal, and no two nodes in BDD representation should have same triple of
value(V, LO, HI).

So basically, a BDD is a abstract liked list with some constrained specified on
them.

\paragraph{3}

Before we get into BDD stuff, let me discuss memory management. We will use
a very big array [[memBdd]]. Lower part of this array will have the BDD
nodes (32 bits each) and uper part will contain pages (4096 bytes each) to
keep hash of variables and cache of computer results.

\begin{verbatim}

    mem+memsize-1 ----> ------------     ^
                        |           |    |     
                        |           |    |
                        |           |    |
                        |           |    |
                        |           |    |
                        |           |    |
                        |           |    
                        |           |    PAGES
                        |           |    
                        |           |    |
                        |           |    |
                        ------------- <----- pageptr
                        |           |
         nodeptr -----> -------------    ^
                        |           |    |
                        |           |   BDD NODES
                        |           |    |
                        |           |    |
              mem ----> ------------- 

\end{verbatim}
 
Data is stored here with a type called [[addr]] which is simply a 32
bit unsigned integer. The [[addr_]] macro converts an ordinary pointer to
[[addr]].

<<GlobalVariables>>=
typedef unsigned int addr;
#define addr_ (p) ((addr)(size_t)(p))
@ %def addr_ addr


To build this infrastructure, we need to define followings.

<<GlobalVariables>>=
#define logPageSize        12
#define memSize            (1<<29)
#define pageSize           (1<<logPageSize) /* bytes per page */
#define pageMask           (pageSize-1)
#define pageInts           pageSize/sizeof(int)
#define bddNode_ (a)       ((bddNode*)(size_t)(a))
#define page_ (a)          ((page*)(size_t)(a))


typedef struct nodeStruct
{
    addr lo, hi;
    int varRef;
    unsigned int index; /* variable id followed by random bits. */
} bddNode;

typedef struct pageStruct
{
    addr dat[pageInts];
} page;

@ %def bddNode nodeStruct page 
  %def nodeStruct logPageSize memSize pageSize pageMask pageInts  bddNode_ page_     

@ \paragraph{The BDD file}

User should pass  BDD expression in a text file with a variable ordering.
If a variable ordering is not given then a ordering is derived by looking
at the order in which variable appears in the BDD expression. BDD
expression can be nested.

Following are the characer codes for logical function.

\begin{verbatim}
            && ::= and
            || ::= or
            !  ::= not (unary)
            !& ::= nand
            !| ::= nor
            ~| ::= xor

\end{verbatim}

The primary BDD expression will have the tag BDD0. All other BDD expression
should have non-zero integer appended to string 'BDD' e.g. BDD1, BDD2 etc.
Any BDD expression can nest other BDD expressions such as BDD1 ::= (or BDD2
BDD3). No BDDX expression is allowed to nest BDD0 as a sub-expression. All
BDD expression must be in reverse-polish notation.

For example, a typical BDD file would look like this. It is left to the
user to specify consistent ordering with BDD subexpressions. However, a
suitable algorithm should be implemented to compute the ordering of the
variables.

\begin{verbatim}
# This is a comment line.
# One should give a variable ordering (optional)
BDD1 ::= (|| x2 x3)
BDD2 ::= (&& (! BDD1) x1)
BDD0 ::= (~| BDD1 BDD2)
\end{verbatim}

Function [[readBDDFile]] should read this file and create an appropriate
data-structure [[bddExpression]].

<<IncludesHeaderFiles>>=
#include	<stdio.h>
#include	<string.h>
#include	<error.h>
#include	<ctype.h>
#include	<stdlib.h>
#include	<stdarg.h>
#include	"construct_bdd.h"

@
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\paragraph{The header file}

Although function definitons and variables declarations are generally kept
in a header file separately of source file, in this literate program we use
a single [[noweb]] file. It will maintain the readability. However two
files will be created by [[notangle]].  One is a source file and other is a
header file [[Header]] as to be consistant with general coding practise.

<<Header>>=
<<License>>
#ifndef CONSTRUCT_BDD_H
#define CONSTRUCT_BDD_H
<<GlobalVariables>>
<<Definitions>>
#endif


@
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\paragraph{Definitions}

<<Definitions>>=

/* Function to read my BDD expression file. */
struct bddExpression* readBDDFile (char*);

@
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\paragraph{Global Variables}

In global variables we have [[bddExpression]] and [[bddNode]] structures.


<<GlobalVariables>>=

#define FILEPATH_MAX    100
#define NAME_MAX        100
#define VAR_SIZE        4        /* variable in BDD expr */
#define OP_SIZE         4        /* Binary operation in BDD expr */
#define ZERO            0
#define ONE             1

/* This won't possibly use. */

struct bddExpression             /* structure for binary expressions. */
{
    struct bddExpression *lBddExpr;
    struct bddExpression *rBddExpr;
    char* binOp;
    char *lVar, *rVar; 
};

@ %def bddExpression 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@\paragraph{Functions}

@\paragraph{Read BDD File}

Function [[readBDDFile]] should take [[filePath]] as argument and return
a data-structure containing BDD-expression. 

<<readBDDFile>>=
struct bddExpression* readBDDFile (char* pfile)
{
    return NULL;
}

@
%%
<<Functions>>=
<<readBDDFile>>

@
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\paragraph{The main function}
<<TheMainFunction>>=
int main (int argc, char** argv)
{
    <<LocalVariable>>
    <<CheckTheCommandLine>>
    <<InitializeEverything>>

    printf("Hello class!\n");
    return EXIT_SUCCESS;
}

@
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\paragraph{Structure of the program}

<<*>>=
<<License>>
<<IncludesHeaderFiles>>
<<Functions>>
<<TheMainFunction>>

@
\paragraph{License and other stuff}
<<License>>=
/* (c) 2011 GNU GPL
 * Dilawar Singh 
 * Email : dilawar@ee.iitb.ac.in
 * Indian Institute of Technology Bombay
 */


