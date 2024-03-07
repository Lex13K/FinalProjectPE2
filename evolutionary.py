from roundRobin import round_robin_tournament
from strategies import *
import random
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

# List of strategy functions from the strategies module
strategyFunctions = [
    tit_for_tat, suspicious_tit_for_tat, tit_for_two_tats, always_defect,
    pavlov, tester, joss, grudger, soft_majority, hard_majority, prober,
    random_strategy
]


def createInitialPopulation(strategies, totalPopulation):
    """Initialize the population with an equal distribution of each strategy."""
    population = []
    perStrategy = totalPopulation // len(strategies)

    for strategy in strategies:
        population.extend([strategy] * perStrategy)

    while len(population) < totalPopulation:
        population.append(random.choice(strategyFunctions))

    return population


def conductGroupTournaments(population, groupSize, rounds, eliminationRate):
    """Conduct group tournaments, update scores, and adjust the population."""
    random.shuffle(population)
    groupScores = {strategy.__name__: 0 for strategy in strategyFunctions}

    for i in range(0, len(population), groupSize):
        group = population[i:i + groupSize]
        scores = round_robin_tournament(group, rounds)

        for name, score in scores.items():
            groupScores[name] += score

    numToEliminate = int(len(population) * eliminationRate)
    adjustments = {}
    eliminatedCount = 0

    for name, score in sorted(groupScores.items(), key=lambda x: x[1]):
        toEliminate = min(score, numToEliminate - eliminatedCount)
        adjustments[name] = score - toEliminate
        eliminatedCount += toEliminate

    newPopulation = []

    for strategy in strategyFunctions:
        strategyName = strategy.__name__
        if strategyName in adjustments:
            newPopulation.extend([strategy] * adjustments[strategyName])

    discrepancy = len(population) - len(newPopulation)

    if discrepancy > 0:
        additionalMembers = random.choices(strategyFunctions, k=discrepancy)
        newPopulation.extend(additionalMembers)
    elif discrepancy < 0:
        random.shuffle(newPopulation)
        newPopulation = newPopulation[:len(population)]

    strategyCounts = {strategy.__name__: 0 for strategy in strategyFunctions}

    for strategy in newPopulation:
        strategyCounts[strategy.__name__] += 1

    topPerformer = max(strategyCounts, key=strategyCounts.get)
    topPerformerShare = strategyCounts[topPerformer] / len(newPopulation) * 100

    print(f"Top Performer: {topPerformer}, Share of Population: {topPerformerShare:.2f}%")

    return newPopulation


def introduceMutation(population, mutationChance):
    """Introduce random mutations in the population based on mutation chance."""
    for i in range(len(population)):
        if random.random() < mutationChance:
            population[i] = random.choice(strategyFunctions)

    return population


def evolutionaryTournament(generations, totalPopulation, groupSize, rounds, eliminationRate, mutationChance):
    """Run the evolutionary tournament, stopping if a strategy dominates."""
    population = createInitialPopulation(strategyFunctions, totalPopulation)

    for generation in range(generations):
        print(f"\nGeneration {generation + 1}:")
        population = conductGroupTournaments(population, groupSize, rounds, eliminationRate)

        strategyCounts = {strategy.__name__: population.count(strategy) for strategy in strategyFunctions}
        for strategy, count in strategyCounts.items():
            if count / totalPopulation >= 0.99:
                print(
                    f"Strategy {strategy} has exceeded 99% of the population. Stopping early at generation {generation + 1}.")
                break

        if 'break' in locals():
            break

        population = introduceMutation(population, mutationChance)

    finalDistribution = {strategy.__name__: population.count(strategy) for strategy in strategyFunctions}
    sortedDistribution = dict(sorted(finalDistribution.items(), key=lambda item: item[1], reverse=True))

    print("\nFinal Strategy Distribution:")
    for strategy, count in sortedDistribution.items():
        print(f"Strategy '{strategy}': {count} individuals")

    filteredDistribution = {strategy: count for strategy, count in finalDistribution.items() if count > 0}
    totalCount = sum(filteredDistribution.values())
    threshold = totalCount * 0.01

    mainStrategies = {k: v for k, v in filteredDistribution.items() if v > threshold}
    othersCount = sum(v for k, v in filteredDistribution.items() if v <= threshold)
    if othersCount > 0:
        mainStrategies['Others'] = othersCount

    sortedStrategies = dict(sorted(mainStrategies.items(), key=lambda item: item[1], reverse=True))

    labels = sortedStrategies.keys()
    sizes = sortedStrategies.values()
    num_strategies = len(strategyFunctions)
    colormap = get_cmap('tab20')
    colors = [colormap(i / num_strategies) for i in range(num_strategies)]

    plt.figure(figsize=(10, 8))
    patches, texts, autotexts = plt.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%',
                                        startangle=90, counterclock=False)
    plt.axis('equal')
    plt.title('Final Strategy Distribution')
    for autotext in autotexts:
        autotext.set_size('x-large')

    plt.show()
