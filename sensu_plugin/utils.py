#!/usr/bin/env python
#coding=utf-8

#
# Copyright (C) 2014 - S. Zachariah Sprackett <zac@sprackett.com>
#
import os
import sys
import json

def read_event(file):
    try:
        event = json.load(file)
        if not 'occurrences' in event:
            event['occurrences'] = 1
        if not 'check' in event:
            event['check'] = {}
        if not 'client' in event:
            event['client'] = {}
        return event
    except Exception as e:
        print("error reading event: %s" % e)
        sys.stdout.flush()
        os._exit(1)
