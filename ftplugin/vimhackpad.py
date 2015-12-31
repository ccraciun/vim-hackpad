# -*- coding: utf-8 -*-

import json
import vim
from hackpad import HackpadSession, parse_url, padid_from_path


PAD_TYPE_TO_VIM_FILETYPE = {
        'html': 'html',
        'md': 'markdown',
        'txt': 'text',
        'native': 'html',
        }

# Keep a hackpad session object up.
session = None


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


def main():
    url = vim.eval("g:hackpad_arg")
    parsed = parse_url(url)
    netloc = parsed.netloc

    cfgfile = vim.eval('g:hackpad_credential_file')

    with open(cfgfile) as f:
        config = json.load(f)
        key = config[netloc]['--key']
        secret = config[netloc]['--secret']

    session = HackpadSession(key, secret, url=url)
    if parsed.path not in ('', '/'):
        print('Got path %s' % parsed.path)
        padid = padid_from_path(parsed.path)
        show_pad(session, padid)
    else:
        show_list(session)


def show_pad(session, padid, fmt='md'):
    vim.command('edit %s.hackpad' % padid)
    vim.command('%d')
    vim.command('setlocal noswapfile')
    vim.command('setlocal buftype=nofile')

    print("Showing pad: %s" % padid)
    pad = session.pad_get(padid, data_format=fmt)
    if not pad.ok:
        print("Hackpad.vim error fetching pad: %s" % pad.content)

    for line in pad.content.split("\n"):
        print(line)
        bufwrite(line)

    vim.command('set syntax=%s' % PAD_TYPE_TO_VIM_FILETYPE[fmt])


def show_list(session):
    vim.command('edit .hackpad')
    vim.command('setlocal noswapfile')
    vim.command('setlocal buftype=nofile')

    bufwrite(' ┌───┐')
    bufwrite(' │ H │ a c k p a d (' + netloc + ')')
    bufwrite(' └───┘')
    bufwrite('')

    pad_list = session.pad_list()
    if not pad_list.ok:
        print("Hackpad.vim error fetching pad list: %s" % pad_list.content)
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
