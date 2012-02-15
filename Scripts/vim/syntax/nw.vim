" Vim syntax file
" Language:		NOWEB
" Author:		Dirk Baechle <dl9obn@darc.de>
" Date:			2002-10-31
" Version:		1.1
" Derived from: 	cweb.vim by Andreas Scherer

" History
"
" v1.1: Corrected `current_syntax = "noweb"' to
"                 `current_syntax = "nw"'
"
" v1.0: Initial version

" NOWEB is a collection of tools for "Literate Programming". 
" Unlike WEB or CWEB it is not bound to a specific programming
" language like PASCAL or C.
" For more informations about NOWEB, the sources or binary distributions
" have a look at 
"
" http://www.eecs.harvard.edu/~nr/noweb
"

" For informations about "Literate Programming" in general
"
" http://www.literateprogramming.com
"
" could be a place to start.
"

" Remove any old syntax stuff hanging around
syntax clear

" Like in CWEB, a NOWEB source file is treated as a TeX file
" including code chunks in between.
source <sfile>:p:h/tex.vim

" The reference to a chunk of code in another code chunk.
syntax match nowebCodeRef contained /<<.>>\|<<[^ ].*[^ ]>>/

" The code text within a code chunk.
syntax region nowebCodeBody contained start=/>>=.\|>>=$/lc=3 end=/^@ \|^@$/me=e-3 contains=nowebCodeRef

" NOWEB code chunks are defined by <<chunk_name>>=
" and ended by the next "@" (not a "@@"!) in the first column of a line.
syntax region nowebCode start=/<<.>>=\|<<[^ ].*[^ ]>>=/ end=/^@ \|^@$/me=e-3 contains=nowebCodeBody

" Here, we mark the beginning of a new text chunk.
syntax match nowebStartText /^@ \|^@$/

if !exists("did_noweb_syntax_inits")
  let did_noweb_syntax_inits = 1
  " The default methods for highlighting. Can be overridden later.
  hi link nowebCodeRef Type
  hi link nowebCodeBody Comment
  hi link nowebCode Statement
  hi link nowebStartText Constant
endif

let b:current_syntax = "nw"

" vim: ts=8
