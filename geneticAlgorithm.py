import random
from timeTable import TimeTable


def evolutionaryAlgorithm(filename, populationSize, mutationRate, offspringsNumber, generations):
    numMutations = 5
    timetable = TimeTable(filename, populationSize, mutationRate, offspringsNumber)
  
    timetable.initializePopulation()

    # for i in range(timetable.populationSize):
    #     chromosome = timetable.population[i]
    #     fitness = timetable.fitnessEvaluation(chromosome)
    #     timetable.population[i] = [fitness, chromosome]

    # parents = timetable.truncation(0)

    for generation in range(generations):
        print('-------------------- Generation Number = ' + str(generation+1) + ' --------------------')
        totalOffsprings = []
        for i in range(offspringsNumber // 2):
            parents = timetable.truncation(0)
            # parents = timetable.randomSelection(0)
            # parents = timetable.fpsSelection(0)
            # parents = timetable.rbsSelection(0)
            # parents = timetable.binarySelection(0)

            p1 = parents[0]
            p2 = parents[1]

            offspringOne, offspringTwo = timetable.crossover(p1, p2, numMutations)
            timetable.population.append(offspringOne)
            timetable.population.append(offspringTwo)

        # timetable.truncation(1)
        timetable.randomSelection(1)
        # timetable.fpsSelection(1)
        # timetable.rbsSelection(1)
        # timetable.binarySelection(1)

    timetable.population = sorted(timetable.population, key=lambda x: x[0])
    timetable.population.reverse()
    print(timetable.population[0][0])
    


    # print(offspringOne)
    # print("---------------------------------------------------")
    # print(offspringTwo)


filename = "Spring 2023 Schedule.csv"
populationSize = 50
mutationRate = 0.2
offspringsNumber = 10
generations = 100

evolutionaryAlgorithm(
    filename, populationSize, mutationRate, offspringsNumber, generations
)
