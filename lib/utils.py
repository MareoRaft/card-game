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

string_prompt = '{}>{}>{}>'.format(fg.BLUE, fg.ORANGE, fg.RED)

def print_pretty(string):
	string_pretty = '\n{} {}\n'.format(string_prompt, string)
	print(string_pretty)

def input_pretty(string):
	string_pretty = '{prompt} {string}\n{prompt} '.format(prompt=string_prompt, string=string)
	output = input(string_pretty)
	return output
