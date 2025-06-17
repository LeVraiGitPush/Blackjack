"""
seat.py
--------
Defines the Seat class which manages an individual seat at the table.
Includes hand state, bets, side bets, and player decisions.
"""

from models.deck import calculate_hand

class Seat:
    def __init__(self, seat_id, bet=0):
        """
        Initializes a seat with a unique seat ID and optional bet amount.
        """
        self.seat_id = seat_id
        self.hand = []
        self.bet = bet
        self.side_bets = {}  # { 'perfect_pair': amount, '21+3': amount, etc. }
        self.status = "active"  # Can be: 'active', 'stand', 'busted', 'blackjack'
        self.has_split = False
        self.has_doubled = False
        self.split_hand = None  # Optional: used if split occurs

    def place_bet(self, amount):
        self.bet = amount

    def add_side_bet(self, bet_type, amount):
        self.side_bets[bet_type] = amount

    def hit(self, card):
        self.hand.append(card)
        if calculate_hand(self.hand) > 21:
            self.status = "busted"

    def stand(self):
        self.status = "stand"

    def double(self, card):
        if len(self.hand) != 2:
            raise Exception("Double down only allowed on first 2 cards.")
        self.has_doubled = True
        self.bet *= 2
        self.hand.append(card)
        self.status = "stand"

    def split(self):
        if self.has_split or len(self.hand) != 2 or self.hand[0][0] != self.hand[1][0]:
            raise Exception("Split not allowed.")
        self.has_split = True
        self.split_hand = Seat(self.seat_id + "_split", self.bet)
        self.split_hand.hand.append(self.hand.pop())
        return self.split_hand

    def is_blackjack(self):
        return len(self.hand) == 2 and calculate_hand(self.hand) == 21

    def reset(self):
        self.hand = []
        self.bet = 0
        self.side_bets = {}
        self.status = "active"
        self.has_split = False
        self.has_doubled = False
        self.split_hand = None
