import colorama
colorama.init()

from colorama import Fore, Back, Style
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')

# from string import string
# print(string)

# and now we need 256 color support
# import sty
# from sty import fg, bg, ef, rs, Rule, Render

from pystring.queen import s
print(s)
