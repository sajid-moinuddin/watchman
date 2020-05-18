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

import logging
import sys
from docopt import docopt
# from watchman import watchman_utils
from watchman import test
arguments = docopt(__doc__, version='${version}')

verbose_mode = False
action = None

print('.............Night gathers, and now my watch begins..............\n')