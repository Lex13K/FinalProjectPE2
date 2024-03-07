from roundRobin import round_robin_tournament
from strategies import *
import random
import matplotlib.pyplot as plt

# List of strategy functions from the strategies module
strategy_functions = [tit_for_tat, suspicious_tit_for_tat, tit_for_two_tats, always_defect, pavlov, tester, joss,
                      grudger, soft_majority, hard_majority, prober, random_strategy]

def create_initial_population(strategy_functions, total_population):
    """Initialize the population with an equal distribution of each strategy."""
    population = []  # Start with an empty population
    per_strategy = total_population // len(strategy_functions)  # Calculate how many individuals per strategy
    for strategy in strategy_functions:
        population.extend([strategy] * per_strategy)  # Add an equal number of each strategy to the population
    while len(population) < total_population:
        population.append(random.choice(strategy_functions))  # Fill in any remainder with random strategies
    return population  # Return the initialized population

def conduct_group_tournaments(population, group_size, rounds, elimination_rate):
    """Conduct group tournaments, update scores, and adjust the population."""
    random.shuffle(population)  # Shuffle the population for random grouping
    group_scores = {strategy.__name__: 0 for strategy in strategy_functions}  # Initialize a score dictionary for strategies

    # Conduct tournaments in groups and collect scores
    for i in range(0, len(population), group_size):
        group = population[i:i + group_size]  # Create a group for the tournament
        scores = round_robin_tournament(group, rounds)  # Conduct the tournament and get scores
        for name, score in scores.items():
            group_scores[name] += score  # Update the total score for each strategy

    # Calculate and apply elimination based on performance
    num_to_eliminate = int(len(population) * elimination_rate)  # Number of individuals to eliminate
    adjustments = {}  # Dictionary to track population adjustments
    eliminated_count = 0  # Counter for eliminated individuals
    for name, score in sorted(group_scores.items(), key=lambda x: x[1]):
        to_eliminate = min(score, num_to_eliminate - eliminated_count)  # Calculate number to eliminate from this strategy
        adjustments[name] = score - to_eliminate  # Adjust the population size for this strategy
        eliminated_count += to_eliminate  # Update the total number of eliminated individuals

    # Reconstruct the new population after elimination
    new_population = []
    for strategy in strategy_functions:
        strategy_name = strategy.__name__
        if strategy_name in adjustments:
            new_population.extend([strategy] * adjustments[strategy_name])  # Add the adjusted number of individuals per strategy

    # Fix any discrepancies from rounding errors during adjustments
    discrepancy = len(population) - len(new_population)
    if discrepancy > 0:  # If there are fewer individuals than needed
        additional_members = random.choices(strategy_functions, k=discrepancy)
        new_population.extend(additional_members)  # Add random strategies to meet the population size
    elif discrepancy < 0:  # If there are too many individuals
        random.shuffle(new_population)
        new_population = new_population[:len(population)]  # Trim the excess

    # Identify and print the top-performing strategy for this generation
    strategy_counts = {strategy.__name__: 0 for strategy in strategy_functions}
    for strategy in new_population:
        strategy_counts[strategy.__name__] += 1  # Count the number of individuals per strategy
    top_performer = max(strategy_counts, key=strategy_counts.get)  # Determine the top performer
    top_performer_share = strategy_counts[top_performer] / len(new_population) * 100  # Calculate the share percentage
    print(f"Top Performer: {top_performer}, Share of Population: {top_performer_share:.2f}%")  # Print top performer info

    return new_population  # Return the adjusted population

def introduce_mutation(population, mutation_chance):
    """Introduce random mutations in the population based on mutation chance."""
    for i in range(len(population)):
        if random.random() < mutation_chance:  # Check if mutation occurs based on chance
            population[i] = random.choice(strategy_functions)  # Replace the individual's strategy with a random one
    return population  # Return the mutated population

def evolutionary_tournament(generations, total_population, group_size, rounds, elimination_rate, mutation_chance):
    """Run the evolutionary tournament, stopping if a strategy dominates."""
    population = create_initial_population(strategy_functions, total_population)  # Initialize the population

    for generation in range(generations):
        print(f"\nGeneration {generation + 1}:")
        population = conduct_group_tournaments(population, group_size, rounds, elimination_rate)  # Conduct the tournaments

        # Check for a dominant strategy exceeding 99% of the population
        strategy_counts = {strategy.__name__: population.count(strategy) for strategy in strategy_functions}
        for strategy, count in strategy_counts.items():
            if count / total_population >= 0.99:
                print(f"Strategy {strategy} has exceeded 99% of the population. Stopping early at generation {generation + 1}.")
                break  # End the tournament early

        if 'break' in locals():
            break  # If a break was triggered, exit the loop

        population = introduce_mutation(population, mutation_chance)  # Mutate the population

    # Calculate the final distribution of strategies
    final_distribution = {strategy.__name__: population.count(strategy) for strategy in strategy_functions}
    sorted_distribution = dict(sorted(final_distribution.items(), key=lambda item: item[1], reverse=True))

    print("\nFinal Strategy Distribution:")  # Display the final distribution of strategies
    for strategy, count in sorted_distribution.items():
        print(f"Strategy '{strategy}': {count} individuals")

    # Prepare data for plotting the distribution
    filtered_distribution = {strategy: count for strategy, count in final_distribution.items() if count > 0}
    total_count = sum(filtered_distribution.values())
    threshold = total_count * 0.01  # Define a threshold for grouping into "Others"

    # Group less common strategies into "Others"
    main_strategies = {k: v for k, v in filtered_distribution.items() if v > threshold}
    others_count = sum(v for k, v in filtered_distribution.items() if v <= threshold)
    if others_count > 0:
        main_strategies['Others'] = others_count

    sorted_strategies = dict(sorted(main_strategies.items(), key=lambda item: item[1], reverse=True))

    # Plotting the distribution
    labels = sorted_strategies.keys()
    sizes = sorted_strategies.values()
    colors = plt.get_cmap('tab20').colors  # Assign colors for the pie chart

    plt.figure(figsize=(10, 8))
    patches, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%',
                                        startangle=90, counterclock=False)
    plt.axis('equal')  # Ensure the pie chart is a circle
    plt.title('Final Strategy Distribution')
    for autotext in autotexts:
        autotext.set_size('x-large')  # Enhance readability of percentage labels

    plt.show()  # Display the pie chart
