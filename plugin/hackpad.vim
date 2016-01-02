"   vim-hackpad
"   -----------
"   Browse Hackpad (hackpad.com) inside Vim
"   Author:  ccraciun
"   License: MIT (see LICENSE file)
"   Version: 0.1-dev

" We need filetype plugins
filetype plugin on

au! BufRead,BufNewFile *.hackpad set filetype=hackpad

if has('python')
    command! -nargs=1 Python python <args>
elseif has('python3')
    command! -nargs=1 Python python3 <args>
else
    echo "Hackepad.vim Error: Requires Vim compiled with +python or +python3"
    finish
endif

execute "Python import sys"
execute "python sys.path.append(r'" . expand("<sfile>:p:h")  . "')"

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

function! HackPad(...)
    if a:0 > 0
        let g:hackpad_arg = a:1
    else
        let g:hackpad_arg = ""
    endif
    execute "edit .hackpad"
    normal! gg

    execute "Python vimhackpad.main()"
endfunction

command! -nargs=* Hackpad call HackPad(<q-args>)
