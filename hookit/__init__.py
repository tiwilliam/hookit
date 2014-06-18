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


WHITELIST = GitHub().meta().get('hooks', [])

args = docopt(__doc__)


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
            logging.error('%s: %s' % (e, data))
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
    ref = payload['ref']
    after = payload['after']
    repo = payload['repository']['name']
    branch = ref.split('/')[-1]

    jail = os.path.abspath(args['--scripts'])
    trigger = os.path.abspath('%s/%s/%s' % (jail, repo, branch))

    # Check if absolute trigger path resides in jail directory
    if not os.path.commonprefix([trigger, jail]).startswith(jail):
        logging.warning('%s: Tried to execute outside jail' % trigger)
        return

    # No action
    if not os.path.isfile(trigger):
        logging.info('%s: No such trigger' % trigger)
        return

    logging.info('%s: Executing trigger' % trigger)
    call([trigger, branch, repo, after])


def run():
    host = args['--listen']

    try:
        port = int(args['--port'])
    except ValueError:
        logging.error('Binding port must be integer')
        sys.exit(1)

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
    logging.error('Could not start server: %s' % message)
    sys.exit(1)


if __name__ == '__main__':
    run()
