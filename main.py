#!/usr/bin/env python3

# builtin imports
from lib.utils import validate_python_version

# third-party imports
import colorama

# local imports
from lib.game import game

if __name__ == '__main__':
	validate_python_version()
	# make color codes work on windows too
	colorama.init()
	# finally, play!
	game()
