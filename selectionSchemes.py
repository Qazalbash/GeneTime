import random
from typing import Any


class SelectionSchemes:
    def __init__(self) -> None:
        self.population = None
        self.populationSize = 100

    def randomSelection(self, flag: int) -> list[Any]:
        if flag == 0:
            p1Index = random.randint(0, self.populationSize - 1)
            p2Index = random.randint(0, self.populationSize - 1)
            while p1Index == p2Index:
                p2Index = random.randint(0, self.populationSize - 1)
            p1 = self.population[p1Index]
            p2 = self.population[p2Index]
            return [p1, p2]

        elif flag == 1:
            randomlist = random.sample(range(len(self.population)), self.populationSize)
            temp_population = [self.population[index] for index in randomlist]
            self.population = temp_population

    def fpsSelection(self, flag):
        sumFitness = 0
        ranges = []

        for chromosome in self.population:
            sumFitness += chromosome[0]

        normalizedFitness = [chromosome[0] / sumFitness for chromosome in self.population]

        pointer = 0

        for i in range(len(normalizedFitness)):
            limits = [pointer, pointer + normalizedFitness[i]]
            ranges.append(limits)
            pointer += normalizedFitness[i]

        p1Index = None

        if flag == 0:
            randomIndex = random.uniform(0, 1)
            for index in range(len(ranges)):
                if ranges[index][0] <= randomIndex <= ranges[index][1]:
                    p1Index = index

            p2Index = p1Index
            while p1Index == p2Index:
                randomIndex = random.uniform(0, 1)
                for index in range(len(ranges)):
                    if ranges[index][0] <= randomIndex <= ranges[index][1]:
                        p2Index = index

            return [self.population[p1Index], self.population[p2Index]]

        elif flag == 1:
            selectedIndexes = []
            while len(selectedIndexes) < self.populationSize:
                randomIndex = random.uniform(0, 1)
                for index in range(len(ranges)):
                    if ranges[index][0] <= randomIndex <= ranges[index][1] and index not in selectedIndexes:
                        selectedIndexes.append(index)

            tempPopulation = []
            for i in selectedIndexes:
                tempPopulation.append(self.population[i])

            self.population = tempPopulation  # self.population.sort()  # self.population.reverse()

    def rbsSelection(self, flag):
        ranks = list(range(len(self.population), 0, -1))

        sumRanks = 0
        for rank in range(1, len(self.population) + 1):
            sumRanks += rank

        self.population = sorted(self.population, key=lambda x: x[0], reverse=True)

        normalizedRanks = [i / sumRanks for i in ranks]

        pointer = 0
        ranges = []

        for i in range(len(normalizedRanks)):
            limits = [pointer, pointer + normalizedRanks[i]]
            ranges.append(limits)
            pointer += normalizedRanks[i]

        if flag == 0:
            p1Index = None
            randomIndex = random.uniform(0, 1)
            for index in range(len(ranges)):
                if ranges[index][0] <= randomIndex <= ranges[index][1]:
                    p1Index = index

            p2Index = p1Index
            while p1Index == p2Index:
                randomIndex = random.uniform(0, 1)
                for index in range(len(ranges)):
                    if ranges[index][0] <= randomIndex <= ranges[index][1]:
                        p2Index = index

            return [self.population[p1Index], self.population[p2Index]]

        elif flag == 1:
            selectedIndexes = []
            while len(selectedIndexes) < self.populationSize:
                randomIndex = random.uniform(0, 1)
                for index in range(len(ranges)):
                    if ranges[index][0] <= randomIndex <= ranges[index][1] and index not in selectedIndexes:
                        selectedIndexes.append(index)

            tempPopulation = [self.population[index] for index in selectedIndexes]

            self.population = tempPopulation

    def truncation(self, flag):
        self.population = sorted(self.population, key=lambda x: x[0], reverse=True)

        if flag == 0:
            return [self.population[0], self.population[1]]

        elif flag == 1:
            self.population = self.population[0: self.populationSize]

    def binarySelection(self, flag):
        if flag == 0:
            contestant1 = random.randint(0, self.populationSize - 1)
            contestant2 = random.choice(list(set(range(self.populationSize)) - {contestant1}))

            if self.population[contestant1][0] >= self.population[contestant2][0]:
                p1Index = contestant1
            else:
                p1Index = contestant2

            contestant1 = random.choice(list(set(range(self.populationSize)) - {p1Index}))
            contestant2 = random.choice(list(set(range(self.populationSize)) - {p1Index, contestant1}))

            if self.population[contestant1][0] >= self.population[contestant2][0]:
                p2Index = contestant1
            else:
                p2Index = contestant2

            return [self.population[p1Index], self.population[p2Index]]

        elif flag == 1:
            selectedIndexes = []

            for i in range(self.populationSize):
                contestant1 = random.choice(list(set(range(len(self.population))) - set(selectedIndexes)))
                contestant2 = random.choice(
                    list(set(range(len(self.population))) - set(selectedIndexes + [contestant1])))

                if self.population[contestant1][0] >= self.population[contestant2][0]:
                    selectedIndexes.append(contestant1)
                else:
                    selectedIndexes.append(contestant2)

            tempPopulation = [self.population[index] for index in selectedIndexes]

            self.population = tempPopulation  # self.population.sort()  # self.population.reverse()
