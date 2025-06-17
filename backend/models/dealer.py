"""
dealer.py
----------
Defines the Dealer class which manages the dealer's hand and behavior.
"""

from models.deck import calculate_hand

class Dealer:
    def __init__(self):
        """Initialize an empty dealer hand."""
        self.hand = []

    def reset_hand(self):
        """Clear the dealer's hand."""
        self.hand = []

    def add_card(self, card):
        """Add a card to the dealer's hand."""
        self.hand.append(card)

    def should_draw(self):
        """
        Returns True if the dealer should draw another card.
        Dealer hits on 16 or less, stands on 17+ (even soft 17).
        """
        value = calculate_hand(self.hand)
        return value < 17

    def play_turn(self, deck):
        """
        Dealer draws until reaching a standing hand.
        """
        while self.should_draw():
            self.add_card(deck.draw_card())

    def is_busted(self):
        """Check if the dealer's hand exceeds 21."""
        return calculate_hand(self.hand) > 21

    def has_blackjack(self):
        """True if dealer has a natural Blackjack (only 2 cards summing 21)."""
        return len(self.hand) == 2 and calculate_hand(self.hand) == 21
