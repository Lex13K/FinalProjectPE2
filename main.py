import random
import strategies
from roundRobin import round_robin_tournament
from evolutionary import evolutionary_tournament

def list_strategies():
    return [getattr(strategies, func) for func in dir(strategies) if callable(getattr(strategies, func)) and not func.startswith("__")]

def select_tournament_type():
    print("Select the type of tournament you want to run:")
    print("1. Round Robin Tournament")
    print("2. Evolutionary Tournament")
    choice = input("Enter your choice (1 or 2): ")
    return int(choice)

def get_rounds_input():
    base_rounds = int(input("Enter the number of rounds for the Round Robin Tournament: "))
    error_option = input("Do you want to include a 1% error element? (yes/no): ").strip().lower()
    if error_option == 'yes':
        error_margin = round(base_rounds * 0.01)
        random_adjustment = random.randint(-error_margin, error_margin)
        adjusted_rounds = base_rounds + random_adjustment
        print(f"Actual number of rounds to be played (after adding randomness): {adjusted_rounds}")
    else:
        adjusted_rounds = base_rounds
        print(f"Actual number of rounds to be played: {adjusted_rounds}")
    return adjusted_rounds

def get_evolutionary_tournament_input():
    generations = int(input("Enter the number of generations for the Evolutionary Tournament: "))
    total_population = int(input("Enter the total population size for the Evolutionary Tournament: "))
    group_size = int(input("Enter the group size for the Evolutionary Tournament: "))
    rounds = int(input("Enter the number of rounds per group for the Evolutionary Tournament: "))
    elimination_rate = float(input("Enter the percentage (as a decimal) of low performers to be replaced each generation: "))
    mutation_chance = float(input("Enter the chance of mutation (0-1, where 0.01 represents a 1% chance): "))
    return generations, total_population, group_size, rounds, elimination_rate, mutation_chance


def main():
    all_strategies = list_strategies()
    tournament_type = select_tournament_type()

    if tournament_type == 1:
        rounds = get_rounds_input()
        print("Running Round Robin Tournament...")
        results = round_robin_tournament(all_strategies, rounds)
        for strategy, score in sorted(results.items(), key=lambda item: item[1], reverse=True):
            print(f"{strategy}: {score}")
    elif tournament_type == 2:
        generations, total_population, group_size, rounds, elimination_rate, mutation_chance = get_evolutionary_tournament_input()
        print(f"Running Evolutionary Tournament with {total_population} individuals, group size of {group_size}, for {generations} generations, with mutation set to {mutation_chance}...")
        evolutionary_tournament(total_population, group_size, rounds, generations, elimination_rate, mutation_chance)
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()