from roundRobin import round_robin_tournament
from strategies import *
import random
import matplotlib.pyplot as plt

strategy_functions = [tit_for_tat, suspicious_tit_for_tat, tit_for_two_tats, always_defect, pavlov, tester, joss,
                      grudger, soft_majority, hard_majority, prober, random_strategy]


def create_initial_population(strategy_functions, total_population):
    """Distribute strategies equally in the initial population."""
    population = []
    per_strategy = total_population // len(strategy_functions)
    for strategy in strategy_functions:
        population.extend([strategy] * per_strategy)
    while len(population) < total_population:
        population.append(random.choice(strategy_functions))
    return population


def conduct_group_tournaments(population, group_size, rounds, elimination_rate):
    import random
    # Assume strategy_functions is a list of all strategy function objects available for the simulation
    strategy_functions = [strategy for strategy in population]  # You may need to adjust this line based on your implementation
    random.shuffle(population)
    group_scores = {strategy.__name__: 0 for strategy in strategy_functions}  # Initialize scores for each strategy

    # Conduct group tournaments and aggregate scores
    for i in range(0, len(population), group_size):
        group = population[i:i + group_size]
        scores = round_robin_tournament(group, rounds)  # Conduct tournament for each group
        for name, score in scores.items():
            group_scores[name] += score  # Aggregate scores

    # Calculate the number of individuals to eliminate
    num_to_eliminate = int(len(population) * elimination_rate)

    # Determine strategies of bottom performers and adjust population
    adjustments = {}
    eliminated_count = 0
    for name, score in sorted(group_scores.items(), key=lambda x: x[1]):
        if eliminated_count < num_to_eliminate:
            to_eliminate = min(score, num_to_eliminate - eliminated_count)
            adjustments[name] = max(0, score - to_eliminate)
            eliminated_count += to_eliminate
        else:
            adjustments[name] = score

    # Adjust population based on calculated adjustments
    new_population = []
    for strategy in strategy_functions:
        strategy_name = strategy.__name__
        if strategy_name in adjustments and adjustments[strategy_name] > 0:
            proportion = adjustments[strategy_name] / sum(adjustments.values())
            count = round(proportion * len(population))
            new_population.extend([strategy] * count)

    # Handle any discrepancies due to rounding
    discrepancy = len(population) - len(new_population)
    if discrepancy > 0:
        additional_members = random.choices(strategy_functions, k=discrepancy)
        new_population.extend(additional_members)
    elif discrepancy < 0:
        random.shuffle(new_population)
        new_population = new_population[:len(population)]

    # Calculate and print top performer information
    strategy_counts = {strategy.__name__: 0 for strategy in strategy_functions}
    for strategy in new_population:
        strategy_counts[strategy.__name__] += 1
    top_performer = max(strategy_counts, key=strategy_counts.get)
    top_performer_share = strategy_counts[top_performer] / len(new_population) * 100
    print(f"Top Performer: {top_performer}, Share of Population: {top_performer_share:.2f}%")

    return new_population



def introduce_mutation(population, mutation_chance):
    """Introduce random mutations into the population."""
    for i in range(len(population)):
        if random.random() < mutation_chance:
            population[i] = random.choice(strategy_functions)
    return population


def evolutionary_tournament(generations, total_population, group_size, rounds, elimination_rate, mutation_chance):
    """Execute the evolutionary tournament across multiple generations."""
    population = create_initial_population(strategy_functions, total_population)

    breaker = False

    for generation in range(generations):
        print(f"\nGeneration {generation + 1}:")
        population = conduct_group_tournaments(population, group_size, rounds, elimination_rate)

        # Check if any strategy exceeds the 99% threshold
        strategy_counts = {strategy.__name__: population.count(strategy) for strategy in strategy_functions}
        for strategy, count in strategy_counts.items():
            if count / total_population > 0.99:
                print(f"Strategy {strategy} has exceeded 99% of the population. Stopping early at generation {generation + 1}.")
                # Break out of the loop to end the tournament
                breaker = True
                break

        if breaker:
            break

        # Introduce mutation if no strategy has exceeded the threshold
        population = introduce_mutation(population, mutation_chance)

    # Final population distribution
    final_distribution = {strategy.__name__: population.count(strategy) for strategy in strategy_functions}

    # Sort the final distribution by count, descending
    sorted_distribution = dict(sorted(final_distribution.items(), key=lambda item: item[1], reverse=True))

    print("\nFinal Strategy Distribution:")
    for strategy, count in sorted_distribution.items():
        print(f"Strategy '{strategy}': {count} individuals")


    filtered_distribution = {strategy: count for strategy, count in final_distribution.items() if count > 0}

    # Determine a threshold for grouping into "Others"
    total_count = sum(filtered_distribution.values())
    threshold = total_count * 0.01  # For example, strategies representing less than 1% of the total

    # Split strategies into main and others
    main_strategies = {k: v for k, v in filtered_distribution.items() if v > threshold}
    others_count = sum(v for k, v in filtered_distribution.items() if v <= threshold)
    if others_count > 0:
        main_strategies['Others'] = others_count

    # Sort the strategies by count in descending order
    sorted_strategies = dict(sorted(main_strategies.items(), key=lambda item: item[1], reverse=True))

    # Data for plotting
    labels = sorted_strategies.keys()
    sizes = sorted_strategies.values()
    colors = plt.get_cmap('tab20').colors  # Get a set of colors up to the number of strategies

    # Plotting pie chart
    plt.figure(figsize=(10, 8))  # Adjusts the size of the figure
    # Startangle is set to 90 to start from the top. Setting counterclock=False will make it clockwise.
    patches, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%',
                                        startangle=90, counterclock=False)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('Final Strategy Distribution')

    # Increase the size of the percentage labels
    for autotext in autotexts:
        autotext.set_size('x-large')

    plt.show()

