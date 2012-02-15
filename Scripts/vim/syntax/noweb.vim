" Remove any old syntax stuff hanging around
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
  w
endif
if !exists("noweb_backend")
    let noweb_backend = "tex" " this seems common
endif

if version < 600
    execute "source <sfile>:p:h/" . noweb_backend . ".vim"
else
    execute "runtime! syntax/" . noweb_backend . ".vim"

    if exists("b:current_syntax")
        unlet b:current_syntax
    endif
endif
syntax match codeChunkStart "^<<.*>>=$" display
syntax match codeChunkEnd "^@$" display
highlight link codeChunkStart Type
highlight link codeChunkEnd Type
if !exists("noweb_language")
    let noweb_language = "nosyntax"
endif

execute "syntax include @Code syntax/" . noweb_language . ".vim"
" syntax include @Code syntax/vim.vim
syntax region codeChunk start="^<<.*>>=$" end="^@$" contains=@Code containedin=ALL keepend
if exists("noweb_fold_code") && noweb_fold_code == 1
    set foldmethod=syntax
    syntax region codeChunk start="^<<.*>>=$" end="^@$" transparent fold containedin=ALL keepend
endif
