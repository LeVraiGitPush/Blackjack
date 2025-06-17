"""
main.py
---------
Entry point CLI for Blackjack Casino game.
Allows players to sit, place bets, and play rounds.
"""

from models.player import Player
from models.seat import Seat
from models.table import Table
import blackjack

def get_int(prompt, min_val=0, max_val=999999):
    """Helper input to safely get an integer."""
    while True:
        try:
            val = int(input(prompt))
            if min_val <= val <= max_val:
                return val
        except ValueError:
            pass
        print("🚫 Invalid input. Enter a number.")

def main():
    print("🎰 Welcome to Blackjack Casino CLI")
    table = Table()
    players = []

    # Create players
    num_players = get_int("Number of players (1-4): ", 1, 4)
    for i in range(num_players):
        name = input(f"Enter name for Player {i + 1}: ")
        players.append(Player(name))

    # Assign seats
    for player in players:
        print(f"\n🎮 {player.name}, choose your seats (1-7), max 3 (comma-separated):")
        chosen = input("Seats: ")
        indices = list(map(int, chosen.split(',')))
        for idx in indices[:3]:
            seat_obj = Seat(seat_id=idx)
            table.assign_seat(player, idx - 1, seat_obj)

    while True:
        # Place bets
        for player in players:
            for seat in player.seats:
                print(f"\n💰 {player.name} - Seat {seat.seat_id}")
                bet = get_int("Main bet: $", 1)
                if not player.can_afford(bet):
                    print("🚫 Not enough balance.")
                    continue
                seat.place_bet(bet)
                player.adjust_balance(-bet)

                # Side bets
                for sb in ['perfect_pair', '21+3', 'lucky_lucky', 'royal_jack', 'buster']:
                    side_bet = input(f"Side bet on {sb}? (amount or 0): ")
                    try:
                        amt = int(side_bet)
                        if amt > 0:
                            if player.can_afford(amt):
                                seat.add_side_bet(sb, amt)
                                player.adjust_balance(-amt)
                            else:
                                print("🚫 Insufficient funds for side bet.")
                    except:
                        pass

        # Run game
        blackjack.run_round(table, players)

        # Show balances
        print("\n💳 Player Balances:")
        for player in players:
            print(f"{player.name}: ${player.balance}")

        # Next round?
        again = input("\nPlay another round? (y/n): ").strip().lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()
