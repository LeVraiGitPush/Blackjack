# backend/routes/game_routes.py
"""
Author:Levraigitpush
game_routes.py
-----------
Logic des bot
"""

from game_state import FAKE_STRATEGY
from flask import Blueprint, request, jsonify
from game_state import get_lobby
from core import blackjack
from models.deck import calculate_hand, card_value
from services.fake_player_logic import play_fake_turns

game_bp = Blueprint("game", __name__)

@game_bp.route("/<lobby_id>/start_round", methods=["POST"])
def start_round(lobby_id):
    from game_state import get_lobby
    from core import blackjack  # ✅ Assure-toi que c’est là

    lobby = get_lobby(lobby_id)
    print("=== START ROUND ===")
    print("LOBBY FOUND:", lobby)
    
    if not lobby:
        return {"error": "Lobby not found"}, 404

    table = lobby.get("table")
    players = lobby.get("players")

    print("TABLE:", table)
    print("PLAYERS:", players)

    blackjack.run_round(table, players)  # 👈 Cette ligne explose probablement

    return {"message": "Round started"}

@game_bp.route("/<lobby_id>/seat/<int:seat_id>/action", methods=["POST"])
def seat_action(lobby_id, seat_id):
    data = request.json
    action = data.get("action")
    lobby = get_lobby(lobby_id)
    if not lobby:
        return {"error": "Lobby not found"}, 404

    seat = lobby["table"].seats[seat_id]
    if not seat:
        return {"error": "Seat not assigned"}, 400

    if action == "hit":
        card = lobby["table"].deck.draw_card()
        seat.hit(card)
        return {
            "card": card,
            "hand": seat.hand,
            "value": calculate_hand(seat.hand),
            "status": seat.status
        }

    elif action == "stand":
        seat.stand()
        return {"status": seat.status}

    elif action == "double":
        try:
            card = lobby["table"].deck.draw_card()
            seat.double(card)
            return {
                "card": card,
                "hand": seat.hand,
                "value": calculate_hand(seat.hand),
                "status": seat.status
            }
        except Exception as e:
            return {"error": str(e)}, 400

    elif action == "split":
        try:
            split_seat = seat.split()
            split_seat.hit(lobby["table"].deck.draw_card())
            seat.hit(lobby["table"].deck.draw_card())
            lobby["table"].seats.append(split_seat)
            return {"msg": "Split successful"}
        except Exception as e:
            return {"error": str(e)}, 400

    return {"error": "Invalid action"}, 400

@game_bp.route("/<lobby_id>/seat/<int:seat_id>/bet", methods=["POST"])
def place_bet(lobby_id, seat_id):
    data = request.json
    amount = data.get("amount")
    player_name = data.get("player")
    side_bets = data.get("side_bets", {})

    lobby = get_lobby(lobby_id)
    if not lobby:
        return {"error": "Lobby not found"}, 404

    player = lobby["players"].get(player_name)
    if not player:
        return {"error": "Player not found"}, 404

    seat = lobby["table"].seats[seat_id]
    if not seat:
        return {"error": "Seat not assigned"}, 400

    if not player.can_afford(amount):
        return {"error": "Insufficient funds"}, 400

    seat.place_bet(amount)
    player.adjust_balance(-amount)

    for sb_type, sb_amt in side_bets.items():
        if player.can_afford(sb_amt):
            seat.add_side_bet(sb_type, sb_amt)
            player.adjust_balance(-sb_amt)

    return {"msg": f"Bet placed: ${amount}", "side_bets": side_bets}

def make_fake_decision(seat, dealer_upcard):
    """Return one of: 'hit', 'stand', 'double', 'split'."""
    hand = seat.hand
    total = calculate_hand(hand)
    up_rank = dealer_upcard[0]

    # Convert dealer upcard to value
    up_value = card_value(dealer_upcard)

    ranks = [card[0] for card in hand]

    # Pair logic
    if len(hand) == 2 and ranks[0] == ranks[1]:
        if ranks[0] in ['A', '8']:
            return "split"
        if ranks[0] == '9' and up_value in range(2, 7+1) or up_value in [8, 9]:
            return "split"
        if ranks[0] == '7' and up_value in range(2, 7+1):
            return "split"
        if ranks[0] in ['2', '3'] and up_value in range(2, 7+1):
            return "split"

    # Soft totals (has Ace)
    if 'A' in ranks and len(hand) == 2:
        second = ranks[0] if ranks[1] == 'A' else ranks[1]
        val = card_value((second, '♣'))

        if val >= 8:
            return "stand"
        elif val == 7:
            if 3 <= up_value <= 6:
                return "double"
            elif up_value in [2, 7, 8]:
                return "stand"
            else:
                return "hit"
        elif 4 <= val <= 6 and 4 <= up_value <= 6:
            return "double"
        else:
            return "hit"

    # Hard totals
    if total >= 17:
        return "stand"
    if 13 <= total <= 16 and 2 <= up_value <= 6:
        return "stand"
    if total == 12 and 4 <= up_value <= 6:
        return "stand"
    if total in [9, 10, 11]:
        if total == 11:
            return "double"
        if total == 10 and 2 <= up_value <= 9:
            return "double"
        if total == 9 and 3 <= up_value <= 6:
            return "double"
    return "hit"

def update_fake_strategy_results(table, results):
    for idx, result in results.items():
        seat = table.seats[idx]
        fake_name = seat.seat_id if isinstance(seat.seat_id, str) else None
        if fake_name in FAKE_STRATEGY:
            if result == "lose":
                FAKE_STRATEGY[fake_name]["current_bet"] *= 2
            else:
                FAKE_STRATEGY[fake_name]["current_bet"] = FAKE_STRATEGY[fake_name]["base_bet"]
