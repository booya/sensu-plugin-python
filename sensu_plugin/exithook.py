#!/usr/bin/env python
#coding=utf-8

#
# Copyright (C) 2014 - S. Zachariah Sprackett <zac@sprackett.com>
#
# Released under the same terms as Sensu (the MIT license); see LICENSE
# for details.
"""
Primitives for using exithooks
"""

import sys


class ExitHook(object):
    """
    A class to record exceptions and exit codes so that we can make use of
    them in our atexit handler.
    """
    def __init__(self):
        self._orig_exit = None
        self.exit_code = None
        self.exception = None
        self.exc_type = None

    def hook(self):
        """Wire up the exit hook"""
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    def exit(self, code=0):
        """Handle exit"""
        self.exit_code = code
        self._orig_exit(code)

    def exc_handler(self, exc_type, exc, *_args):
        """Handle exception"""
        self.exception = exc
        self.exc_type = exc_type
