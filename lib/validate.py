# This module is for validation / error checking.  Within this project, to 'validate' means to check that inputs are good and emit an error otherwise.  So almost all errors that occur should happen in this file.
from lib.config import MIN_FACE_VALUE, MAX_FACE_VALUE, MIN_SUIT_VALUE, MAX_SUIT_VALUE, MIN_PLAYERS, MAX_PLAYERS

def face_value(value):
    if not isinstance(value, int):
        raise TypeError('the face value must be an integer')
    if not (MIN_FACE_VALUE <= value <= MAX_FACE_VALUE):
        raise ValueError('face value must be between {} and {} inclusive'.format(MIN_FACE_VALUE, MAX_FACE_VALUE))

def suit_value(value):
    if not isinstance(value, int):
        raise TypeError('the suit value must be an integer')
    if not (MIN_SUIT_VALUE <= value <= MAX_SUIT_VALUE):
        raise ValueError('the suit value must be at least {} and at most {}'.format(MIN_SUIT_VALUE, MAX_SUIT_VALUE))

def score_adjustment(value):
    if not isinstance(value, int):
        raise TypeError('the score adjustment value must be an integer')

def num_players(value):
    if not isinstance(value, int):
        raise TypeError('the number of players must be an integer')
    if not MIN_PLAYERS <= value <= MAX_PLAYERS:
        raise ValueError('the number of players must be at least {} and at most {}'.format(MIN_PLAYERS, MAX_PLAYERS))

def player_name(value):
    if not isinstance(value, str):
        raise TypeError('player\'s name must be a string')
    if value == '':
        raise TypeError('player\'s name cannot be the empty string')
