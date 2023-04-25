import random
from timeTable import TimeTable


def evolutionaryAlgorithm(
    filename, populationSize, mutationRate, offspringsNumber, generations
):
    timetable = TimeTable(filename, populationSize, mutationRate, offspringsNumber)
    timetable.initializePopulation()

    for i in range(timetable.populationSize):
        chromosome = timetable.population[i]
        fitness = timetable.fitnessEvaluation(chromosome)
        timetable.population[i] = [fitness, chromosome]

    # parents = timetable.truncation(0)

    for generation in range(generations):
        totalOffsprings = []
        for i in range(offspringsNumber // 2):
            parents = timetable.truncation(0)
            # parents = timetable.randomSelection(0)
            # parents = timetable.fpsSelection(0)
            # parents = timetable.rbsSelection(0)
            # parents = timetable.binarySelection(0)

            p1 = parents[0]
            p2 = parents[1]

    print(p1[0])


filename = "Spring 2023 Schedule.csv"
populationSize = 20
mutationRate = 0.2
offspringsNumber = 10
generations = 100

evolutionaryAlgorithm(
    filename, populationSize, mutationRate, offspringsNumber, generations
)
