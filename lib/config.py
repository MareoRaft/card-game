import sys

from sty import fg

from lib.prompt import Prompt


# game dynamics
NUM_PENALTY_CARDS = 4

MIN_FACE_VALUE = 2
MAX_FACE_VALUE = 14

MIN_SUIT_VALUE = 1
MAX_SUIT_VALUE = 4

MIN_PLAYERS = 2
MAX_PLAYERS = 4


# color palette
blue = fg(26, 20, 127)
light_blue = fg(45, 120, 255)
gold = fg(248, 194, 15)
red = fg(230, 20, 8)

DEFAULT_TEXT_COLOR = light_blue
ERROR_TEXT_COLOR = red


# make a prompt object for interacting with the user
PROMPT = Prompt(input_prefix='{}>{}>{}>{} '.format(light_blue, gold, red, DEFAULT_TEXT_COLOR),
                output_prefix='\n{}'.format(DEFAULT_TEXT_COLOR),
                warn_prefix=ERROR_TEXT_COLOR)
