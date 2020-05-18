
#!/usr/bin/env python

import sys
import logging

sys.path.append('src/main/python')

from watchman import main

main.begin(logging.DEBUG)