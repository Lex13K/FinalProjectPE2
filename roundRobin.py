from strategies import *

def play_round(strategy1, strategy2, history1, history2):
    move1 = strategy1(history2)
    move2 = strategy2(history1)
    return move1, move2

def calculate_score(move1, move2):
    if move1 == 'C' and move2 == 'C':
        return 3, 3
    elif move1 == 'C' and move2 == 'D':
        return 0, 5
    elif move1 == 'D' and move2 == 'C':
        return 5, 0
    else:
        return 1, 1

def simulate_game(strategy1, strategy2, rounds):
    history1, history2 = [], []
    scores1, scores2 = [], []
    for _ in range(rounds):
        move1, move2 = play_round(strategy1, strategy2, history1, history2)
        score1, score2 = calculate_score(move1, move2)
        history1.append(move1)
        history2.append(move2)
        scores1.append(score1)
        scores2.append(score2)
    return sum(scores1), sum(scores2)

def round_robin_tournament(strategies, rounds):
    scores = {strategy.__name__: 0 for strategy in strategies}
    for i, strategy1 in enumerate(strategies):
        for strategy2 in strategies[i:]:
            score1, score2 = simulate_game(strategy1, strategy2, rounds)
            scores[strategy1.__name__] += score1
            if strategy1 != strategy2:
                scores[strategy2.__name__] += score2
    return scores
