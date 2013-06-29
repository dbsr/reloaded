#!/bin/env python2.7
# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013


import sys
import os
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(_here, '../lib'))

import socket

from socketio.server import SocketIOServer
from gevent import monkey

monkey.patch_all()

from server import app


def start_server(host, port, hide_status, debug):
    app.debug = bool(debug)
    app.reloaded['hide_status'] = bool(hide_status)
    server = SocketIOServer((host, int(port)), app, resource='socket.io')
    print "Reloaded server started serving on: {}:{}.".format(host, port)
    try:
        server.serve_forever()
    except socket.error:
        print ("Reloaded server could not bind to port: {}. Is reloaded already"
               " running?".format(port))
        sys.exit(1)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("--port", type=int)
    parser.add_argument("--debug", type=int)
    parser.add_argument("--hide-status", type=int)
    args = parser.parse_args()

    start_server(**vars(args))
