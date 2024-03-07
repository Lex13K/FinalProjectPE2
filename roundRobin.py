def play_round(strategy1, strategy2, history1, history2):
    # Play one round of a game using two strategies and their respective histories
    move1 = strategy1(history2)  # Get move from strategy1, passing in opponent's history
    move2 = strategy2(history1)  # Get move from strategy2, passing in opponent's history
    return move1, move2  # Return both moves


def calculate_score(move1, move2):
    # Calculate the score for a single round based on the moves
    if move1 == 'C' and move2 == 'C':
        # If both cooperate, both get 3 points
        return 3, 3
    elif move1 == 'C' and move2 == 'D':
        # If strategy1 cooperates and strategy2 defects, strategy1 gets 0, strategy2 gets 5
        return 0, 5
    elif move1 == 'D' and move2 == 'C':
        # If strategy1 defects and strategy2 cooperates, strategy1 gets 5, strategy2 gets 0
        return 5, 0
    else:
        # If both defect, both get 1 point
        return 1, 1


def simulate_game(strategy1, strategy2, rounds):
    # Simulate a game for a number of rounds between two strategies
    history1, history2 = [], []  # Initialize history records for both strategies
    scores1, scores2 = [], []  # Initialize score records for both strategies
    for _ in range(rounds):
        # Play a round and update histories and scores
        move1, move2 = play_round(strategy1, strategy2, history1, history2)
        score1, score2 = calculate_score(move1, move2)
        history1.append(move1)  # Update strategy1's history
        history2.append(move2)  # Update strategy2's history
        scores1.append(score1)  # Update strategy1's score
        scores2.append(score2)  # Update strategy2's score
    return sum(scores1), sum(scores2)  # Return the total scores for both strategies


def round_robin_tournament(strategies, rounds):
    # Conduct a round-robin tournament with a list of strategies
    scores = {strategy.__name__: 0 for strategy in strategies}  # Initialize scores for each strategy
    for i, strategy1 in enumerate(strategies):
        for strategy2 in strategies[i:]:
            # Play a game between each pair of strategies and update scores
            score1, score2 = simulate_game(strategy1, strategy2, rounds)
            scores[strategy1.__name__] += score1  # Update strategy1's total score
            if strategy1 != strategy2:
                scores[strategy2.__name__] += score2  # Update strategy2's total score if not playing against itself
    return scores  # Return final scores from the tournament
