"""
Author : Levraigitpush
chart_ai.py
-----------
Implements Blackjack Basic Strategy Chart logic.
Used by fake players to decide actions: hit, stand, double, split.
"""

from models.deck import calculate_hand, card_value

def make_fake_decision(seat, dealer_upcard):
    """
    Determine the best action for the fake player using standard Blackjack strategy.
    Actions: 'hit', 'stand', 'double', 'split'
    """
    hand = seat.hand
    total = calculate_hand(hand)
    dealer_value = card_value(dealer_upcard)

    ranks = [card[0] for card in hand]

    # ----- PAIR STRATEGY -----
    if len(hand) == 2 and ranks[0] == ranks[1]:
        pair_rank = ranks[0]
        if pair_rank in ['A', '8']:
            return 'split'
        if pair_rank == '9' and (2 <= dealer_value <= 6 or dealer_value in [8, 9]):
            return 'split'
        if pair_rank == '7' and 2 <= dealer_value <= 7:
            return 'split'
        if pair_rank in ['2', '3'] and 2 <= dealer_value <= 7:
            return 'split'
        if pair_rank == '6' and 2 <= dealer_value <= 6:
            return 'split'
        if pair_rank == '4' and dealer_value in [5, 6]:
            return 'split'
        if pair_rank == '5':
            pass  # treat as hard 10
        else:
            return 'stand'

    # ----- SOFT HAND STRATEGY (contains Ace) -----
    if 'A' in ranks and len(hand) == 2:
        other_card = [r for r in ranks if r != 'A'][0] if ranks.count('A') == 1 else 'A'
        second_val = card_value((other_card, '♠'))  # suit doesn't matter

        # Soft 19 or 20 (A,8) or (A,9)
        if second_val >= 8:
            return 'stand'

        if second_val == 7:
            if 3 <= dealer_value <= 6:
                return 'double'
            elif dealer_value in [2, 7, 8]:
                return 'stand'
            else:
                return 'hit'

        if 4 <= second_val <= 6:
            if 4 <= dealer_value <= 6:
                return 'double'
            else:
                return 'hit'

        if second_val <= 3:
            return 'hit'

    # ----- HARD TOTAL STRATEGY -----
    if total >= 17:
        return 'stand'
    if 13 <= total <= 16:
        if 2 <= dealer_value <= 6:
            return 'stand'
        else:
            return 'hit'
    if total == 12:
        if 4 <= dealer_value <= 6:
            return 'stand'
        else:
            return 'hit'
    if total == 11:
        return 'double'
    if total == 10 and 2 <= dealer_value <= 9:
        return 'double'
    if total == 9 and 3 <= dealer_value <= 6:
        return 'double'
    if total <= 8:
        return 'hit'

    return 'stand'  # Fallback (shouldn't be hit)
