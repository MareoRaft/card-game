# builtin imports

# third-party imports

# local imports
from lib.config import NUM_PENALTY_CARDS, MIN_FACE_VALUE, MAX_FACE_VALUE, MIN_SUIT_VALUE, MAX_SUIT_VALUE, MIN_PLAYERS, MAX_PLAYERS
from lib.classes import PenaltyCard, Card, Deck, Player
from lib import validate
from lib.utils import prompt


def output_scoreboard(players):
    prompt.input(
        'And the current rankings are...(drumroll please)...\npress RETURN to continue')
    output = ''
    descending_players = get_descending_players(players)
    for index, player in enumerate(descending_players):
        rank = index + 1
        output += '{}. {}, with a score of {}\n'.format(
            rank, player.name, player.score)
    prompt.output(output)


def turn(deck, player, players):
    # player must press a key to draw card
    prompt.input('It\'s {}\'s turn!\npress RETURN to draw'.format(player.name))
    # draw card
    try:
        card = deck.draw()
    except IndexError:
        # in the rare case that the deck is empty, reset the deck.  This could lead to two players drawing the exact same card, which wouldn't happen in a *real* game of cards.  But this isn't really a big deal.
        prompt.output('shuffling a new deck...')
        deck.replenish()
        deck.shuffle()
        card = deck.draw()
    # show the card for all to see
    prompt.output('{} draws card\n{}'.format(player.name, card))
    # put card in hand
    player.draw(card)


def adjust_player_scores(players):
    penalty_players = [p for p in players if isinstance(p.card, PenaltyCard)]
    non_penalty_players = [
        p for p in players if not isinstance(p.card, PenaltyCard)]
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
    prompt.output('Next round.')
    # each player draws a card from the deck
    for player in players:
        turn(deck, player, players)
    # adjust player scores
    adjust_player_scores(players)
    # discard hands
    for player in players:
        player.discard()
    # output round info to terminal
    output_scoreboard(players)


def input_num_players():
    # set the number of players
    return prompt.input('How many players?', request_type=int, validator=validate.num_players)


def input_player(num):
    # setup a player
    input_message = 'What is player {}\'s name?'.format(num)
    return prompt.input(input_message, converter=Player)


def get_descending_players(players):
    # returns players sorted, highest first
    return list(sorted(players, key=lambda p: p.score, reverse=True))


def has_winner(players):
    """ Returns a boolean indicating whether or not a winner exists. """
    descending_players = get_descending_players(players)
    max_score = descending_players[0].score
    second_max_score = descending_players[1].score
    return (max_score >= 21) and (max_score >= second_max_score + 2)


def setup_game():
    # set up the deck
    penalty_cards = [PenaltyCard() for _ in range(NUM_PENALTY_CARDS)]
    regular_cards = [Card(face_val, suit_value)
                     for face_val in range(MIN_FACE_VALUE, MAX_FACE_VALUE + 1)
                     for suit_value in range(MIN_SUIT_VALUE, MAX_SUIT_VALUE + 1)]
    cards = penalty_cards + regular_cards
    deck = Deck(cards)
    deck.shuffle()
    # set the number of players
    num_players = input_num_players()
    # setup each player
    players = [input_player(index + 1) for index in range(num_players)]
    return deck, players


def game():
    """ A game allows for two through four players, the number of which should be selectable at the beginning of a game (setup_game).  A game consists of rounds until certain score criteria is met. """
    deck, players = setup_game()
    while not has_winner(players):
        round(deck, players)
    winner = get_descending_players(players)[0]
    prompt.output('The winner is {}!!!'.format(winner.name))
