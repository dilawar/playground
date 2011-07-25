% This is a test program. It test knuth graph-base library and check its
% functinality.

% If you think that something is techinically, mathematically, philosophically
% or politically incorrect, please blame is on Dilawar Singh
% <dilawar@ee.iitb.ac.in>

% Created on July 23, 2011. A lot of neuron got burnt!
\def\title{Example\_\thinspace GRAPHBASE}
@i boilerplate.w %<< Some legal stuff. PLEASE READ IT BEFORE MAKING ANY CHANGES.

@* Introducton. This is |test_program|. Ideally this should be renamed
|learn_graphbase|. So we are going to learn this Knuth's graphbase and pretend
that we are testing it.

The best introduction on how to use graphbase is in |gb_basic|, which contains
subroutines for generating and transforming various classical graphs. DO READ
THIS FILE even if you lack time or enthusiasm or both.

@ The code below should be system-independent; it should produce equivalent
result on all systems, assuming that the standard |calloc| and |cfree| functions
of \Cee\ are available. I have only tested it on linux and Cygwin. Since I am
heavily biased against Windows, I am not going to test this on Windows. 

@(test_example.c@>=
#include "gb_graph.h" /* all of the user of |gb_graph| should do this. */
@<Declarations of test  variables@>@;
@#
int main()
{
    @<Create a small graph@>;
    @<Create another small graph@>;
    @<Intersect both of them@>;
    @<Union both of them@>;
    @<Test if we get them right@>;
    printf("OK! our endevour seem to work!\n");
    exit(0);
}

@ The \Cee\ code for |gb_graph| does not have a main routine; it is just a bunch
of subroutines to be incorporated into programs at the higher label, via the
system loading routines.




