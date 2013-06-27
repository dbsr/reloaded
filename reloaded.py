#!/bin/env python2.7
# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013


import sys
import os

_here = os.path.dirname(os.path.realpath(__file__))
sys.path.extend([
    os.path.join(_here, 'reloaded/server'),
    os.path.join(_here, 'reloaded/server/ext')
])

from socketio.server import SocketIOServer
from gevent import monkey

monkey.patch_all()

from server import app


def start_server(host_address):
    try:
        server = SocketIOServer(host_address, app, resource='socket.io')
        server.serve_forever()
    except:
        # assume for now server is already running
        pass


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="reloaded server address", default="localhost")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--debug", type=int, help="enable debug messages")
    parser.add_argument("--show-status", type=int, default=1, help="enable / disable the reloaded status indicator")
    args = parser.parse_args()
    host_address = (args.host, args.port)
    app.debug = args.debug

    start_server(host_address)
