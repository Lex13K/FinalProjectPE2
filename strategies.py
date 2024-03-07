import random
random.seed(2024)
# Cooperates on the first move, then mimics the opponent's last move.
def tit_for_tat(opponent_history):
    return 'C' if not opponent_history else opponent_history[-1]
# Defects on the first move, then mimics the opponent's last move.
def suspicious_tit_for_tat(opponent_history):
    return 'D' if not opponent_history else opponent_history[-1]
# Cooperates unless the opponent has defected in the last two rounds.
def tit_for_two_tats(opponent_history):
    return 'C' if len(opponent_history) < 2 or opponent_history[-1] == 'C' or opponent_history[-2] == 'C' else 'D'
# Always defects.
def always_defect(opponent_history):
    return 'D'
# Cooperates on the first move, then defects only if the opponent defected in the last round.
def pavlov(opponent_history):
    return 'C' if not opponent_history or opponent_history[-1] == 'C' else 'D'
# Cooperates on the first move, defects on the second, then mimics the opponent's last move if they defected last.
def tester(opponent_history):
    if not opponent_history:
        return 'C'
    elif len(opponent_history) == 1:
        return 'D'
    else:
        return 'D' if opponent_history[-1] == 'D' else 'C'
# Cooperates on the first move, then defects with a 10% chance, otherwise mimics the opponent's last move.
def joss(opponent_history):
    if not opponent_history:
        return 'C'
    else:
        return 'D' if random.random() < 0.10 else opponent_history[-1]
# Defects forever after the first defection by the opponent.
def grudger(opponent_history):
    return 'D' if 'D' in opponent_history else 'C'
# Defects if the opponent has defected more than cooperated, otherwise cooperates.
def soft_majority(opponent_history):
    return 'D' if opponent_history.count('D') > opponent_history.count('C') else 'C'
# Defects unless the opponent has cooperated more than defected.
def hard_majority(opponent_history):
    return 'D' if not opponent_history or opponent_history.count('D') >= opponent_history.count('C') else 'C'
# Cooperates on the first move, defects on the second, then follows a tit_for_tat strategy.
def prober(opponent_history):
    if len(opponent_history) < 2:
        return 'C' if len(opponent_history) == 0 else 'D'
    else:
        return 'C' if opponent_history[-1] == 'C' else 'D'
# Chooses randomly between cooperating and defecting.
def random_strategy(opponent_history):
    return random.choice(['C', 'D'])
