# -*- coding: utf-8 -*-
#
# (c) Mihai Maruseac, 341C3 (2011), mihai.maruseac@rosedu.org
#

import cPickle

def main(files):
    """
    Compares runs from the passed list of files.

    Basically, it just prints everything to be piped to a gnuplot command.

    return True if everything is ok, False otherwise
    """
    _lists_ = []
    for fname in files:
        try:
            with open(fname) as f:
                _lists_.append(cPickle.load(f))
        except:
            return False

    minl = min(map(lambda l:len(l), _lists_))

    for i in range(minl):
        print i, 
        for l in _lists_:
            print l[i],
        print
    return True


