#!/usr/bin/env python
#coding=utf-8

#
# Copyright (C) 2014 - S. Zachariah Sprackett <zac@sprackett.com>
#
# Released under the same terms as Sensu (the MIT license); see LICENSE
# for details.
"""
Primitives for implementing a Sensu handler
"""
import os
import sys
import atexit
import requests

import sensu_plugin.utils


class SensuHandler(object):
    def __init__(self):
        self.event = None
        atexit.register(self._exitfunction)

    def handle(self):
        print('ignoring event -- no handler defined')

    def filter(self):
        self.filter_disabled()
        self.filter_repeated()
        self.filter_silenced()
        self.filter_dependencies()

    def bail(self, msg):
        print("%s: %s/%s" %
              (msg, self.event['client']['name'], self.event['check']['name']))
        os._exit(0)

    def api_request(self, method, path, block):
        s = requests.Session()
        s.auth = (settings['api']['user'], settings['api']['password'])
        url = "%s:%s%s" % (settings['api']['host'], settings['api']['port'],
                path)
        req = request.Request(method, url)
# FIXME: Yield goes here
        return s.send(prepped)

    def filter_disabled(self):
        try:
            if self.event['check']['alert'] is False:
                self.bail('alert disabled')
        except KeyError:
            pass

    def filter_repeated(self):
        occurrences = 1
        interval = 30
        refresh = 1800
        try:
            occurrences = self.event['check']['occurrences']
            interval = self.event['check']['interval']
            refresh = self.event['check']['refresh']
        except:
            pass

        if self.event['occurrences'] < occurrences:
            self.bail('not enough occurrences')

        if self.event['occurrences'] > occurrences and self.event['action'] == 'create':
                number = int(refresh / interval)
                print(self.event['occurrences'] % number)
                if number == 0 or not self.event['occurrences'] % number == 0:
                    self.bail("only handling every %d occurrences" % number)


    def filter_silenced(self):
        pass

    def filter_dependencies(self):
        pass

    def stash_exists(self):
        pass

    def event_exists(self):
        pass

    def _exitfunction(self):
        self.event = sensu_plugin.utils.read_event(sys.stdin)
        self.filter()
        self.handle()
