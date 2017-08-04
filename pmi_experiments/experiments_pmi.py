#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import config


def main():
    print '====================================== ' + config.options.experiment

    print 'TODO!'


# example call: python experiments.py -p pickle_small -e experiment1 -s 3000 -l 3010
if __name__ == "__main__":
    main()  # options are parsed in config.oy
