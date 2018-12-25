import re

# config
in_path = 'html/queen.html'
out_path = 'pystring/queen.py'

# input
string = open(in_path).read()

# perform regex
## colors to colors
string = re.sub(
	r'<span style="color:rgb\((\d{1,3}) , (\d{1,3}) , (\d{1,3})\);">(.)</span>',
	r"fg(\1, \2, \3) + '\4' + ",
	string)
## newlines to newlines
string = re.sub(
	r'\n',
	r"'\\n' + ",
	string)
## header to header
string = re.sub(
	r'<code><span style="display:block;line-height:8px; font-size: 8px; font-weight:bold;white-space:pre;font-family: monospace;color: black; background: white;">',
	r"from sty import fg, bg, ef, rs, Rule, Render\n\ns = ",
	string)
## footer to nothing
string = re.sub(
	r" \+ </span></code>'\\n' \+ ",
	r"",
	string)
## condense white things to save space
string = re.sub(r"""fg\(255, 255, 255\)""", "fg.white", string)
for _ in range(9):
	string = re.sub(
		r"""fg\.white \+ '([^']+)' \+ fg\.white \+ '([^']+)'""",
		r"fg.white + '\1\2'",
		string)

# output
open(out_path, 'w').write(string)
