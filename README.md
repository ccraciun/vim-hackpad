# vim-hackpad

Browse and use [hackpad](http://hackpad.com) inside Vim!

Heavily inspired from [vim-reddit](https://github.com/joshhartigan/vim-reddit),
[vim-hackernews](https://github.com/ryanss/vim-hackernews) and hoping to be more like
[CoVim](https://github.com/FredKSchott/CoVim) in the future.

## usage

Set g:hackpad_credential_file to point to a file holding your hackpad
credentials. Default is `~/.hackpad.cred.json'. Format is:

{
  "pad_domain.hackpad.com": {
    "key": "key",
    "secret": "secret",
    "url": "https://pad_domain.hackpad.com/",
    "default": true
  }
}

To open a listing of pads, use ed command
    :Hackpad https://pad_domain.hackpad.com/
To open a specific pad, use ed command
    :Hackpad https://pad_domain.hackpad.com/pad_id
Or open a new buffer
    :edit hackpad://pad_domain.hackpad.com/pad_id

## installation

pip install requests-oathlib is needed.

## TODO

* Drop dependency on requests_oauthlib
* Finish implementing everything
