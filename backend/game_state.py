# backend/game_state.py

import uuid
from models.table import Table
from models.player import Player

# In-memory storage of lobbies (can later be Redis or DB)
LOBBIES = {}
FAKE_STRATEGY = {}  # Map fake name -> strategy state

def create_lobby(host_name):
    """Create a new lobby with a host player"""
    lobby_id = str(uuid.uuid4())[:8]
    player = Player(name=host_name)
    table = Table()
    LOBBIES[lobby_id] = {
        "table": table,
        "host": player,
        "players": {player.name: player}
    }
    return lobby_id

def get_lobby(lobby_id):
    """Return lobby data"""
    return LOBBIES.get(lobby_id)

def add_fake_player(lobby_id, fake_name, base_bet=10):
    """Add a fake player to the lobby"""
    fake = Player(name=fake_name)
    lobby = get_lobby(lobby_id)
    if fake.name not in lobby["players"]:
        lobby["players"][fake.name] = fake
    FAKE_STRATEGY[fake_name] = {
        "base_bet": base_bet,
        "current_bet": base_bet,
        "last_result": None,  # 'win' or 'lose'
    }

