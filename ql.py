#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import sys

import src.gui
import src.cmp_plot

def usage():
    print './ql.py : simulates a robot'
    print './ql.py cmp [FILES] : compares several runs'

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == 'cmp':
        if not src.cmp_plot.main(sys.argv[2:]):
            usage()
    elif len(sys.argv) == 1:
       src.gui.main()
    else:
        usage()

