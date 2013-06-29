# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from flask import Flask, send_file, Response, request


from monitor import FileMonitor


app = Flask(__name__)

app.reloaded = {
    'filemonitor': FileMonitor()
}


@app.route('/reloaded/<path:filename>')
def send_reloaded_file(filename):
    try:
        return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assets', filename))
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
        app.reloaded['filemonitor'].watch_files(self, files)

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
