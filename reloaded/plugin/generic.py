# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os
import subprocess
from functools import wraps


class ReloadedPluginException(Exception):
    '''Subclass this to implement a editor specific error handler.'''
    pass


def reloader_error_handler(m):
    @wraps(m)
    def wrapper(self, *args, **kwargs):
        try:
            m(self, *args, **kwargs)
        except ReloadedPluginException as e:
            if self.error_handler:
                self.error_handler(e)
            else:
                raise
    return wrapper


class Plugin(object):
    """Use this to override the default settings and to start / stop the reloaded
    server"""

    prc = None

    # Should be a function / lambda accepting two arguments (self, e).
    error_handler = None

    # Default reloaded server settings.
    RUN_SERVER_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'server', 'run.py')
    reloaded_host = 'localhost'
    reloaded_port = 9000
    reloaded_debug = 0
    reloaded_show_status = 1

    @reloader_error_handler
    def start_server(self, restart=False):
        if not self.poll():
            if not restart:
                return
            self.stop_server()

        try:
            self.prc = subprocess.Popen([
                self.RUN_SERVER_PY,
                '--host', self.reloaded_host,
                '--port', str(self.reloaded_port),
                '--debug', str(self.reloaded_debug),
                '--show-status', str(self.reloaded_show_status)
            ])
        except OSError as e:
            raise ReloadedPluginException(e)

    @reloader_error_handler
    def stop_server(self):
        # Make sure the server is (still) running.
        if not self.poll():
            try:
                self.prc.kill()
            except OSError as e:
                raise self.error_handler(e)

    def poll(self):
        return self.prc.poll() if self.prc else True

    @reloader_error_handler
    def debug(self):
        raise ReloadedPluginException('lol')
