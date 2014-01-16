#!/usr/bin/env python
#coding=utf-8

#
# Copyright (C) 2014 - S. Zachariah Sprackett <zac@sprackett.com>
#
from __future__ import print_function
import os
import sys
import json


def config_files():
    if 'SENSU_CONFIG_FILES' in os.environ:
        return os.environ['SENSU_CONFIG_FILES'].split(':')
    else:
        pass


def load_config(filename):
    pass


def settings():
    pass


def read_event(filehandle):
    try:
        event = json.load(filehandle)
        if not 'occurrences' in event:
            event['occurrences'] = 1
        if not 'check' in event:
            event['check'] = {}
        if not 'client' in event:
            event['client'] = {}
        return event
    except ValueError as exc:
        print("error reading event: %s" % exc)
        sys.stdout.flush()
        os._exit(1)
