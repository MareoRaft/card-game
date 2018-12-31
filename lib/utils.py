""" A place for general-purpose helper functions that are fairly peripheral. """
import sys

import colorama
from colorama import Fore, Back, Style
from sty import fg, bg, ef, rs, Rule, Render

from lib.prompt import Prompt

# some colors for the prompt
colorama.init()
blue = fg(26, 20, 127)
light_blue = fg(45, 120, 255)
gold = fg(248, 194, 15)
red = fg(230, 20, 8)

# make a prompt object for interacting with the user
prompt = Prompt(input_prefix='{}>{}>{}>{} '.format(light_blue, gold, red, light_blue),
		output_prefix='\n{}'.format(light_blue),
		warn_prefix=red)

def validate_python_version():
	if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 7):
		raise SystemExit('Please use Python version >= 3.7.')
