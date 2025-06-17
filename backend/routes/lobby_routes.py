# backend/routes/lobby_routes.py
"""
Author:Levraigitpush
fake_player_logic.py
-----------
Logic des bot
"""
from models.seat import Seat
from flask import Blueprint, request, jsonify
from game_state import create_lobby, get_lobby, add_fake_player

lobby_bp = Blueprint("lobby", __name__)

@lobby_bp.route("/create", methods=["POST"])
def create():
    data = request.json
    host_name = data.get("host_name")
    if not host_name:
        return {"error": "Missing host_name"}, 400

    lobby_id = create_lobby(host_name)
    return {"lobby_id": lobby_id}

@lobby_bp.route("/<lobby_id>", methods=["GET"])
def lobby_info(lobby_id):
    lobby = get_lobby(lobby_id)
    if not lobby:
        return {"error": "Lobby not found"}, 404

    players = list(lobby["players"].keys())
    return {"players": players}

@lobby_bp.route("/<lobby_id>/add_fake", methods=["POST"])
def add_fake(lobby_id):
    data = request.json
    fake_name = data.get("name")
    if not fake_name:
        return {"error": "Missing name"}, 400

    add_fake_player(lobby_id, fake_name)
    return {"msg": f"Fake player {fake_name} added"}

@lobby_bp.route("/<lobby_id>/assign_seat", methods=["POST"])
def assign_seat_route(lobby_id):

    data = request.json
    player_name = data.get("player")
    seat_index = data.get("seat_index")

    print(f"📥 /assign_seat → lobby={lobby_id}, player={player_name}, seat_index={seat_index}")

    lobby = get_lobby(lobby_id)
    if not lobby:
        print("❌ Lobby not found")
        return {"error": "Lobby not found"}, 404

    players = lobby.get("players", {})
    table = lobby.get("table")

    if player_name not in players:
        print(f"❌ Player '{player_name}' not in lobby.players: {list(players.keys())}")
        return {"error": "Player not found"}, 404

    if not isinstance(seat_index, int) or not (0 <= seat_index < 7):
        print(f"❌ Invalid seat index: {seat_index}")
        return {"error": "Invalid seat index"}, 400

    if table.seats[seat_index]:
        print(f"❌ Seat {seat_index} is already occupied by: {table.seats[seat_index].seat_id}")
        return {"error": "Seat already occupied"}, 400

    # Assign the seat
    seat_obj = Seat(seat_id=seat_index)
    table.assign_seat(players[player_name], seat_index, seat_obj)

    print(f"✅ Player '{player_name}' assigned to seat {seat_index}")
    return {"msg": f"{player_name} assigned to seat {seat_index + 1}"}