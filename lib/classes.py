import random

from lib.decorate import read_only
from lib import validate
from data.strings.image_strings import card_image_strings


class PenaltyCard:
	""" A penalty card. """
	def __str__(self):
		""" Pretty string version of the card for the user. """
		# I chose the Joker image for the penalty card.
		return card_image_strings['joker']
	

class Card:
	def __init__(self, face_value, suit_value):
		""" `face_value` is any integer from 2 to 14, inclusive.  `suit_value` is any integer from 1 to 4, inclusive. """
		self.face_value = face_value
		self.suit_value = suit_value

	def __str__(self):
		""" Pretty string version of the card for the user. """
		card_id = '{}-{}'.format(self.face_value, self.suit_value)
		return card_image_strings[card_id]

	@property
	def face_value(self):
		return self._face_value
	@face_value.setter
	@read_only
	def face_value(self, new_face_value):
		# jack is 11, queen 12, king 13, ace is 14
		validate.face_value(new_face_value)
		self._face_value = new_face_value

	@property
	def suit_value(self):
		return self._suit_value
	@suit_value.setter
	@read_only
	def suit_value(self, new_suit_value):
		# club is 1, diamond is 2, heart 3, spade 4
		validate.suit_value(new_suit_value)
		self._suit_value = new_suit_value

	# implement an ordering on the cards
	# i wonder if there's a nicer way to do this, like saying "standard ordering on (self.face_value, self.suit_value)"
	def __eq__(self, other):
		return (self.face_value, self.suit_value) == (other.face_value, other.suit_value)

	def __ne__(self, other):
		return not self == other

	def __lt__(self, other):
		return (self.face_value, self.suit_value) < (other.face_value, other.suit_value)

	def __le__(self, other):
		return self < other or self == other

	def __gt__(self, other):
		return not self <= other

	def __ge__(self, other):
		return not self < other


class Deck:
	""" A deck of cards. """
	def __init__(self, cards):
		""" A 'new' deck is basically a list of cards (the `cards` given).  They are intentionally *not* shuffled on init because you might want your deck to be in a specific order. """
		self._original_cards = cards
		self.replenish()

	def replenish(self):
		""" Restore the deck to its original state. """
		self._cards = self._original_cards

	def shuffle(self):
		""" Shuffles the cards currently in the deck with uniform probability. """
		random.shuffle(self._cards)

	def draw(self):
		""" Draw a card from the deck and return it. """
		return self._cards.pop()


class Player:
	def __init__(self, name):
		validate.player_name(name)
		self._name = name
		self._score = 0
		self.card = None

	@property
	def name(self):
		return self._name

	@property
	def score(self):
		return self._score

	def adjust_score(self, adjustment):
		validate.score_adjustment(adjustment)
		# adjust score
		self._score += adjustment
		# the score cannot go below 0
		self._score = max(0, self._score)

	def draw(self, card):
		# add `card` to player's hand
		self.card = card

	def discard(self):
		self.card = None
