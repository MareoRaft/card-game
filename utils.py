""" A place for general-purpose helper functions that are fairly peripheral. """

import sys

def validate_python_version():
	if sys.version_info[0] < 3 or
			sys.version_info[0] == 3 and sys.version_info[1] < 7:
		raise SystemExit('Please use Python version >= 3.7.')
