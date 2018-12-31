#!/usr/bin/env python3
# This will probably work in python2 just the same.
import os
from os import path
import re

def html_to_pystring(html):
    string = html
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
    ## header to nothing
    string = re.sub(
        r'<code><span style="display:block;line-height:8px; font-size: 8px; font-weight:bold;white-space:pre;font-family: monospace;color: black; background: white;">',
        r'',
        string)
    ## footer to color reset
    string = re.sub(
        r" \+ </span></code>'\\n' \+ ",
        r' + Style.RESET_ALL',
        string)
    ## condense repeated colors to save space
    for _ in range(9):
        string = re.sub(
            r"""(fg\(\d{1,3}, \d{1,3}, \d{1,3}\)) \+ '([^']+)' \+ \1 \+ '([^']+)'""",
            r"\1 + '\2\3'",
            string)
    ## condense white string
    string = re.sub(r"""fg\(255, 255, 255\)""", "fg.white", string)
    ## condense black string
    string = re.sub(r"""fg\(0, 0, 0\)""", "fg.black", string)

    # output
    return string

def main():
    in_dir_path = 'data/html'
    out_path = 'data/strings/image_strings.py'
    # write the top of the file
    header = 'import colorama\nfrom colorama import Fore, Back, Style\nfrom sty import fg, bg, ef, rs, Rule, Render\n\ncolorama.init()\n\ncard_image_strings = dict()\n\n'
    open(out_path, 'w').write(header)
    # generate the strings and write them to the file
    for in_file_name in sorted(os.listdir(in_dir_path)):
        card_id, ext = path.splitext(in_file_name)
        if ext == '.html':
            in_file_path = path.join(in_dir_path, in_file_name)
            html = open(in_file_path).read()
            pystring = html_to_pystring(html)
            new_content = 'card_image_strings["{}"] = {}\n\n'.format(card_id, pystring)
            open(out_path, 'a').write(new_content)

if __name__ == '__main__':
    main()
