# -*- coding: utf8 -*-

"""
Usage:
  githook [--scripts=<dir>] [--listen=<address>] [--port=<port>]

args:
  -v --version        Show version
  --scripts=<dir>     Where to look for hook scripts [default: .]
  --listen=<address>  Server address to listen on [default: 0.0.0.0]
  --port=<port>       Server port to listen on [default: 8000]
"""

import json
import struct
import socket
import logging
import os.path
from cgi import parse_qs

from docopt import docopt

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler


args = docopt(__doc__, version=0.1)

WHITELIST = [
    ('192.30.252.0', 22),
    ('204.232.175.64', 27)
]


def to_num(ip):
    return struct.unpack('<L', socket.inet_aton(ip))[0]


def to_netmask(ip, bits):
    return to_num(ip) & ((2L << bits - 1) - 1)


def in_network(ip, net):
    return to_num(ip) & net == net


def in_whitelist(client):
    for ip, bit in WHITELIST:
        if in_network(client, to_netmask(ip, bit)):
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
        length = int(self.headers.getheader('Content-Length'))
        data = self.rfile.read(length)

        # Parse POST data and get payload
        payload = parse_qs(data).get('payload', None)
        if not payload:
            self.send_forbidden()
            return

        payload = json.loads(payload[0])
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
    repo = payload['repository']['name']
    branch = ref.split('/')[-1]

    jail = os.path.abspath(args['--scripts'])
    trigger = os.path.abspath('%s/%s' % (repo, branch))

    # Check if absolute trigger path resides in jail directory
    if not os.path.commonprefix([trigger, jail]).startswith(jail):
        logging.warning('%s: Tried to execute outside jail' % trigger)
        return

    # No action
    if not os.path.isfile(trigger):
        logging.info('%s: No such trigger' % trigger)
        return

    logging.info('%s: Executing trigger' % trigger)
    # TODO: Execute script


def run():
    host = args['--listen']
    port = int(args['--port'])

    http = HTTPServer((host, port), HookHandler)
    http.serve_forever()


if __name__ == '__main__':
    run()