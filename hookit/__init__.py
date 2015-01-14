# -*- coding: utf8 -*-

"""
Usage:
  hookit [--scripts=<dir>] [--listen=<address>] [--port=<port>]

args:
  --scripts=<dir>     Where to look for hook scripts [default: .]
  --listen=<address>  Server address to listen on [default: 0.0.0.0]
  --port=<port>       Server port to listen on [default: 8000]
"""

import sys
import json
import socket
import logging
import os.path
from subprocess import call

from docopt import docopt
from github3 import GitHub
from ipaddress import ip_address, ip_network

try:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler

logger = logging.getLogger('hookit')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

VERSION = '0.9.0'

WHITELIST = GitHub().meta().get('hooks', [])


def in_whitelist(client_ip):
    for ip in WHITELIST:
        if ip_address(u'%s' % client_ip) in ip_network(ip):
            return True
    return False


class HookHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_forbidden()

    def do_POST(self):
        # Reject all requests from non-Github IPs
        if not in_whitelist(self.client_address[0]):
            self.send_forbidden()
            return

        # Read POST data
        length = int(self.headers.get('Content-Length'))
        data = self.rfile.read(length).decode("utf-8")

        # Parse POST data and get payload
        try:
            payload = json.loads(data)
        except ValueError as e:
            logger.error('%s: %s' % (e, data))
            self.send_forbidden()
            return

        if 'zen' in payload and 'ref' not in payload:
            self.send_ok()
            return

        hook_trigger(payload)
        self.send_ok()

    def send_ok(self):
        self.send_response(200)
        self.end_headers()

    def send_forbidden(self):
        self.send_response(403)
        self.end_headers()


def hook_trigger(payload):
    owner = payload['repository']['owner']['name']
    repository = payload['repository']['name']
    branch = payload['ref'].split('/')[-1]
    commit = payload['after']

    jail = os.path.abspath(docopt(__doc__)['--scripts'])

    triggers = [
        os.path.abspath('%s/%s' % (jail, owner)),
        os.path.abspath('%s/%s/%s' % (jail, owner, repository)),
        os.path.abspath('%s/%s/%s/%s' % (jail, owner, repository, branch)),
    ]

    for trigger in triggers:
        # Check if absolute trigger path resides in jail directory
        if not os.path.commonprefix([trigger, jail]).startswith(jail):
            logger.warning('Tried to execute script outside jail: %s' % trigger)
            break

        # No action
        if not os.path.isfile(trigger):
            continue

        logger.debug('Executing %s' % trigger)
        call([trigger] + [
            '--owner=%s' % owner,
            '--branch=%s' % branch,
            '--repository=%s' % repository,
            '--commit=%s' % commit,
        ])
        break


def run():
    args = docopt(__doc__)
    host = args['--listen']

    try:
        port = int(args['--port'])
    except ValueError:
        logger.error('Binding port must be integer')
        sys.exit(1)

    logger.info('Starting hookit %s', VERSION)
    logger.info('Now listening for webhooks on http://%s:%s...' % (host, port))

    try:
        http = HTTPServer((host, port), HookHandler)
        http.serve_forever()
    except (socket.gaierror, socket.error) as e:
        startup_error(e.strerror.capitalize())
    except OverflowError as e:
        startup_error('Port must be in interval 0-65535')
    except KeyboardInterrupt:
        print('')
        sys.exit(0)


def startup_error(message):
    logger.error('Could not start server: %s' % message)
    sys.exit(1)
