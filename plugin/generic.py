# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os
import subprocess


class VimfoxPluginException(Exception):
    pass


class Plugin(object):
    """Use this to override the default settings and to start / stop the vimfox
    server"""

    prc = None

    # Default vimfox server settings.
    RUN_SERVER_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'server', 'run.py')
    vimfox_server_host = 'localhost'
    vimfox_server_port = 9000
    vimfox_debug = -1
    vimfox_show_status = 0

    def start_server(self):
        if not self.poll():
            self.stop_server()
        try:
            self.prc = subprocess.Popen([
                self.RUN_SERVER_PY,
                '--host', self.vimfox_server_host,
                '--port', str(self.vimfox_server_port),
                '--debug', str(self.vimfox_debug),
                '--show-status', str(self.vimfox_show_status)
            ])
        except OSError as e:
            raise VimfoxPluginException(e)

    def stop_server(self):
        # Make sure the server is (still) running.
        if not self.poll():
            try:
                self.prc.kill()
            except OSError as e:
                raise VimfoxPluginException(e)

    def poll(self):
        return self.prc.poll() if self.prc else True
