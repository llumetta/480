import time
import random
from itertools import combinations



class Card:
    def __init__(self, number, suit): #jack 11, queen 12, king 13, ace 14. #suits: hearts 1, clubs 2, diamonds 3, spades 4
        self.number = number
        self.suit = suit


class Hand:
    def __init__(self, card1, card2, card3, card4, card5):
        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
        self.card4 = card4
        self.card5 = card5
        self.handList = [card1, card2, card3, card4, card5]

    #calculates what rank your hand is from 0-9
    def calculate_score(self):
        numbers = [card.number for card in self.handList]
        suits = [card.suit for card in self.handList]

        num_counts = {n: numbers.count(n) for n in set(numbers)}
        counts = list(num_counts.values())
        unique_numbers = sorted(set(numbers))
        is_flush = len(set(suits)) == 1
        is_straight = (
                len(unique_numbers) == 5 and
                unique_numbers[-1] - unique_numbers[0] == 4
        )

        if {14, 2, 3, 4, 5}.issubset(set(numbers)):
            is_straight = True
            unique_numbers = [1, 2, 3, 4, 5]

        if is_straight and is_flush:
            if max(unique_numbers) == 14:
                return 9  # royal flush
            return 8  # straight flush
        if 4 in counts:
            return 7  # four of a kind
        if 3 in counts and 2 in counts:
            return 6  # full house
        if is_flush:
            return 5  # flush
        if is_straight:
            return 4  # straight
        if 3 in counts:
            return 3  # three of a kind
        if counts.count(2) == 2:
            return 2  # two pair
        if 2 in counts:
            return 1  # pair
        return 0  # high card

#pulls a random card not in dealt_cards
def pull_random_card(dealt_cards):
    all_numbers = range(2, 15)
    all_suits = range(1, 5)

    full_deck = {(number, suit) for number in all_numbers for suit in all_suits}

    dealt_set = {(card.number, card.suit) for card in dealt_cards}

    remaining = list(full_deck - dealt_set)

    if not remaining:
        raise ValueError("No cards left to draw.")

    number, suit = random.choice(remaining)
    return Card(number, suit)

#returns best score out of seven cards
def best_five_hand_score(seven_cards):
    best_score = -1
    for combo in combinations(seven_cards, 5):
        hand = Hand(*combo)
        score = hand.calculate_score()
        if score > best_score:
            best_score = score
    return best_score


#returns the 5 cards of your best hand of 7
def best_five_hand(seven_cards):
    best_hand = None
    best_score = -1

    for combo in combinations(seven_cards, 5):
        hand = Hand(*combo)
        score = hand.calculate_score()
        if score > best_score:
            best_score = score
            best_hand = combo
        elif score == best_score:
            # Tiebreaker for same score: prefer hand with higher cards
            sorted_hand = sorted([c.number for c in combo], reverse=True)
            sorted_best = sorted([c.number for c in best_hand], reverse=True)
            if sorted_hand > sorted_best:
                best_hand = combo

    return best_hand

#monte carlo simulation
def simulate_game(bot_hole, known_community, dealt_cards):
    opponent_hole = []
    for i in range(2):
        card = pull_random_card(dealt_cards)
        opponent_hole.append(card)
        dealt_cards.append(card)

    full_community = known_community[:]
    while len(full_community) < 5:
        card = pull_random_card(dealt_cards)
        full_community.append(card)
        dealt_cards.append(card)

    bot_full_hand = bot_hole + full_community
    opponent_full_hand = opponent_hole + full_community

    bot_score = best_five_hand_score(bot_full_hand)
    opponent_score = best_five_hand_score(opponent_full_hand)

    if (bot_score == opponent_score):
        bot_best = best_five_hand(bot_full_hand)
        opponent_best = best_five_hand(opponent_full_hand)

        bot_ranks = sorted([card.number for card in bot_best], reverse=True)
        opponent_ranks = sorted([card.number for card in opponent_best], reverse=True)

        for bot, opponent in zip(bot_ranks, opponent_ranks):
            if bot > opponent:
                return True
            else:
                return False
    else:
        return bot_score > opponent_score

#stay or fold based on many simulations
def monte_carlo_decision(bot_hole, known_community):
    start = time.time()
    wins = 0
    simulations = 0

    while time.time() - start < 10:
        dealt = bot_hole + known_community

        if simulate_game(bot_hole, known_community, dealt):
            wins += 1
        simulations += 1

    if (simulations > 0):
        win_rate = wins / simulations
    else:
        win_rate = 0
    return "stay" if win_rate >= 0.5 else "fold"


def print_cards(label, cards):
    print(f"{label}: " + ' '.join(f"|===Number: {card.number} Suit: {card.suit}===|" for card in cards))

community_cards = []
dealt_cards = []
if __name__ == '__main__':

    dealt_cards = []
    bot_hole = []
    bot_hole.append(pull_random_card(dealt_cards))
    bot_hole.append(pull_random_card(dealt_cards))
    dealt_cards.extend(bot_hole)

    print("\nBot's Pocket Hand:")
    print_cards("Bot Pocket", bot_hole)

    community_cards = []
    print("\nPre-Flop:")
    print_cards("Community", community_cards)
    decision = monte_carlo_decision(bot_hole, community_cards)
    print(f"Bot decision: {decision}")
    if decision == "fold":
        exit()

    for i in range(3):
        community_cards.append(pull_random_card(dealt_cards))
    dealt_cards.extend(community_cards)

    print("\nPre-Turn:")
    print_cards("Community", community_cards)
    decision = monte_carlo_decision(bot_hole, community_cards)
    print(f"Bot decision: {decision}")
    if decision == "fold":
        exit()

    turn_card = pull_random_card(dealt_cards)
    community_cards.append(turn_card)
    dealt_cards.append(turn_card)

    print("\nPre-River:")
    print_cards("Community", community_cards)
    decision = monte_carlo_decision(bot_hole, community_cards)
    print(f"Bot decision: {decision}")
    if decision == "fold":
        exit()

    river_card = pull_random_card(dealt_cards)
    community_cards.append(river_card)
    dealt_cards.append(river_card)

    opponent_hole = []
    opponent_hole.append(pull_random_card(dealt_cards))
    opponent_hole.append(pull_random_card(dealt_cards))

    print("\nPost-River:")
    print_cards("Final Community", community_cards)

    bot_full_hand = bot_hole + community_cards
    opponent_full_hand = opponent_hole + community_cards

    bot_score = best_five_hand_score(bot_full_hand)
    opponent_score = best_five_hand_score(opponent_full_hand)

    if (bot_score == opponent_score):
        bot_best = best_five_hand(bot_full_hand)
        opponent_best = best_five_hand(opponent_full_hand)

        bot_ranks = sorted([card.number for card in bot_best], reverse=True)
        opponent_ranks = sorted([card.number for card in opponent_best], reverse=True)

        for bot, opponent in zip(bot_ranks, opponent_ranks):
            if bot > opponent:
                final_result = True
            else:
                final_result = False
    else:
        final_result = (bot_score > opponent_score)

    print_cards("Opponent Hand", opponent_hole)
    if (final_result):
        print("Bot wins")
    else:
        print("Bot loses")



