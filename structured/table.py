import random
from copy import deepcopy
from pprint import pprint

from matplotlib import pyplot as plt

from chromosome import Chromosome
from load import *


def is_end_time_within_limit(start_time: int, duration: int) -> bool:
    return start_time + duration <= DAY_END


def faculty_clash(class_: Class, instructor: Instructor, classroom_schedule: list) -> bool:
    return any(_class_ == class_ or _class_.instructor == instructor for _class_ in classroom_schedule)


class Schedule:
    """class for scheduling time slots"""

    TIME_GAP = 15  # minutes

    def __init__(self, filename: str, population_size: int, number_of_offspring: int,
                 mutation_rate: int | float) -> None:
        self.data = Data(filename)
        self.data.extraction()
        self.population_size = population_size
        self.number_of_offspring = number_of_offspring
        self.mutation_rate = mutation_rate
        self.population = []
        self.NUM_ROOMS_WEEKLY = 150
        self.chromosome = Chromosome(self.data.classrooms, self.data.instructors)
        self.available_days = [Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]

    def initializePopulation(self) -> None:
        total_classrooms = len(self.data.classrooms)
        total_classes = len(self.data.classes)
        for i in range(self.population_size):
            chromosome = Chromosome(self.data.classrooms, self.data.instructors)
            class_index = 0
            while class_index < total_classes:
                day = self.available_days[random.randrange(0, len(self.available_days))]
                classroom = self.data.classrooms[random.randrange(0, total_classrooms)]
                class_ = self.data.classes[class_index]
                instructor = class_.instructor

                # faculty clash
                while faculty_clash(class_, instructor, chromosome.schedule[day][classroom]):
                    classroom = self.data.classrooms[random.randrange(0, total_classrooms)]

                # class_.start_time = random.randrange(DAY_START, DAY_END - class_.duration, self.TIME_GAP)

                if len(chromosome.schedule[day][classroom]) == 0:
                    class_.start_time = DAY_START
                else:
                    last_class = chromosome.schedule[day][classroom][-1]
                    possible_start_time = last_class.start_time + last_class.duration + self.TIME_GAP
                    if not is_end_time_within_limit(possible_start_time, class_.duration):
                        continue
                    class_.start_time = possible_start_time

                chromosome.schedule[day][classroom].append(deepcopy(class_))
                class_index += 1

            chromosome.fitness = self.fitness(chromosome)
            self.population.append(chromosome)

    def mutation(self, chromosome: Chromosome, iteration: int = 10) -> Chromosome:
        mutated_chromosome = deepcopy(chromosome)
        if iteration == 0:
            mutated_chromosome.fitness = self.fitness(mutated_chromosome)
            return mutated_chromosome

        day1 = random.choice(self.available_days)
        day2 = random.choice(self.available_days)
        while day1 == day2:
            day2 = random.choice(self.available_days)

        room1 = random.choice(self.data.classrooms)
        class1 = mutated_chromosome.schedule[day1][room1]

        if len(class1) == 0:
            return self.mutation(chromosome, iteration - 1)

        class_index = random.randrange(0, len(class1))
        class_ = class1[class_index]

        duration = class_.duration
        number = class_.id

        for room2 in mutated_chromosome.schedule[day2].keys():
            class2 = mutated_chromosome.schedule[day2][room2]
            if any(number == c.id for c in class2):
                return self.mutation(chromosome, iteration - 1)

        room2 = random.choice(list(mutated_chromosome.schedule[day2].keys()))
        class2 = mutated_chromosome.schedule[day2][room2]

        if any(number == c.id for c in class2):
            return self.mutation(chromosome, iteration - 1)

        if len(class2) == 0:
            class_.start_time = DAY_START
        else:
            last_class = class2[-1]
            possible_start_time = last_class.start_time + last_class.duration + self.TIME_GAP
            if not is_end_time_within_limit(possible_start_time, duration):
                return self.mutation(chromosome, iteration - 1)
            class_.start_time = possible_start_time

        mutated_chromosome.schedule[day2][room2].append(class_)
        mutated_chromosome.schedule[day1][room1].remove(class_)
        return mutated_chromosome

    @staticmethod
    def classes_in_same_room(classroom: list[Class]) -> int:
        same_classes = 0
        N = len(classroom)
        for i in range(N):
            for j in range(i + 1, N):
                if classroom[i].name == classroom[j].name and classroom[i].instructor == classroom[j].instructor:
                    same_classes += 1
        return same_classes

    @staticmethod
    def classes_in_same_time(classroom: list[Class]) -> int:
        same_classes = 0
        N = len(classroom)
        for i in range(N):
            for j in range(i + 1, N):
                if classroom[i].start_time == classroom[j].start_time:
                    same_classes += 1
        return same_classes

    def time_limit_violations(self, chromosome) -> int:
        violations = 0
        for day in chromosome.schedule.keys():
            for classroom in chromosome.schedule[day].keys():
                if len(chromosome.schedule[day][classroom]) == 0:
                    continue
                last_class = chromosome.schedule[day][classroom][-1]
                if not is_end_time_within_limit(last_class.start_time, last_class.duration):
                    violations += 1
        return self.NUM_ROOMS_WEEKLY - violations

    @staticmethod
    def is_free_slot_available(chromosome: Chromosome) -> bool:
        for day in chromosome.schedule.keys():
            for classroom in chromosome.schedule[day].keys():
                for i in range(len(chromosome.schedule[day][classroom]) - 1):
                    class_ = chromosome.schedule[day][classroom][i]
                    next_class = chromosome.schedule[day][classroom][i + 1]
                    if class_.start_time + class_.duration + Schedule.TIME_GAP != next_class.start_time:
                        return True
        return False

    def fitness(self, chromosome: Chromosome) -> float:
        same_classes = 0
        same_time = 0
        violations = self.time_limit_violations(chromosome)
        free_slot_available = self.is_free_slot_available(chromosome) * 100
        for day in chromosome.schedule.keys():
            for classroom in chromosome.schedule[day].keys():
                same_classes += self.classes_in_same_room(chromosome.schedule[day][classroom])
                same_time += self.classes_in_same_time(chromosome.schedule[day][classroom])
        return same_classes + same_time + violations + free_slot_available

    def crossover(self, p1: Chromosome, p2: Chromosome, num_of_mutation: int) -> tuple[Chromosome, Chromosome]:
        p1 = deepcopy(p1)
        p2 = deepcopy(p2)

        for _ in range(num_of_mutation):
            p1 = self.mutation(p1)
            p2 = self.mutation(p2)

        p1.fitness = self.fitness(p1)
        p2.fitness = self.fitness(p2)

        return p1, p2

    def random_selection(self, parent_selection=True) -> list[Chromosome]:
        if parent_selection:
            p1_index = random.randint(0, self.population_size - 1)
            p2_index = random.randint(0, self.population_size - 1)
            while p1_index == p2_index:
                p2_index = random.randint(0, self.population_size - 1)
            p1, p2 = self.population[p1_index], self.population[p2_index]
            return [p1, p2]
        # random_population = random.sample(self.population, self.number_of_offspring)
        random_population = random.sample(self.population, self.population_size)
        return random_population

    def fitness_proportional_selection(self, parent_selection=True) -> list[Chromosome]:
        total_fitness = 0
        for chromosome in self.population:
            total_fitness += chromosome.fitness

        normalized_fitness = []
        for chromosome in self.population:
            normalized_fitness.append(chromosome.fitness / total_fitness)

        roulette_wheel = [normalized_fitness[0]]
        for i in range(1, len(normalized_fitness)):
            roulette_wheel.append(roulette_wheel[i - 1] + normalized_fitness[i])

        if parent_selection:
            random_number = random.uniform(0, 1)
            p1_index = None
            for i in range(len(roulette_wheel)):
                if random_number < roulette_wheel[i]:
                    p1_index = i
                    break

            p2_index = p1_index

            while p2_index == p1_index:
                for i in range(len(roulette_wheel)):
                    if random_number < roulette_wheel[i]:
                        p2_index = i
                        break

            return [self.population[p1_index], self.population[p2_index]]

        selected_population = []
        # for _ in range(self.number_of_offspring):
        for _ in range(self.population_size):
            random_number = random.uniform(0, 1)
            for i in range(len(roulette_wheel)):
                if random_number < roulette_wheel[i]:
                    selected_population.append(self.population[i])
                    break

        return selected_population

    def rank_based_selection(self, parent_selection=True) -> list[Chromosome]:
        self.population = sorted(self.population, key=lambda x: x.fitness)
        total_rank = self.population_size * (self.population_size + 1) / 2
        normalized_rank = []
        for i in range(self.population_size):
            normalized_rank.append((i + 1) / total_rank)

        roulette_wheel = [normalized_rank[0]]
        for i in range(1, len(normalized_rank)):
            roulette_wheel.append(roulette_wheel[i - 1] + normalized_rank[i])

        if parent_selection:
            random_number = random.uniform(0, 1)
            p1_index = None
            for i in range(len(roulette_wheel)):
                if random_number < roulette_wheel[i]:
                    p1_index = i
                    break

            p2_index = p1_index

            while p2_index == p1_index:
                random_number = random.uniform(0, 1)
                for i in range(len(roulette_wheel)):
                    if random_number < roulette_wheel[i]:
                        p2_index = i
                        break

            return [self.population[p1_index], self.population[p2_index]]

        selected_population = []
        # for _ in range(self.number_of_offspring):
        for _ in range(self.population_size):
            random_number = random.uniform(0, 1)
            for i in range(len(roulette_wheel)):
                if random_number < roulette_wheel[i]:
                    selected_population.append(self.population[i])
                    break
        return selected_population

    def truncation_selection(self, parent_selection=True) -> list[Chromosome]:
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        if parent_selection:
            return [self.population[0], self.population[1]]
        return self.population
        # return self.population[:self.number_of_offspring]

    def binary_selection(self, parent_selection=True) -> list[Chromosome]:
        if parent_selection:
            c1_index = random.randint(0, self.population_size - 1)
            c2_index = random.randint(0, self.population_size - 1)
            while c1_index == c2_index:
                c2_index = random.randint(0, self.population_size - 1)

            c1 = self.population[c1_index]
            c2 = self.population[c2_index]

            p1_index = c2_index if c1.fitness < c2.fitness else c1_index
            p2_index = p1_index

            while p2_index == p1_index:
                c1_index = random.randint(0, self.population_size - 1)
                c2_index = random.randint(0, self.population_size - 1)
                while c1_index == c2_index:
                    c2_index = random.randint(0, self.population_size - 1)

                c1 = self.population[c1_index]
                c2 = self.population[c2_index]

                p2_index = c2_index if c1.fitness < c2.fitness else c1_index

            return [self.population[p1_index], self.population[p2_index]]

        selected_population = []
        for _ in range(self.number_of_offspring):
            c1_index = random.randint(0, self.population_size - 1)
            c2_index = random.randint(0, self.population_size - 1)
            while c1_index == c2_index:
                c2_index = random.randint(0, self.population_size - 1)

            c1 = self.population[c1_index]
            c2 = self.population[c2_index]

            selected_population.append(c2 if c1.fitness < c2.fitness else c1)

        return selected_population


population_size = 20
mutation_rate = 0.2
number_of_offspring = 10
generations = 100
schedule = Schedule("Spring 2023 Schedule.csv", population_size, number_of_offspring, mutation_rate)
schedule.initializePopulation()

num_of_mutations = 1

fitness = []

for generation in range(generations):
    for i in range(number_of_offspring // 2):
        parents = schedule.truncation_selection(True)
        # parents = schedule.binary_selection(True)
        children = schedule.crossover(parents[0], parents[1], num_of_mutations)
        schedule.population.extend(children)

    schedule.population = schedule.random_selection(False)
    # schedule.population = schedule.truncation_selection(False)

    optimal_chromosome = None
    optimal_fitness = -float("inf")
    for chromosome in schedule.population:
        if chromosome.fitness > optimal_fitness:
            optimal_chromosome = chromosome
            optimal_fitness = chromosome.fitness
    fitness.append(optimal_chromosome.fitness)
    print(f"{generation + 1} : {optimal_chromosome.fitness}")

optimal_chromosome = None
optimal_fitness = -float("inf")
for chromosome in schedule.population:
    if chromosome.fitness > optimal_fitness:
        optimal_chromosome = chromosome
        optimal_fitness = chromosome.fitness
fitness.append(optimal_chromosome.fitness)
pprint(optimal_chromosome.schedule)

plt.plot(fitness)
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Structured Fitness Truncation Random Selection")
plt.savefig("structured-fitness-truncation-random-selection.png")
