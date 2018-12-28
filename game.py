#!/usr/bin/env python3

# builtin imports
from __future__ import print_function
import random

# third-party imports
import colorama

# local imports
from utils import validate_python_version
from decorate import read_only
from classes import PenaltyCard, Card, Deck, Player
from config import MIN_FACE_VALUE, MAX_FACE_VALUE, MIN_SUIT, MIN_PLAYERS, MAX_PLAYERS

card_strings = {}
for face_value in range(MIN_FACE_VALUE, MAX_FACE_VALUE + 1):
	for suit in range(MIN_SUIT, MAX_SUIT + 1):
		card_id = '{}-{}'.format(face_value, suit)
		import_path = 'data.pystring.{}'.format(card_id)
		module = __import__(import_path, fromlist=[''])
		card_strings[card_id] = module.s

def is_penalty_card(card):
	if card is None:
		raise ValueError
	return 

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
	penalty_players = [p for p in players if isinstance(card, PenaltyCard)]
	non_penalty_players = [p for p in players if not isinstance(card, PenaltyCard)]
	# 1 point penalty for players with penalty card
	for penalty_player in penalty_players:
			penalty_player.adjust_score(-1)
	# 2 points for player(s) with highest ranked card
	# note: The 'if' statement is necessary because it is possible that all players draw penalty cards, in which case you cannot get a max.
	if non_penalty_players:
		max_card = max(p.card for p in non_penalty_players)
		for non_penalty_player in non_penalty_players:
			# note: If we were dealing with a deck that had multiple cards of the same value, more than one player could get the 2-point bonus.
			if non_penalty_player.card == max_card:
				non_penalty_player.adjust_score(2)

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
	# make color codes work on windows too
	colorama.init()
	# finally, play!
	game()
