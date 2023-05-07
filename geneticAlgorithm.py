from matplotlib import pyplot as plt

from timeTable import TimeTable


def evolutionaryAlgorithm(filename, populationSize, mutationRate, offspringsNumber, generations, filenameStudents):
    numMutations = 1
    timetable = TimeTable(filename, populationSize, mutationRate, offspringsNumber, filenameStudents)

    timetable.initializePopulation()

    # for i in range(timetable.populationSize):
    #     chromosome = timetable.population[i]
    #     fitness = timetable.fitnessEvaluation(chromosome)
    #     timetable.population[i] = [fitness, chromosome]

    # parents = timetable.truncation(0)
    fitness = []
    for generation in range(generations):
        print(f'-------------------- Generation Number = {generation + 1} --------------------')
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
        # timetable.randomSelection(1)
        # timetable.fpsSelection(1)
        timetable.rbsSelection(1)
        # timetable.binarySelection(1)

        timetable.population = sorted(timetable.population, key=lambda x: x[0], reverse=True)
        optimalChromosome = timetable.population[0]
        fitness.append(optimalChromosome[0])
        print("Fitness:" + str(optimalChromosome[0]))

    timetable.population = sorted(timetable.population, key=lambda x: x[0], reverse=True)
    optimalChromosome = timetable.population[0]
    print("Fitness:" + str(optimalChromosome[0]))
    classDetails = optimalChromosome[2]
    timetable.getTimeTable(classDetails)
    plt.plot(range(len(fitness)), fitness)
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.savefig("fitness-linear.png")

    # print(offspringOne)
    # print("---------------------------------------------------")
    # print(offspringTwo)


filename = "Spring 2023 Schedule.csv"
filenameStudents = "Spring 2023 student enrollment.csv"
populationSize = 20
mutationRate = 0.2
offspringsNumber = 10
generations = 1000

evolutionaryAlgorithm(
    filename, populationSize, mutationRate, offspringsNumber, generations, filenameStudents
)
