#!/usr/bin/env python
# encoding: utf-8
"""
command.py

Created by Olli Wang (olliwang@ollix.com) on 2011-04-25.
Copyright (c) 2011 Ollix. All rights reserved.
"""

import sys

from oparse import command


class BacksqlCommand(command.Command):
    usage = 'backsql'

    def command(self, args, options):
        pass


if __name__ == '__main__':
    command = BacksqlCommand()
    command(*sys.argv)
