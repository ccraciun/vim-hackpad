"   vim-hackpad
"   -----------
"   Browse Hackpad (hackpad.com) inside Vim
"   Author:  ccraciun
"   License: MIT (see LICENSE file)
"   Version: 0.1-dev

" We need filetype plugins
filetype plugin on

au! BufRead,BufNewFile *.hackpad set filetype=hackpad

" Defaults
if !exists("g:hackpad_credential_file")
    let g:hackpad_credential_file = expand('~') . '/.hackpad.cred.json'
endif

function! HackPad(...)
    if a:0 > 0
        let g:hackpad_arg = a:1
    else
        let g:hackpad_arg = ""
    endif
    execute "edit .hackpad"
    normal! gg
endfunction

command! -nargs=* Hackpad call HackPad(<q-args>)
