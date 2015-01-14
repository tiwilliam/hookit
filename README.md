# Bind GitHub WebHooks to actions

    Usage:
      hookit [--scripts=<dir>] [--listen=<address>] [--port=<port>]

    Options:
      -v --version        Show version
      --scripts=<dir>     Where to look for hook scripts [default: .]
      --listen=<address>  Server address to listen on [default: 0.0.0.0]
      --port=<port>       Server port to listen on [default: 8000]

## Execute scripts in any language

On recieving a webhook the server will try to execute a script located
at  `.../<owner>/<repository>/<branch>`, hookit will pass some arguments
with useful data. An example script may look like:

    #!/usr/bin/env python

    import argparse
    from subprocess import call

    parser = argparse.ArgumentParser(description='Hook some hooks.')
    parser.add_argument('--repository')
    parser.add_argument('--branch')
    args = parser.parse_args()

    message = 'You have changes in the %s branch of %s' % (args.branch, args.repository)
    call(['/usr/bin/say', message])

## Catch all events

It's also possible to listen for all push events in an organisation
or repository. Just place your hook script at the level you are
interested of (eg. `.../<owner>/<repository>` or `.../<owner>`).

## Script arguments

Here is a complete list of all arguments passed to scripts:

    .../tiwilliam/hookit
        --owner=tiwilliam
        --branch=master
        --repository=hookit
        --commit=a3a707700d845919178c72cd266ffc28d882c380

## Installation

This package is availiable on Python Package Index

    pip install hookit

## Security

The server will only accept requests from GitHub's trusted servers and
run scripts from an jailed directory.

GitHub's trusted servers will be updated on start using
their [meta endpoint](https://api.github.com/meta).
