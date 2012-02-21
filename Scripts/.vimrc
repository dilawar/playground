" All system-wide defaults are set in $VIMRUNTIME/debian.vim (usually just
" /usr/share/vim/vimcurrent/debian.vim) and sourced by the call to :runtime
" you can find below.  If you wish to change any of those settings, you should
" do it in this file (/etc/vim/vimrc), since debian.vim will be overwritten
" everytime an upgrade of the vim packages is performed.  It is recommended to
" make changes after sourcing debian.vim since it alters the value of the
" 'compatible' option.

" This line should not be removed as it ensures that various options are
" properly set to work with the Vim-related packages available in Debian.
runtime! debian.vim

" Uncomment the next line to make Vim more Vi-compatible
" NOTE: debian.vim sets 'nocompatible'.  Setting 'compatible' changes numerous
" options, so any other options should be set AFTER setting 'compatible'.
"set compatible

" Vim5 and later versions support syntax highlighting. Uncommenting the
" following enables syntax highlighting by default.
if has("syntax")
  syntax on
endif

" If using a dark background within the editing area and syntax highlighting
" turn on this option as well
"set background=dark

" Uncomment the following to have Vim jump to the last position when
" reopening a file
if has("autocmd")
  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif
endif

" Uncomment the following to have Vim load indentation rules and plugins
" according to the detected filetype.
if has("autocmd")
  filetype plugin indent on
endif

" The following are commented out as they cause vim to behave a lot
" differently from regular Vi. They are highly recommended though.
set showcmd		" Show (partial) command in status line.
set showmatch		" Show matching brackets.
set ignorecase		" Do case insensitive matching
set smartcase		" Do smart case matching
set incsearch		" Incremental search
set autowrite		" Automatically save before commands like :next and :make
set hidden             " Hide buffers when they are abandoned
set mouse=a		" Enable mouse usage (all modes)
set number
set ruler
set hlsearch
set autoindent
set smartindent
set tabstop=3
set expandtab
set shiftwidth=1
set textwidth=80
set wrap
set iskeyword+=_
set spell spelllang=en
set dictionary+=/usr/share/dict/words

" c-support
set errorformat^=%-GIn\ file\ included\ %.%#
let $VIMRUNTIME="/home/dilawar/Works/MyPublic/Scripts/vim"

colorscheme peachpuff
imap jj <Esc>
imap qq <C-P>
imap ww <C-N>
imap ddd <C-X><C-K>

au BufRead,BufNewFile *.snw set filetype=noweb
let g:haddock_browser="/usr/bin/firefox"
let g:alternateExtensions_C="H,hh,h"
let g:alternateExtensions_hh="C,cc,cpp,c"
let g:SuperTabDefaultCompletionType="context"
:highlight Pmenu guibg=brown gui=bold

"let g:SuperTabDefaultCompletionType="context"
let noweb_backend="tex"
let noweb_language="haskell"
let noweb_fold_code=1

"copy current visual selection to ~/.vbuf
vmap <leader>y :w! ~/.vbuf<cr>
"copy current line to the buffer file if no visual selection
nmap <leader>y :.w! ~/.vbuf<cr>
"paste the content of the buffer file
nmap <leader>p :r ~/.vbuf<cr> 
