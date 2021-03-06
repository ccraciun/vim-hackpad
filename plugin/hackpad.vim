"   vim-hackpad
"   -----------
"   Browse Hackpad (hackpad.com) inside Vim
"   Author:  ccraciun
"   License: MIT (see LICENSE file)
"   Version: 0.1-dev

" We need filetype plugins
filetype plugin on

"autocmd! InsertEnter,CursorHold,BufReadCmd hackpad://*/?* call HackPadRead(expand("<amatch>"))
"autocmd! InsertLeave,BufWriteCmd hackpad://*/?* call HackPadWrite(expand("<amatch>"))
" TODO: Use hackpad/client/ios updating so we're less disruptive.
autocmd! BufReadCmd hackpad://*/?* call HackPadRead(expand("<amatch>"))
autocmd! BufWriteCmd hackpad://*/?* call HackPadWrite(expand("<amatch>"))
autocmd! BufReadCmd hackpad://*/ call HackPadList(expand("<amatch>"))

if has('python')
    command! -nargs=1 Python python <args>
elseif has('python3')
    command! -nargs=1 Python python3 <args>
else
    echo "Hackepad.vim Error: Requires Vim compiled with +python or +python3"
    finish
endif

execute "Python import sys"
execute "Python sys.path.append(r'" . expand("<sfile>:p:h")  . "')"

Python << EOF
if 'vimhackpad' not in sys.modules:
    import vimhackpad
else:
    import imp
    vimhackpad = imp.reload(vimhackpad)
EOF


" Defaults
if !exists("g:hackpad_credential_file")
    let g:hackpad_credential_file = expand('~') . '/.hackpad.cred.json'
endif

if !exists("g:hackpad_list_summary_lines")
    let g:hackpad_list_summary_lines = 3
endif


" Open Hackpad Pad or show Hackpad Pad List by URL
function! HackPad(...)
    if a:0 > 0
        let g:hackpad_url = a:1
    else
        let g:hackpad_url = ""
    endif
    execute "Python vimhackpad.load()"
endfunction

" Create a new hackpad
function! HackPadCreate(...)
    if a:0 > 0
        let g:hackpad_url = a:1
    endif
    execute "Python vimhackpad.create()"
endfunction

" Show hackpad list
function! HackPadList(...)
    if a:0 > 0
        let g:hackpad_url = a:1
    endif
    execute "Python vimhackpad.load_list()"
endfunction

function! HackPadRead(pad_uri)
    let l:winview = winsaveview()
    let g:hackpad_url = a:pad_uri
    execute "Python vimhackpad.read()"
    call winrestview(l:winview)
endfunction

function! HackPadWrite(pad_uri)
    let l:winview = winsaveview()
    let g:hackpad_url = a:pad_uri
    execute "Python vimhackpad.save()"
    call winrestview(l:winview)
endfunction

command! -nargs=* Hackpad call HackPad(<q-args>)
command! -nargs=* HackpadCreate call HackPadCreate(<q-args>)
