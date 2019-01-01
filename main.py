#!/usr/bin/env python3

# builtin imports

# third-party imports
import colorama

# local imports
from lib import validate
from lib.game import game

if __name__ == '__main__':
    validate.python_version()
    # make color codes work on windows too
    colorama.init()
    # finally, play!
    game()
