#!/usr/bin/env python

"""
Night gathers, and now my watch begins.

Usage:
watchman watch [options]

Options:
-v --verbose                 be more verbose
--vector-id STRING           if you want vector to create a scene
--version                    show version
"""

"""
pyb publish
pip install .tar.gz
runMyScript.py
uninstall
"""

import logging
import sys
import logging

from docopt import docopt
# from watchman import watchman_utils
from watchman import main
arguments = docopt(__doc__, version='${version}')

verbose_mode = False
action = None

log_level = logging.INFO

if verbose_mode:
    log_level = logging.DEBUG

print('.............Night gathers, and now my watch begins..............\n')


main.begin(log_level)
