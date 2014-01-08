#!/usr/bin/env python
#coding=utf-8

#
# Copyright (C) 2014 - S. Zachariah Sprackett <zac@sprackett.com>
#
# Released under the same terms as Sensu (the MIT license); see LICENSE
# for details.
"""
Provides primitives for implemening a Sensu plugin
"""

from __future__ import print_function
import atexit
import sys
import argparse
import os
import traceback
from collections import namedtuple
from sensu_plugin.exithook import ExitHook

ExitCode = namedtuple('ExitCode', ['OK', 'WARNING', 'CRITICAL', 'UNKNOWN'])


class SensuPlugin(object):
    """
    The base class that implements functionality required for all sensu
    plugins.  You probably should not be using this class directly.
    """
    def __init__(self):
        self.plugin_info = {
            'check_name': None,
            'message': None,
            'status': None
        }
        self._hook = ExitHook()
        self._hook.hook()

        self.exit_code = ExitCode(0, 1, 2, 3)
        for field in self.exit_code._fields:
            self._make_dynamic(field)

        atexit.register(self._exitfunction)

        self.parser = argparse.ArgumentParser()
        if hasattr(self, 'setup'):
            self.setup()
        (self.options, self.remain) = self.parser.parse_known_args()

        self.run()

    def output(self, args):
        """Format and print the arguments"""
        print("SensuPlugin: %s" % ' '.join(str(a) for a in args))

    def _make_dynamic(self, method):
        """Build and register our dynamic functions"""

        def dynamic(*args):
            """ This becomes ok, warning, critical and unknown """
            self.plugin_info['status'] = method
            if len(args) == 0:
                args = None
            self.output(args)
            sys.exit(getattr(self.exit_code, method))

        method_lc = method.lower()
        dynamic.__doc__ = "%s method" % method_lc
        dynamic.__name__ = method_lc
        setattr(self, dynamic.__name__, dynamic)

    def run(self):
        """The actual check.  You should override this method"""
        self.warning("Not implemented! You should override SensuPlugin.run()")

    def _exitfunction(self):
        """The exit handler.  Deal with exceptions and plugins that don't
        implement the run method"""
        if self._hook.exit_code is None and self._hook.exception is None:
            print("Check did not exit! You should call an exit code method.")
            sys.stdout.flush()
            os._exit(1)
        elif self._hook.exception:
            print("Check failed to run: %s, %s" %
                 (sys.last_type, traceback.format_tb(sys.last_traceback)))
            sys.stdout.flush()
            os._exit(2)
