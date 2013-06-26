# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os
import threading

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from flask import Flask, send_file, Response, request

app = Flask(__name__)

app.reloaded = {}


@app.route('/reloaded/<path:filename>')
def send_reloaded_file(filename):
    app.logger.info(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', filename))
    try:
        return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', filename))
    except:
        return Response(':(', status=404)


class ReloadedNamespace(BaseNamespace):
    sockets = {}

    def initialize(self):
        self.logger = app.logger
        self.log('socket initialized')
        self.sockets[id(self)] = self

        return True

    def log(self, msg):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, msg))

    def disconnect(self, *args, **kwargs):
        self.log("connection lost")
        if id(self) in self.sockets:
            del self.sockets[id(self)]
            self.emit('disconnect')
        app.reloaded['ready'] = True

    def on_settings(self):
        self.log("processing settings request.")
        self.emit("settings", {"debug_mode": app.debug, "hide_status": app.reloaded['hide_status']})

    def on_watch_files(self, files):
        self.log("new watch files: " + ", ".join(files))
        app.reloaded['watch_files'] = files
        init_watch()

        return True

    @classmethod
    def socketio_send(self, event, data):
        app.logger.info("emit {} => {}.".format(event, data))
        for ws in self.sockets.values():
            ws.emit(event, data)


@app.route('/socket.io/<path:remaining>')
def socketio(remaining):
    try:
        socketio_manage(request.environ, {'/ws': ReloadedNamespace}, request)
    except:
        app.logger.error("Socket Error.", exc_info=True)

    return Response()


@app.route('/debug')
def debug():
    return Response("""
            <!DOCTYPE html>
        <html>
        <head>
            <title></title>
            <meta charset="utf-8" />
        </head>
        <body>
            <script id="reloaded-script" rel="text/javascript" src="http://localhost:9000/reloaded/reloaded.js"></script>
        </body>
        </html>""")


t_event = None


def init_watch():
    global t_event
    try:
        t_event.set()
    except:
        pass
    if not app.reloaded['watch_files']:
        return
    t_event = threading.Event()
    t = threading.Thread(target=watch, args=(t_event,))
    t.start()


def watch(stop_event):
    mtimes = {}
    while not stop_event.is_set():
        for f in app.reloaded['watch_files']:
            if not os.path.exists(f):
                print "could not stat: {!r}.".format(f)
                continue
            old_mtime = mtimes.get(f)
            new_mtime = os.stat(f).st_mtime
            if old_mtime and old_mtime != new_mtime:
                ReloadedNamespace.socketio_send('reload', f)
            mtimes[f] = os.stat(f).st_mtime
        stop_event.wait(1)
