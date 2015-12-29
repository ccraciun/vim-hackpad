"   vim-hackpad
"   -----------
"   Browse Hackpad (hackpad.com) inside Vim
"   Author:  ccraciun
"   License: MIT (see LICENSE file)
"   Version: 0.1-dev



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


" Load main page.
execute "Python vimhackpad.main()"


noremap <buffer> o :Python vimhackpad.openpad()<cr>
