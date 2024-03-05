import random

# Starting with defining several functions that will be used as strategies

def tit_for_tat(own_history, opponent_history):
    if not opponent_history:
        return 'C'  # Cooperate on the first move
    else:
        return opponent_history[-1]  # Mimic the opponent's last move

def suspicious_tit_for_tat(own_history, opponent_history):
    if not opponent_history:
        return 'D'  # Defect on the first move
    else:
        return opponent_history[-1]  # Then mimic the opponent's last move

def tit_for_two_tats(own_history, opponent_history):
    if len(opponent_history) < 2 or opponent_history[-1] == 'C' or opponent_history[-2] == 'C':
        return 'C'  # Cooperate by default and if not two consecutive defections
    else:
        return 'D'  # Defect if the opponent defected in the last two rounds

def always_defect(own_history, opponent_history):
    return 'D'  # Always defect

def pavlov(own_history, opponent_history):
    if not opponent_history or opponent_history[-1] == 'C':
        return 'C'  # Cooperate by default and if last round was cooperation from the opponent
    else:
        return 'D' if opponent_history[-1] == 'D' else 'C'

def tester(own_history, opponent_history):
    if not opponent_history:
        return 'C'  # Cooperate on the first move
    elif len(opponent_history) == 1:
        return 'D'  # Defect on the second move
    elif opponent_history[-1] == 'D':
        return tit_for_tat(own_history, opponent_history)  # Switch to Tit for Tat if opponent defects
    else:
        return 'D'  # Otherwise, keep defecting

def joss(own_history, opponent_history):
    if not opponent_history:
        return 'C'  # Cooperate on the first move
    else:
        if random.random() < 0.10:  # 10% chance of defecting instead of mimicking
            return 'D'
        else:
            return opponent_history[-1]

def grudger(own_history, opponent_history):
    if 'D' in opponent_history:
        return 'D'  # Defect forever after the first defection by the opponent
    else:
        return 'C'  # Cooperate until then

def soft_majority(own_history, opponent_history):
    if opponent_history.count('D') > opponent_history.count('C'):
        return 'D'
    else:
        return 'C'

def hard_majority(own_history, opponent_history):
    if not opponent_history:
        return 'D'  # Start by defecting
    if opponent_history.count('D') > opponent_history.count('C'):
        return 'D'
    else:
        return 'C'

def prober(own_history, opponent_history):
    # In the first two moves, act according to the prober's strategy
    if len(own_history) < 2:
        if len(own_history) == 0:
            return 'C'  # Cooperate on the first move
        else:
            return 'D'  # Defect on the second move
    else:
        # After the first two moves, switch to using a Tit for Tat strategy
        # Now correctly passing both own_history and opponent_history
        return tit_for_tat(own_history, opponent_history)



def random_strategy(own_history, opponent_history):
    return random.choice(['C', 'D'])


def CHATGPT(own_history, opponent_history):
    # Start with cooperation
    if not opponent_history:
        return 'C'

    # Calculate the tendency to defect
    defect_rate = opponent_history.count('D') / len(opponent_history)

    # Adapt strategy based on opponent's behavior
    if len(opponent_history) > 1:
        # If opponent defects too much, become cautious
        if defect_rate > 0.5:
            return 'D' if opponent_history[-1] == 'C' else 'C'
        # Forgiveness if recently defected twice in a row
        elif len(opponent_history) >= 3 and opponent_history[-2:] == ['D', 'D']:
            return 'C'
        # Regular Tit for Tat otherwise
        else:
            return opponent_history[-1]
    else:
        # Mimic the last move initially
        return opponent_history[-1]

def CHATGPT2(own_history, opponent_history):
    # Calculate the defection rate
    total_moves = len(opponent_history)
    defections = opponent_history.count('D')
    defection_rate = defections / total_moves if total_moves else 0

    # Start with cooperation
    if not opponent_history:
        return 'C'

    # Adapt forgiveness based on defection rate
    if defection_rate < 0.3:
        # Be more forgiving if defection rate is low
        if total_moves >= 2 and opponent_history[-2:] == ['D', 'C']:
            return 'C'  # Forgive if the opponent just cooperated after a defection
    elif defection_rate >= 0.3 and defection_rate < 0.6:
        # Standard Tit for Two Tats behavior for moderate defection rates
        if total_moves < 2 or opponent_history[-1] == 'C' or opponent_history[-2] == 'C':
            return 'C'
        else:
            return 'D'
    else:
        # Less forgiving if the opponent defects frequently
        return 'D' if defections > 2 and opponent_history[-1] == 'D' else 'C'

    # Default to mimicking the opponent's last move
    return opponent_history[-1]


def CHATGPT3(own_history, opponent_history, rounds=200):
    current_round = len(own_history) + 1
    defection_rate = opponent_history.count('D') / current_round if current_round > 1 else 0

    # Early Game: Start with Tit for Tat
    if current_round <= 50:
        return 'C' if current_round == 1 else opponent_history[-1]

    # Mid Game: Adapt based on opponent's behavior
    elif current_round <= 150:
        if defection_rate > 0.5:
            # If opponent defects a lot, switch to Grudger
            return 'D' if 'D' in opponent_history[-10:] else 'C'  # Look at the last 10 moves
        else:
            # Otherwise, continue with Tit for Tat
            return opponent_history[-1]

    # Late Game: Strategy adjustment based on current score
    else:
        own_score = sum([calculate_score(own, opp)[0] for own, opp in zip(own_history, opponent_history)])
        opponent_score = sum([calculate_score(own, opp)[1] for own, opp in zip(own_history, opponent_history)])
        if own_score > opponent_score:
            # If leading, play it safe
            return 'C' if defection_rate < 0.3 else 'D'
        else:
            # If behind or close, take calculated risks
            return 'D' if (rounds - current_round) % 3 == 0 else opponent_history[-1]  # Defect every third round

# Helper function to calculate the score based on the move pair, assuming the function exists in the context
def calculate_score(move1, move2):
    if move1 == 'C' and move2 == 'C':
        return (3, 3)
    elif move1 == 'C' and move2 == 'D':
        return (0, 5)
    elif move1 == 'D' and move2 == 'C':
        return (5, 0)
    else:
        return (1, 1)

def play_round(strategy1, strategy2, history1, history2):
    move1 = strategy1(history1, history2)
    move2 = strategy2(history2, history1)
    return move1, move2


def calculate_score(move1, move2):
    if move1 == 'C' and move2 == 'C':
        return (3, 3)
    elif move1 == 'C' and move2 == 'D':
        return (0, 5)
    elif move1 == 'D' and move2 == 'C':
        return (5, 0)
    else:
        return (1, 1)

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

strategies = [tit_for_tat, suspicious_tit_for_tat, tit_for_two_tats,
              always_defect,pavlov, tester, joss, grudger,
              soft_majority, hard_majority, prober, random_strategy,
              CHATGPT, CHATGPT2, CHATGPT3]

# Function to run a round-robin tournament
def round_robin_tournament(strategies, rounds=200):
    scores = {strategy.__name__: 0 for strategy in strategies}  # Initialize scores for each strategy
    for i, strategy1 in enumerate(strategies):
        for strategy2 in strategies[i:]:  # Include self-play by starting from current index
            score1, score2 = simulate_game(strategy1, strategy2, rounds)
            scores[strategy1.__name__] += score1
            if strategy1 != strategy2:
                scores[strategy2.__name__] += score2  # Add score to the second strategy only if it's a different one
    return scores

# Function to simulate the game, calculate score, and play round remain unchanged from your initial setup...

# Run the tournament
tournament_scores = round_robin_tournament(strategies, 200)

# Print the results
for strategy, score in sorted(tournament_scores.items(), key=lambda item: item[1], reverse=True):
    print(f"{strategy}: {score}")

