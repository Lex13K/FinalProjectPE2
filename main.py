import random
import strategies
from roundRobin import round_robin_tournament
from evolutionary import evolutionary_tournament

# Function to list all callable strategy functions from the strategies module, excluding magic methods
def list_strategies():
    return [getattr(strategies, func) for func in dir(strategies) if callable(getattr(strategies, func)) and not func.startswith("__")]

# Function to prompt the user to select the type of tournament to run
def select_tournament_type():
    print("Select the type of tournament you want to run:")
    print("1. Round Robin Tournament")
    print("2. Evolutionary Tournament")
    while True:
        try:
            choice = int(input("Enter your choice (1 or 2): "))
            if choice in [1, 2]:
                return choice
            else:
                print("Please enter 1 or 2.")
        except ValueError:
            print("Please enter a valid integer.")


# Function to get the number of rounds for the Round Robin Tournament, with optional error element
def get_rounds_input():
    while True:
        try:
            base_rounds = int(input("Enter the number of rounds for the Round Robin Tournament: "))
            if base_rounds > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")
    while True:
        error_option = input("Do you want to include a 1% error element? (yes/no): ").strip().lower()
        if error_option in ['yes', 'no']:
            if error_option == 'yes':
                error_margin = round(base_rounds * 0.01)
                random_adjustment = random.randint(-error_margin, error_margin)
                adjusted_rounds = base_rounds + random_adjustment
                print(f"Actual number of rounds to be played (after adding randomness): {adjusted_rounds}")
            else:
                adjusted_rounds = base_rounds
                print(f"Actual number of rounds to be played: {adjusted_rounds}")
            break
        else:
            print("Please enter 'yes' or 'no'.")
    return adjusted_rounds

# Function to decide if a preset should be used for the Evolutionary Tournament and which one
def get_evolutionary_tournament_preset():
    while True:
        try:
            print("Do you want to use a preset for the Evolutionary Tournament?: ")
            print("0. Pick my own values")
            print("1. Larger Simulation")
            print("2. Smaller Simulation")
            preset_choice = int(input("Enter your choice: "))
            if preset_choice in [0, 1, 2]:
                if preset_choice == 0:
                    return get_evolutionary_tournament_input()
                elif preset_choice == 1:
                    return 50, 1000, 50, 50, 0.05, 0.01
                elif preset_choice == 2:
                    return 10, 100, 10, 20, 0.1, 0.01
            else:
                print("Please enter 0, 1, or 2.")
        except ValueError:
            print("Please enter a valid integer.")


# Function to manually input parameters for the Evolutionary Tournament
def get_evolutionary_tournament_input():
    while True:
        try:
            generations = int(input("Enter the number of generations for the Evolutionary Tournament: "))
            if generations <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")
    while True:
        try:
            total_population = int(input("Enter the total population size for the Evolutionary Tournament: "))
            if total_population <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")
    while True:
        try:
            group_size = int(input("Enter the group size for the Evolutionary Tournament: "))
            if group_size <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")
    while True:
        try:
            rounds = int(input("Enter the number of rounds per group for the Evolutionary Tournament: "))
            if rounds <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")
    while True:
        try:
            elimination_rate = float(input("Enter the percentage (as a decimal) of low performers to be replaced each generation: "))
            if not 0 <= elimination_rate <= 1:
                raise ValueError
            break
        except ValueError:
            print("Please enter a decimal number between 0 and 1.")
    while True:
        try:
            mutation_chance = float(input("Enter the chance of mutation (0-1, where 0.01 represents a 1% chance): "))
            if not 0 <= mutation_chance <= 1:
                raise ValueError
            break
        except ValueError:
            print("Please enter a decimal number between 0 and 1.")
    return generations, total_population, group_size, rounds, elimination_rate, mutation_chance

# Main function to run the selected tournament type
def main():
    all_strategies = list_strategies()
    tournament_type = select_tournament_type()

    if tournament_type == 1:
        rounds = get_rounds_input()
        print("Running Round Robin Tournament...")
        results = round_robin_tournament(list_strategies(), rounds)
        for strategy, score in sorted(results.items(), key=lambda item: item[1], reverse=True):
            print(f"{strategy}: {score}")  # Display the scores of strategies
    elif tournament_type == 2:
        evolutionary_inputs = get_evolutionary_tournament_preset()
        print(f"Running Evolutionary Tournament with {evolutionary_inputs[1]} individuals, group size of {evolutionary_inputs[2]}, for {evolutionary_inputs[0]} generations, with mutation set to {evolutionary_inputs[5]}...")
        evolutionary_tournament(*evolutionary_inputs)
    else:
        print("Invalid selection.")  # Handle invalid tournament type selection

main()  # MOST IMPORTANT LINE OF THE CODE :D
