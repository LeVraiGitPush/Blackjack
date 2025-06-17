"""
side_bets.py
-------------
Provides logic for calculating side bet outcomes based on Blackjack hands.
"""

from collections import Counter

# 🃏 Perfect Pair
def check_perfect_pair(hand):
    """
    hand: list of 2 cards
    Returns: multiplier or 0
    """
    if len(hand) != 2:
        return 0
    r1, s1 = hand[0]
    r2, s2 = hand[1]
    
    if r1 != r2:
        return 0

    if s1 == s2:
        return 25  # Perfect pair
    elif s1 in '♥♦' and s2 in '♥♦' or s1 in '♠♣' and s2 in '♠♣':
        return 12  # Colored pair
    else:
        return 6  # Mixed pair

# ♠️ 21+3
def check_21_plus_3(player_hand, dealer_card):
    """
    Evaluate 21+3 combination with player's 2 cards + dealer's 1 card.
    Returns: payout multiplier or 0
    """
    if len(player_hand) < 2 or not dealer_card:
        return 0
    
    cards = player_hand + [dealer_card]
    ranks = [card[0] for card in cards]
    suits = [card[1] for card in cards]
    
    is_flush = len(set(suits)) == 1
    sorted_ranks = sorted([_rank_value(r) for r in ranks])
    is_straight = sorted_ranks == list(range(min(sorted_ranks), max(sorted_ranks)+1))
    rank_count = Counter(ranks)

    if len(rank_count) == 1 and is_flush:
        return 100  # Suited trips
    elif is_straight and is_flush:
        return 40  # Straight flush
    elif len(rank_count) == 1:
        return 30  # Trips
    elif is_straight:
        return 10  # Straight
    elif is_flush:
        return 5  # Flush
    return 0

def _rank_value(rank):
    order = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
    return order.get(rank, 0)

# 🍀 Lucky Lucky
def check_lucky_lucky(player_hand, dealer_card):
    if len(player_hand) < 2 or not dealer_card:
        return 0

    cards = player_hand + [dealer_card]
    total = sum(_card_blackjack_value(c[0]) for c in cards)
    suits = [c[1] for c in cards]
    ranks = [c[0] for c in cards]
    is_suited = len(set(suits)) == 1
    rank_values = sorted([_rank_value(r) for r in ranks])

    if ranks.count('7') == 3 and is_suited:
        return 200
    elif rank_values == [6, 7, 8] and is_suited:
        return 100
    elif ranks.count('7') == 3:
        return 50
    elif rank_values == [6, 7, 8]:
        return 30
    elif total == 21 and is_suited:
        return 10
    elif total == 21:
        return 3
    elif total in [19, 20]:
        return 2
    return 0

def _card_blackjack_value(rank):
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    return int(rank)

# 💥 Buster Blackjack
def check_buster(dealer_hand, dealer_busted, player_blackjack):
    """
    dealer_hand: list of cards in dealer's hand
    dealer_busted: boolean
    player_blackjack: boolean
    """
    if not dealer_busted:
        return 0
    
    card_count = len(dealer_hand)

    if card_count >= 8 and player_blackjack:
        return 2000
    elif card_count == 7 and player_blackjack:
        return 800
    elif card_count >= 8:
        return 250
    elif card_count == 7:
        return 50
    elif card_count == 6:
        return 18
    elif card_count == 5:
        return 4
    elif card_count in [3, 4]:
        return 2
    return 0

# 👑 Royal Jack
def check_royal_jack(hand):
    """
    Check for royal jack combos in the hand.
    Only valid on first 2 or 3 cards.
    """
    jacks = [c for c in hand if c[0] == 'J']
    if len(jacks) < 2:
        return 0

    suits = [s for _, s in jacks]

    if len(jacks) == 3 and len(set(suits)) == 1:
        return 600
    elif len(jacks) == 3:
        return 250
    elif len(jacks) == 2 and jacks[0][1] == jacks[1][1] == '♦':
        return 150
    elif len(jacks) == 2 and jacks[0][1] == jacks[1][1]:
        return 100
    elif len(jacks) == 2:
        return 35
    return 0
