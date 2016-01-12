# -*- coding: utf-8 -*-

import json
import vim
from hackpad import HackpadSession, parse_url
from itertools import repeat, chain, islice

session = None

PAD_TYPE_TO_VIM_SYNTAX = {
        'html': 'html',
        'md': 'markdown',
        'txt': 'text',
        'native': 'html',
        }
VIM_SYNTAX_TO_PAD_TYPE = {v: k for k, v in PAD_TYPE_TO_VIM_SYNTAX.items()}


def bufwrite(string, squash_repeated_empty_lines=True):
    b = vim.current.buffer

    # Never write more than two blank lines in a row
    if squash_repeated_empty_lines:
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


def load():
    url = vim.eval("g:hackpad_url")
    hpad_cred_file = vim.eval("g:hackpad_credential_file")
    key, secret = __get_credentials_for_url(url, hpad_cred_file)

    session = HackpadSession(key, secret, url=url)
    if not session.padid:
        show_list(session)
    else:
        read(url)


def read(url=None):
    url = url or vim.eval("@%")
    hpad_cred_file = vim.eval("g:hackpad_credential_file")
    key, secret = __get_credentials_for_url(url, hpad_cred_file)

    session = HackpadSession(key, secret, url=url)
    # TODO(cosmic): Need a g:hackpad_pad_format
    __setup_buffer(session, session.padid, fmt='md')

    if refresh_pad(session, session.padid):
        vim.command('set nomodified')


def refresh_pad(session, padid, fmt='md'):
    req = session.pad_get(padid, data_format=fmt)
    if __handle_req_error(req): return False

    lines = req.content.split("\n")
    vim.current.buffer[:] = lines
    return True


def save(url=None):
    url = url or vim.eval("@%")
    hpad_cred_file = vim.eval("g:hackpad_credential_file")
    key, secret = __get_credentials_for_url(url, hpad_cred_file)

    # TODO(cosmic): Here is probably where we need to fetch and see if hackpad has been changed.
    session = HackpadSession(key, secret, url=url)
    if not session.padid:
        print "Can't save pad list."
        return
    else:
        fmt = VIM_SYNTAX_TO_PAD_TYPE[vim.eval("&syntax")]
        if save_pad(session, session.padid, fmt):
            vim.command('set nomodified')


def save_pad(session, padid, fmt='md'):
    b = vim.current.buffer
    content = '\n'.join(b)

    req = session.pad_put(padid, content, data_format=fmt)
    if __handle_req_error(req): return False
    return True


def __get_credentials_for_url(url, cred_fname):
    parsed = parse_url(url)
    netloc = parsed.netloc

    with open(cred_fname) as f:
        config = json.load(f)
        key = config[netloc]['key']
        secret = config[netloc]['secret']

        return key, secret


def __setup_buffer(session, padid=None, fmt=None):
    bufname = 'hackpad://{}/{}'.format(session.parsed_url.netloc,
                                              padid or '')
    if bufname is not vim.eval('@%'):
        vim.command('silent edit! {}'.format(bufname))

    if padid:
        vim.command('setlocal swapfile')
        vim.command('setlocal filetype=hackpad')
        vim.command('silent preserve') # in case we go offline
    else:
        vim.command('setlocal noswapfile')
        vim.command('setlocal buftype=nofile')
        vim.command('setlocal filetype=hackpad_list')

    if fmt:
        vim.command('setlocal syntax={}'.format(PAD_TYPE_TO_VIM_SYNTAX[fmt]))


def __handle_req_error(req):
    if not req.ok:
        try:
            json_resp = req.json()
        except ValueError:
            print("Hackpad.vim error talking to hackpad: %s" % req.reason)
            return req.reason
        else:
            print("Hackpad.vim error talking to hackpad: %s" % json_resp['error'])
            return json_resp['error']
    return None


def show_list(session):
    __setup_buffer(session, fmt='md')
    vim.command('%d')

    bufwrite(' ┌───┐')
    bufwrite(' │ H │ a c k p a d (' + session.url + ')')
    bufwrite(' └───┘')
    bufwrite('')

    req = session.pad_list()
    if __handle_req_error(req): return

    pad_ids = req.json()
    pads = {pad_id: session.pad_get(pad_id) for pad_id in pad_ids}
    pads = {pad_id: pad_request.content for pad_id, pad_request in pads.items()}

    for pad_id, pad in pads.items():
        summary_stop_line = 1 + int(vim.eval("g:hackpad_list_summary_lines"))
        lines = filter(lambda line: line, pad.split('\n'))
        summary = islice(chain(lines, repeat('')), 1, summary_stop_line)

        bufwrite('[{}](hackpad://{}/{})'.format(lines[0], session.parsed_url.netloc, pad_id))
        for line in summary:
            bufwrite(line)
        bufwrite('')
