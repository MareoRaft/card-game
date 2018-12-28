from config import MIN_FACE_VALUE, MAX_FACE_VALUE, MIN_SUIT, MIN_PLAYERS, MAX_PLAYERS

class PenaltyCard:
	""" A penalty card. """
	def __str__(self):
		""" Pretty string version of the card for the user. """
		return 'a penalty card'
	

class Card:
	def __init__(self, face_value, suit):
		""" `face_value` is any integer from 2 to 14, inclusive.  `suit` is any integer from 1 to 4, inclusive. """
		self.face_value = face_value
		self.suit = suit

	def __str__(self):
		""" Pretty string version of the card for the user. """
		card_id = '{}-{}'.format(self.face_value, self.suit)
		return card_strings[card_id]

	@property
	def face_value(self):
		return self._face_value
	@face_value.setter
	@read_only
	def face_value(self, new_face_value):
		# jack is 11, queen 12, king 13, ace is 14
		if not (MIN_FACE_VALUE <= face_value <= MAX_FACE_VALUE):
			raise ValueError
		self._face_value = new_face_value

	@property
	def suit(self):
		return self._suit
	@suit.setter
	@read_only
	def suit(self, new_suit):
		# club is 1, diamond is 2, heart 3, spade 4
		if not (MIN_SUIT <= suit <= MAX_SUIT):
			raise ValueError
		self._suit = new_suit

	# implement an ordering on the cards
	def __eq__(self, other):
		return self.face_value == other.face_value and self.suit == other.suit

	def __lt__(self, other):
		return self.face_value < other.face_value or self.suit < other.suit

	# the rest of the orderings depends on the previous ones.  i don't know which of these are automatic and which i actually need to implement.  so maybe we can delete some of these...
	def __leq__(self, other):
		return self < other or self == other

	def __gt__(self, other):
		return not self <= other

	def __geq__(self, other):
		return self > other or self == other

	# i wonder if there was a nicer way to do this, like saying "standard ordering on (self.face_value, self.suit)"


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
		if not isinstance(adjustment, int):
			raise TypeError
		# adjust score
		self._score += adjustment
		# the score cannot go below 0
		self._score = max(0, self._score)

	def draw(self, card):
		# add `card` to player's hand
		self.card = card

	def discard(self):
		self.card = None
