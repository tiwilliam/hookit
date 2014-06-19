# Bind GitHub WebHooks to actions

    Usage:
      hookit [--scripts=<dir>] [--listen=<address>] [--port=<port>]
    
    Options:
      -v --version        Show version
      --scripts=<dir>     Where to look for hook scripts [default: .]
      --listen=<address>  Server address to listen on [default: 0.0.0.0]
      --port=<port>       Server port to listen on [default: 8000]

## Execute scripts in any language

On webhook the server will try to execute a script located at `<scripts>/<repository>/<branch>`.
The script will run with arguments containing repository, branch and commit hash. An example script may look like:

    #!/usr/bin/env python

    import sys
    from subprocess import call

    branch = sys.argv[1]
    repo = sys.argv[2]

    message = 'You have changes in the %s branch of %s' % (branch, repo)
    call(['/usr/bin/say', message])

## Installation

This package is availiable on Python Package Index

    pip install hookit

## Security

The server will only accept requests from GitHub's trusted servers and run scripts from an jailed directory.

GitHub's trusted servers will be updated on start using their [meta endpoint](https://api.github.com/meta).
