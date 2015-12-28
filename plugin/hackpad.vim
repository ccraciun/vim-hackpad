if !has('python')
  echo 'vim-hackpad requires Vim compiled with +python!'
  finish
endif

execute 'python import sys'
execute "python sys.path.append(r'" . expand("<sfile>:p:h")  . "')"
execute "python from vimhackpad import vim_hackpad"

command! -nargs=* Hackpad python vim_hackpad(<f-args>)

au! BufRead,BufNewFile *.hackpad set filetype=hackpad
