"""
table.py
---------
Defines the Table class that coordinates game state, seats, and round orchestration.
"""

from models.deck import *
from models.seat import *
from models.dealer import *

class Table:
    def __init__(self):
        """Initialize table with 7 seats and a fresh deck."""
        self.seats = [None] * 7  # 7 seats max, each can hold a Seat instance
        self.dealer = Dealer()
        self.deck = Deck()

    def assign_seat(self, player, seat_index, seat_obj):
        """
        Assigns a player to a seat index with a Seat object.
        """
        if not (0 <= seat_index < 7):
            raise IndexError("Seat index must be between 0 and 6.")
        if self.seats[seat_index]:
            raise ValueError(f"Seat {seat_index + 1} is already occupied.")
        self.seats[seat_index] = seat_obj
        player.add_seat(seat_obj)

    def start_round(self):
        """Clear all hands and prepare for a new round."""
        self.dealer.reset_hand()
        for seat in self.seats:
            if seat:
                seat.reset()

    def get_active_seats(self):
        """Return all currently assigned seats."""
        return [seat for seat in self.seats if seat is not None]

    def resolve_hands(self):
        """
        After dealer plays, compare all player hands to dealer.
        Returns dict of outcomes per seat.
        """
        results = {}
        dealer_value = self.dealer_value()
        dealer_bust = self.dealer.is_busted()

        for idx, seat in enumerate(self.seats):
            if not seat:
                continue
            player_value = seat_value = seat.split_hand_value = 0
            if seat.status == "busted":
                results[idx] = "lose"
            elif seat.is_blackjack() and not self.dealer.has_blackjack():
                results[idx] = "blackjack"
            elif self.dealer.has_blackjack() and not seat.is_blackjack():
                results[idx] = "lose"
            elif dealer_bust:
                results[idx] = "win"
            else:
                player_value = calculate_hand(seat.hand)
                if player_value > dealer_value:
                    results[idx] = "win"
                elif player_value == dealer_value:
                    results[idx] = "push"
                else:
                    results[idx] = "lose"
        return results

    def dealer_value(self):
        return calculate_hand(self.dealer.hand)

    def clear_table(self):
        """Remove all players from seats."""
        for i in range(len(self.seats)):
            self.seats[i] = None
