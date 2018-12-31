""" A place for general-purpose helper functions that are fairly peripheral. """

import sys

# todo: make below more concise
import colorama
from colorama import Fore, Back, Style
from sty import fg, bg, ef, rs, Rule, Render
colorama.init()

def validate_python_version():
	if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 7):
		raise SystemExit('Please use Python version >= 3.7.')

blue = fg(26, 20, 127)
light_blue = fg(45, 120, 255)
gold = fg(248, 194, 15)
red = fg(230, 20, 8)
string_prompt = '{}>{}>{}>{} '.format(light_blue, gold, red, light_blue)

def print_pretty(string):
	string_pretty = '\n{}{}'.format(light_blue, string)
	print(string_pretty)

def input_pretty(string):
	print_pretty(string)
	output = input(string_prompt)
	return output
