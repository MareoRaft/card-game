#!/usr/bin/python

# builtin imports
from __future__ import print_function
import random

# third-party imports
# none here

# local imports
from utils import validate_python_version
from decorate import read_only

MIN_PLAYERS = 2
MAX_PLAYERS = 4


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
		return '({}, {})'.format(self.face_value, self.suit)

	@property
	def face_value(self):
		return self._face_value
	@face_value.setter
	@read_only
	def face_value(self, new_face_value):
		# jack is 11, queen 12, king 13, ace is 14
		if not (2 <= face_value <= 14):
			raise ValueError
		self._face_value = new_face_value

	@property
	def suit(self):
		return self._suit
	@suit.setter
	@read_only
	def suit(self, new_suit):
		# club is 1, diamond is 2, heart 3, spade 4
		if not (1 <= suit <= 4):
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


def is_penalty_card(card):
	if card is None:
		raise ValueError
	return isinstance(card, PenaltyCard)

def output_scoreboard(players):
	output = 'And the current rankings are...(drumroll please)...\n'
	descending = list(reversed(sorted((p.score, p) for p in players)))
	# TODO: clean this up
	for index, tuple_ in enumerate(descending):
		(_, player) = tuple_
		rank = index + 1
		output += '{}. {}, with a score of {}\n'.format(rank, player.name, player.score)
	print(output)

def turn(deck, player):
	print('It is player {}\'s turn!'.format(player.name))
	# player must press a key to draw card
	raw_input('press any key to draw')
	# draw card
	try:
		card = deck.draw()
	except IndexError:
		# in the rare case that the deck is empty, take the discard pile and shuffle it
		print('reshuffling the discard pile.')
		discarded_cards = set(deck._original_cards) - set(p.card for p in players)
		deck.__init__(discarded_cards)
		deck.shuffle()
		card = deck.draw()
	# show the card for all to see
	print('player {} draws card {}.'.format(player.name, card))
	# put card in hand 
	player.draw(card)


def adjust_player_scores(players):
	penalty_players = [p for p in players if is_penalty_card(p.card)]
	non_penalty_players = [p for p in players if not is_penalty_card(p.card)]
	# 1 point penalty for penalty card players
	for penalty_player in penalty_players:
			penalty_player.adjust_score(-1)
	# 2 points for player with highest ranked card
	# note: We take advantage of the fact that the cards are linearly ordered and there are no duplicates.
	max_card = max(p.card for p in non_penalty_players)
	for player in players:
		if player.card == max_card:
			player.adjust_score(2)

def round(deck, players):
	""" A round consists of each player drawing a card and then a scoreboard update. """
	# each player draws a card from the deck
	for player in players:
		turn(deck, player)
	# adjust player scores
	adjust_player_scores(players)
	# discard hands
	for player in players:
		player.discard()
	# output round info to terminal
	output_scoreboard(players)

def input_num_players():
	# set the number of players
	while True:
		try:
			num_players = int(raw_input('How many players?'))
			assert MIN_PLAYERS <= num_players <= MAX_PLAYERS
			return num_players
		except:
			pass

def input_player():
	# TODO: use the PROMPT module
	# TODO: make this loop like input_num_players when there's bad input
	# setup a player
	name = str(raw_input('What is player\'s name?'))
	return Player(name)

def leader(players):
	# returns a player with a max score
	# TODO: factor out this ordering of players, which happens 3 times in the program
	ascending = list(sorted((p.score, p) for p in players))
	return ascending[-1][1]

def has_winner(players):
	""" Returns a boolean indicating whether or not a winner exists. """
	ascending_scores = list(sorted(p.score for p in players))
	max_score = ascending_scores[-1]
	second_max_score = ascending_scores[-2]
	return max_score >= 21 and max_score >= second_max_score + 2

def setup_game():
	# set up the deck
	penalty_cards = [PenaltyCard()] * 4
	regular_cards = [Card(face_val, suit) for face_val in range(2, 14 + 1) for suit in range(1, 4 + 1)]
	cards = penalty_cards + regular_cards
	deck = Deck(cards)
	deck.shuffle()
	# set the number of players
	num_players = input_num_players()
	# setup each player
	players = [input_player() for _ in range(num_players)]
	return deck, players

def game():
	""" A game allows for two through four players, the number of which should be selectable at the beginning of a game (setup_game).  A game consists of rounds until certain score criteria is met. """
	deck, players = setup_game()
	while not has_winner(players):
		round(deck, players)
	winner = leader(players)

if __name__ == '__main__':
	# TODO: possibly make a 'main.py' which does the manage python version, or maybe not
	validate_python_version()
	game()
