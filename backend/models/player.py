#!/usr/bin/env python3
"""
player.py
----------
Defines the Player class for Blackjack. 
Handles player's name, balance, and assigned seats.
"""

class Player:
    def __init__(self, name, balance=1000):
        """
        Initialize a player with a name and optional starting balance.
        """
        self.name = name
        self.balance = balance
        self.seats = []  # List of Seat instances (max 3)

    def can_afford(self, amount):
        """Check if the player has enough balance for the given amount."""
        return self.balance >= amount

    def adjust_balance(self, amount):
        """
        Adjust balance by amount (can be negative for losses).
        """
        self.balance += amount

    def add_seat(self, seat):
        """
        Assign a seat to the player (max 3).
        """
        if len(self.seats) >= 3:
            raise ValueError(f"{self.name} cannot occupy more than 3 seats.")
        self.seats.append(seat)

    def remove_seat(self, seat):
        """Remove a seat from the player's assigned seats."""
        if seat in self.seats:
            self.seats.remove(seat)

    def reset_seats(self):
        """Clear all seat assignments (e.g., between rounds)."""
        self.seats = []

    def __str__(self):
        return f"{self.name} (${self.balance})"
