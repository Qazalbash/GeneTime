import datetime

from matplotlib import pyplot as plt

from timeTable import TimeTable


def evolutionaryAlgorithm(filename, populationSize, mutationRate,
                          offspringsNumber, generations, filenameStudents,
                          numIterations):
    avgEndTimes = {}
    avgFitness = {}
    lowestAvgEndTime = datetime.datetime.strptime("18:00", "%H:%M")
    highestFitness = 0
    highestIterationFitness = 0
    optimalClassDetails = 0

    for iteration in range(1, numIterations + 1):

        numMutations = 1
        timetable = TimeTable(filename, populationSize, mutationRate,
                              offspringsNumber, filenameStudents)
        timetable.initializePopulation()

        for generation in range(1, generations + 1):
            print('-------------------- Iternation Number = ' + str(iteration) +
                  ', Generation Number = ' + str(generation) +
                  ' --------------------')
            for i in range(offspringsNumber // 2):
                parents = timetable.truncation(0)
                # parents = timetable.randomSelection(0)
                # parents = timetable.fpsSelection(0)
                # parents = timetable.rbsSelection(0)
                # parents = timetable.binarySelection(0)

                p1 = parents[0]
                p2 = parents[1]

                offspringOne, offspringTwo = timetable.crossover(
                    p1, p2, numMutations)
                # offsprings = [offspringOne, offspringTwo]

                # for j in range(2):
                #     # randomNumber = round(random.uniform(0.00, 1.00), 2)
                #     # if randomNumber < mutationRate:
                #     mutatedChromosome, C2, updated_faculty_working_hours = timetable.mutation(offsprings[j][1], offsprings[j][2], offsprings[j][3])
                #     updatedFitness = timetable.fitnessEvaluation(mutatedChromosome, C2)
                #     offsprings[j] = [updatedFitness, mutatedChromosome, C2, updated_faculty_working_hours]

                # for offspring in offsprings:
                #     timetable.population.append(offspring)

                timetable.population.append(offspringOne)
                timetable.population.append(offspringTwo)

            # timetable.truncation(1)
            timetable.randomSelection(1)
            # timetable.fpsSelection(1)
            # timetable.rbsSelection(1)
            # timetable.binarySelection(1)

            timetable.population = sorted(timetable.population,
                                          key=lambda x: x[0],
                                          reverse=True)
            optimalChromosome = timetable.population[0]
            print("Fitness:" + str(optimalChromosome[0]))
            optimalSchedule = optimalChromosome[1]
            endTimes = timetable.getEndTimes(optimalSchedule)

            total_seconds = sum(dt.timestamp() for dt in endTimes)
            average_seconds = total_seconds / len(endTimes)
            avgDatetime = datetime.datetime.fromtimestamp(average_seconds)

            if avgDatetime < lowestAvgEndTime:
                lowestAvgEndTime = avgDatetime

            if "Generation " + str(generation) in avgEndTimes:
                avgEndTimes["Generation " + str(generation)].append(avgDatetime)
            else:
                avgEndTimes["Generation " + str(generation)] = [avgDatetime]

            if optimalChromosome[0] > highestFitness:
                highestFitness = optimalChromosome[0]

            if "Generation " + str(generation) in avgFitness:
                avgFitness["Generation " + str(generation)].append(
                    optimalChromosome[0])
            else:
                avgFitness["Generation " +
                           str(generation)] = [optimalChromosome[0]]

        timetable.population = sorted(timetable.population,
                                      key=lambda x: x[0],
                                      reverse=True)
        optimalChromosome = timetable.population[0]
        print("Fitness:" + str(optimalChromosome[0]))
        if optimalChromosome[0] > highestIterationFitness:
            highestIterationFitness = optimalChromosome[0]
            optimalClassDetails = optimalChromosome[2]

    timetable.getTimeTable(optimalClassDetails)  # makes csv file
    print('Best Fitness:' + str(highestFitness))
    print('Lowest Average End Time: ' + lowestAvgEndTime.strftime("%H:%M"))
    # print(avgEndTimes)
    # print(avgFitness)

    graphMaker(avgEndTimes, avgFitness)

    # timetable.population = sorted(timetable.population, key=lambda x: x[0], reverse=True)
    # optimalChromosome = timetable.population[0]
    # print("Fitness:" + str(optimalChromosome[0]))
    # classDetails = optimalChromosome[2]
    # timetable.getTimeTable(classDetails)  # makes csv file
    # graphMaker(totalEndTimes)

    # plt.plot(range(len(fitness)), fitness)
    # plt.xlabel("Generations")
    # plt.ylabel("Fitness")
    # plt.savefig("fitness-linear.png")


def graphMaker(avgEndTime, avgFitness):
    xAxis = []
    avgAvgEndTimes = []
    avgFitnessValues = []
    generationNumber = 0

    for generation, endTimes in avgEndTime.items():
        generationNumber += 1
        xAxis.append(generationNumber)
        total_seconds = sum(dt.timestamp() for dt in endTimes)
        average_seconds = total_seconds / len(endTimes)
        avgDatetime = datetime.datetime.fromtimestamp(average_seconds)
        avgAvgEndTimes.append(avgDatetime)

    for generation, fitness in avgFitness.items():
        avg = sum(fitness) / len(fitness)
        avgFitnessValues.append(avg)

    endTimesGraph(xAxis, avgAvgEndTimes)
    fitnessGraph(xAxis, avgFitnessValues)


def endTimesGraph(xAxis, avgAvgEndTimes):
    plt.plot(xAxis, avgAvgEndTimes, label='Average Weekly End Times')
    plt.title("Average Weekly End Times Across Generations")
    plt.xlabel("Generations")
    plt.ylabel("Average Weekly End Times")
    plt.legend()
    plt.savefig("results(endTimes)/Truncation-Random.png")
    plt.show()


def fitnessGraph(xAxis, avgFitnessValues):
    plt.plot(xAxis, avgFitnessValues, label='Average Fitness')
    plt.title("Average Fitness Across Generations")
    plt.xlabel("Generations")
    plt.ylabel("Average Fitness")
    plt.legend()
    plt.savefig("results(fitness)/Truncation-Random.png")


filename = "Spring 2023 Schedule.csv"
filenameStudents = "Spring 2023 student enrollment.csv"
populationSize = 20
mutationRate = 0.2
offspringsNumber = 10
generations = 10
numIterations = 10

evolutionaryAlgorithm(filename, populationSize, mutationRate, offspringsNumber,
                      generations, filenameStudents, numIterations)
