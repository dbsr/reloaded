# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

import os
import threading


class FileMonitor(object):

    def watch_files(self, namespace, files):
        self.namespace = namespace
        self.files = {}
        for f in files:
            if not os.path.isfile(f):
                print "could not stat: {!r}.".format(f)
                continue
            self.files[f] = os.stat(f).st_mtime
        self.init_watch()

    def init_watch(self):
        if not self.files:
            return
        try:
            self.stop_event.set()
        except:
            pass
        self.stop_event = threading.Event()
        t = threading.Thread(target=self.watch, args=(self.stop_event,))
        t.start()

    def kill(self):
        try:
            self.stop_event.set()
        except:
            pass

    def watch(self, stop_event):
        while not stop_event.is_set():
            for f, mtime in self.files.items():
                new_mtime = os.stat(f).st_mtime
                if new_mtime and mtime != new_mtime:
                    self.namespace.socketio_send('reload', f)
                self.files[f] = os.stat(f).st_mtime
            stop_event.wait(1)
