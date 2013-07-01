#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import sys
import os
import socket
import argparse

_here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(_here, 'lib'))
print _here

from socketio.server import SocketIOServer
from gevent import monkey

monkey.patch_all()

from reloaded.server import app


def start_server(host, port, hide_status, debug):
    print "server initiating..."
    app.debug = bool(debug)
    app.reloaded['hide_status'] = bool(hide_status)
    server = SocketIOServer((host, int(port)), app, resource='socket.io')
    print "listening on: '{}:{}'".format(host, port)
    try:
        server.serve_forever()
    except socket.error:
        print ("Reloaded server could not bind to: '{}:{}' \nIs reloaded already"
               " running?".format(host, port))
        sys.exit(1)
    except KeyboardInterrupt:
        print "\nShutting down server..."
        try:
            app.reloaded['filemonitor'].kill()
        except:
            pass
        sys.exit(0)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--debug", action="store_true", help="be more verbose")
    parser.add_argument("--hide-status", action="store_true", help="hide the reloaded status indicator")

    args = vars(parser.parse_args())
    start_server(**args)
