# services/fake_player_logic.py
"""
Author:Levraigitpush
fake_player_logic.py : Logic des bot
"""

from models.deck import calculate_hand, card_value
from game_state import FAKE_STRATEGY
from services.chart_ai import make_fake_decision 

def play_fake_turns(table, lobby_id):
    dealer_up = table.dealer.hand[0]

    for seat in table.get_active_seats():
        player_name = seat.seat_id if isinstance(seat.seat_id, str) else None
        if player_name not in FAKE_STRATEGY:
            continue

        while seat.status == "active":
            action = make_fake_decision(seat, dealer_up)
            if action == "hit":
                seat.hit(table.deck.draw_card())
            elif action == "stand":
                seat.stand()
            elif action == "double":
                try:
                    seat.double(table.deck.draw_card())
                except:
                    seat.hit(table.deck.draw_card())
            elif action == "split":
                try:
                    split = seat.split()
                    split.hit(table.deck.draw_card())
                    seat.hit(table.deck.draw_card())
                    table.seats.append(split)
                except:
                    seat.hit(table.deck.draw_card())
