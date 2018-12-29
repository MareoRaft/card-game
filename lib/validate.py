# This module is for validation / error checking.  Within this project, to 'validate' means to check that inputs are good and emit an error otherwise.  So almost all errors that occur should happen in this file.

def face_value(value):
	if not (MIN_FACE_VALUE <= value <= MAX_FACE_VALUE):
		raise ValueError('face value must be between {} and {} inclusive'.format(MIN_FACE_VALUE, MAX_FACE_VALUE))

def suit_value(new_suit_value):
	if not (MIN_SUIT_VALUE <= new_suit_value <= MAX_SUIT_VALUE):
		raise ValueError('bad suit_value value')

def score_adjustment(value):
	if not isinstance(value, int):
		raise TypeError
