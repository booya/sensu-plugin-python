#!/usr/bin/env python
#coding=utf-8

#
# Copyright (C) 2014 - S. Zachariah Sprackett <zac@sprackett.com>
#
# Released under the same terms as Sensu (the MIT license); see LICENSE
# for details.
"""
Provides primitives for implementing a Sensu check
"""

from __future__ import print_function
from sensu_plugin.plugin import SensuPlugin


class SensuPluginCheck(SensuPlugin):
    """
    The framework for implementing a Sensu check
    """
    def check_name(self, name=None):
        """Get or set the name of this Sensu check"""
        if name:
            self.plugin_info['check_name'] = name

        if self.plugin_info['check_name'] is not None:
            return self.plugin_info['check_name']

        return self.__class__.__name__

    def message(self, *m):
        """Set the default message this check will output"""
        self.plugin_info['message'] = m

    def output(self, m):
        """Output the message"""
        msg = ''
        if m is None or (m[0] is None and len(m) == 1):
            m = self.plugin_info['message']

        if not m is None and not (m[0] is None and len(m) == 1):
            msg = ": {}".format(' '.join(str(message) for message in m))

        print("{} {}{}".format(self.check_name(),
              self.plugin_info['status'], msg))
