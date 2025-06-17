"""
blackjack.py
-------------
Main game engine logic for running Blackjack rounds.
Controls dealing, turn order, side bets, dealer logic, and payouts.
"""

from models.deck import calculate_hand, display_hand_with_value
from core.side_bets import (
    check_perfect_pair,
    check_21_plus_3,
    check_lucky_lucky,
    check_buster,
    check_royal_jack
)

def run_round(table, players):
    """Runs one round of Blackjack."""
    print("\n🎲 Starting new round...\n")
    table.start_round()

    # Deal initial 2 cards to each active seat
    for _ in range(2):
        for seat in table.get_active_seats():
            seat.hit(table.deck.draw_card())
        table.dealer.add_card(table.deck.draw_card())

    # Display dealer's upcard
    dealer_up = table.dealer.hand[0]
    print(f"🃏 Dealer shows: {dealer_up[0]}{dealer_up[1]}")

    # Process side bets BEFORE player actions
    for seat in table.get_active_seats():
        print(f"\n💺 Seat {seat.seat_id} Hand: {display_hand_with_value(seat.hand)}")
        for bet_type, amount in seat.side_bets.items():
            payout = 0
            if bet_type == 'perfect_pair':
                payout = check_perfect_pair(seat.hand)
            elif bet_type == '21+3':
                payout = check_21_plus_3(seat.hand, dealer_up)
            elif bet_type == 'lucky_lucky':
                payout = check_lucky_lucky(seat.hand, dealer_up)
            elif bet_type == 'royal_jack':
                payout = check_royal_jack(seat.hand)
            if payout:
                print(f"💸 {bet_type} WON! +{payout}x payout")
            else:
                print(f"❌ {bet_type} lost")

    # Player decisions
    for seat in table.get_active_seats():
        print(f"\n➡️ Turn for Seat {seat.seat_id}")
        while seat.status == "active":
            print(f"Your hand: {display_hand_with_value(seat.hand)}")
            move = input("Action [hit/stand/double/split]? ").strip().lower()
            if move == "hit":
                seat.hit(table.deck.draw_card())
                if seat.status == "busted":
                    print("💥 Busted!")
                    break
            elif move == "stand":
                seat.stand()
                break
            elif move == "double":
                try:
                    seat.double(table.deck.draw_card())
                    print("💰 Doubled and one card drawn.")
                    break
                except Exception as e:
                    print(f"🚫 {e}")
            elif move == "split":
                try:
                    split_seat = seat.split()
                    split_seat.hit(table.deck.draw_card())
                    seat.hit(table.deck.draw_card())
                    table.seats.append(split_seat)
                    print(f"🔀 Split successful. Now playing both hands.")
                except Exception as e:
                    print(f"🚫 {e}")
            else:
                print("❓ Invalid action. Try again.")

    # Dealer's turn
    print("\n🎮 Dealer's hand:")
    table.dealer.play_turn(table.deck)
    print(display_hand_with_value(table.dealer.hand))

    dealer_bust = table.dealer.is_busted()
    dealer_blackjack = table.dealer.has_blackjack()

    # Final resolution
    for seat in table.get_active_seats():
        result = "undecided"
        hand_value = calculate_hand(seat.hand)
        player_blackjack = seat.is_blackjack()

        if seat.status == "busted":
            result = "lose"
        elif player_blackjack and not dealer_blackjack:
            result = "blackjack"
        elif dealer_blackjack and not player_blackjack:
            result = "lose"
        elif dealer_bust:
            result = "win"
        else:
            dealer_value = calculate_hand(table.dealer.hand)
            if hand_value > dealer_value:
                result = "win"
            elif hand_value < dealer_value:
                result = "lose"
            else:
                result = "push"

        print(f"\n🧾 Seat {seat.seat_id} Result: {result.upper()}")

        # Evaluate buster side bet
        if 'buster' in seat.side_bets:
            buster_payout = check_buster(table.dealer.hand, dealer_bust, player_blackjack)
            if buster_payout:
                print(f"💥 BUSTER BET WON! +{buster_payout}x")
            else:
                print("❌ Buster bet lost")
