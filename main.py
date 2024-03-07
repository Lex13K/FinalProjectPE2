from strategies import *
from roundRobin import round_robin_tournament
from evolutionary import evolutionaryTournament

strategyFunctions = [
    tit_for_tat, suspicious_tit_for_tat, tit_for_two_tats, always_defect,
    pavlov, tester, joss, grudger, soft_majority, hard_majority, prober,
    random_strategy
]


def selectTournamentType():
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


def getRoundsInput():
    while True:
        try:
            baseRounds = int(input("Enter the number of rounds for the Round Robin Tournament: "))
            if baseRounds > 0:
                break
            else:
                print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")
    while True:
        errorOption = input("Do you want to include a 1% error element? (yes/no): ").strip().lower()
        if errorOption in ['yes', 'no']:
            if errorOption == 'yes':
                errorMargin = round(baseRounds * 0.01)
                randomAdjustment = random.randint(-errorMargin, errorMargin)
                adjustedRounds = baseRounds + randomAdjustment
                print(f"Actual number of rounds to be played (after adding randomness): {adjustedRounds}")
            else:
                adjustedRounds = baseRounds
                print(f"Actual number of rounds to be played: {adjustedRounds}")
            break
        else:
            print("Please enter 'yes' or 'no'.")
    return adjustedRounds


def getEvolutionaryTournamentPreset():
    print("Do you want to use a preset for the Evolutionary Tournament?: ")
    print("0. Pick my own values")
    print("1. Larger Simulation")
    print("2. Smaller Simulation")
    while True:
        try:
            presetChoice = int(input("Enter your choice: "))
            if presetChoice in [0, 1, 2]:
                if presetChoice == 0:
                    return getEvolutionaryTournamentInput()
                elif presetChoice == 1:
                    return 50, 1000, 50, 50, 0.05, 0.01
                elif presetChoice == 2:
                    return 10, 100, 10, 20, 0.1, 0.01
            else:
                print("Please enter 0, 1, or 2.")
        except ValueError:
            print("Please enter a valid integer.")


def getEvolutionaryTournamentInput():
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
            totalPopulation = int(input("Enter the total population size for the Evolutionary Tournament: "))
            if totalPopulation <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a positive integer.")
    while True:
        try:
            groupSize = int(input("Enter the group size for the Evolutionary Tournament: "))
            if groupSize <= 0:
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
            eliminationRate = float(input("Enter the percentage (as a decimal) of low performers to be replaced each generation: "))
            if not 0 <= eliminationRate <= 1:
                raise ValueError
            break
        except ValueError:
            print("Please enter a decimal number between 0 and 1.")
    while True:
        try:
            mutationChance = float(input("Enter the chance of mutation (0-1, where 0.01 represents a 1% chance): "))
            if not 0 <= mutationChance <= 1:
                raise ValueError
            break
        except ValueError:
            print("Please enter a decimal number between 0 and 1.")
    return generations, totalPopulation, groupSize, rounds, eliminationRate, mutationChance


def main():
    tournamentType = selectTournamentType()

    if tournamentType == 1:
        rounds = getRoundsInput()
        print("Running Round Robin Tournament...")
        results = round_robin_tournament(strategyFunctions, rounds)
        for strategy, score in sorted(results.items(), key=lambda item: item[1], reverse=True):
            print(f"{strategy}: {score}")  # Display the scores of strategies
    elif tournamentType == 2:
        evolutionaryInputs = getEvolutionaryTournamentPreset()
        print(f"Running Evolutionary Tournament with {evolutionaryInputs[1]} individuals, group size of {evolutionaryInputs[2]}, for {evolutionaryInputs[0]} generations, with mutation set to {evolutionaryInputs[5]}...")
        evolutionaryTournament(*evolutionaryInputs)
    else:
        print("Invalid selection.")  # Handle invalid tournament type selection


main()  # MOST IMPORTANT LINE OF THE CODE :D
