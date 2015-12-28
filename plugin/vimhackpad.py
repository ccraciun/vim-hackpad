# -*- coding: utf-8 -*-

import vim
from hpad import HackpadSession


def bufwrite(string):
    b = vim.current.buffer

    # Never write more than two blank lines in a row
    if not string.strip() and not b[-1].strip() and not b[-2].strip():
        return

    # Vim must be given UTF-8 rather than unicode
    if isinstance(string, unicode):
        string = string.encode('utf-8', errors='replace')

    # Code block markers for syntax highlighting
    if string and string[-1] == unichr(160).encode('utf-8'):
        b[-1] = string
        return

    if not b[0]:
        b[0] = string
        return

    if not b[0]:
        b[0] = string
    else:
        b.append(string)


def vim_hackpad(url, key, secret):
    vim.command('edit .hackpad')
    vim.command('setlocal noswapfile')
    vim.command('setlocal buftype=nofile')

    bufwrite(' [ H ] a c k p a d')
    bufwrite(' ' + url)
    bufwrite('')

    session = HackpadSession(key, secret, url=url)
    pad_list = session.pad_list()
    if not pad_list.status_code.ok:
        print(pad_list.json())
        return

    pad_ids = session.pad_list().json()
    pads = {pad_id: session.pad_get(pad_id) for pad_id in pad_ids}
    pads = {pad_id: pad_request.content for pad_id, pad_request in pads.items()}

    for pad_id, pad in pads.items():
        lines = filter(lambda line: line, pad.split('\n'))

        bufwrite(pad_id + ':  ' + lines[0])
        if len(lines) > 1:
            bufwrite(lines[1])
        else:
            bufwrite('')
        bufwrite('')
