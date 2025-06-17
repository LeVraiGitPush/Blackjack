"""
deck.py
---------
Module for managing a shoe (8 decks) in a Blackjack game.
Handles shuffling, drawing, and automatic reshuffle when half the cards are used.
"""

import random

class Deck:
    def __init__(self, num_decks=8):
        """Initialize the deck with num_decks (8 for casino shoe)."""
        self.num_decks = num_decks
        self.full_deck = self._generate_deck()
        self.cards = self.full_deck.copy()
        self.shuffle()

    def _generate_deck(self):
        """Generate multiple standard 52-card decks."""
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        return [(rank, suit) for rank in ranks for suit in suits] * self.num_decks

    def shuffle(self):
        """Shuffle the cards."""
        random.shuffle(self.cards)

    def draw_card(self):
        """Draw a card from the deck. Automatically reshuffle if needed."""
        if self.cards_remaining() < len(self.full_deck) // 2:
            self.reshuffle()
        return self.cards.pop()

    def cards_remaining(self):
        """Return the number of remaining cards in the deck."""
        return len(self.cards)

    def reshuffle(self):
        """Rebuild and shuffle the full shoe."""
        print("[🔄] Deck reshuffling... New shoe loaded.")
        self.cards = self.full_deck.copy()
        self.shuffle()

"""
card_utils.py
--------------
Utility functions for handling cards, displaying hands, and calculating hand values.
"""

def card_value(card):
    """Returns the value of a single card for Blackjack."""
    rank = card[0]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11  # Handle Ace as 11 initially, reduce later if needed
    else:
        return int(rank)

def calculate_hand(hand):
    """
    Calculate the best value of a hand in Blackjack.
    Handles Aces as 11 or 1 dynamically.
    """
    value = 0
    aces = 0

    for card in hand:
        val = card_value(card)
        value += val
        if card[0] == 'A':
            aces += 1

    while value > 21 and aces:
        value -= 10  # Convert Ace from 11 to 1
        aces -= 1

    return value

def display_hand(hand):
    """Returns a simple string representation of a hand."""
    return ' '.join([f"{rank}{suit}" for rank, suit in hand])

def display_hand_with_value(hand):
    """Returns hand with total value."""
    return f"{display_hand(hand)} (Total: {calculate_hand(hand)})"
