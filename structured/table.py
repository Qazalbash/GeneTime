import csv
import random
from copy import deepcopy

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

                if len(chromosome.schedule[day][classroom]) == 0:
                    class_.start_time = DAY_START
                else:
                    last_class = chromosome.schedule[day][classroom][-1]
                    possible_start_time = last_class.start_time + last_class.duration + self.TIME_GAP
                    if not is_end_time_within_limit(possible_start_time, class_.duration):
                        continue
                    class_.start_time = possible_start_time

                chromosome.instructors_schedule[instructor.id].append(
                    (class_.id, day, class_.start_time, class_.duration))
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
        for index in range(len(class1) - 1):
            if class1[index].start_time + class1[index].duration + Schedule.TIME_GAP > class1[index + 1].start_time:
                class_index = index + 1
                break
        class_ = class1[class_index]
        start_time = class_.start_time
        duration = class_.duration
        class_id = class_.id

        for room2 in self.data.classrooms:
            class2 = mutated_chromosome.schedule[day2][room2]
            if any(class_id == c.id for c in class2):
                return self.mutation(chromosome, iteration - 1)

        room2 = random.choice(self.data.classrooms)
        class2 = mutated_chromosome.schedule[day2][room2]

        if any(class_id == c.id for c in class2):
            return self.mutation(chromosome, iteration - 1)

        if len(class2) == 0:
            class_.start_time = DAY_START
        else:
            possible_start_time = DAY_START
            for i in range(len(class2) - 1):
                if class2[i].start_time + class2[i].duration + 2 * self.TIME_GAP + duration <= class2[i + 1].start_time:
                    if not is_end_time_within_limit(class2[i].start_time + class2[i].duration + self.TIME_GAP,
                                                    duration):
                        continue
                    possible_start_time = class2[i].start_time + class2[i].duration + self.TIME_GAP
                    break
            class_.start_time = possible_start_time

        if self.faculty_clash(mutated_chromosome.instructors_schedule[class_.instructor.id], day2, class_.start_time,
                              duration):
            return self.mutation(chromosome, iteration - 1)

        mutated_chromosome.instructors_schedule[class_.instructor.id].remove((class_id, day1, start_time, duration))
        mutated_chromosome.instructors_schedule[class_.instructor.id].append(
            (class_id, day2, class_.start_time, duration))
        mutated_chromosome.schedule[day2][room2].append(class_)
        mutated_chromosome.schedule[day1][room1].remove(class_)
        return mutated_chromosome

    @staticmethod
    @njit(nopython=True)
    def faculty_clash(faculty_schedule: list[tuple], day: int, start_time: int, duration: int) -> bool:
        N = len(faculty_schedule)
        for i in range(N):
            id_i, day_i, start_i, duration_i = faculty_schedule[i]
            if day_i == day and not (start_i + duration_i < start_time or start_time + duration < start_i):
                return True
        return False

    @staticmethod
    def faculty_clashes(instructors_schedule: dict) -> int:
        clashes = 0
        for instructor_id in instructors_schedule.keys():
            classes = instructors_schedule[instructor_id]
            N = len(classes)
            for i in range(N):
                id_i, day_i, start_i, duration_i = classes[i]
                for j in range(i + 1, N):
                    id_j, day_j, start_j, duration_j = classes[j]
                    if day_i == day_j and not (start_i + duration_i < start_j or start_j + duration_j < start_i):
                        clashes += 1
        return clashes

    @staticmethod
    def classes_in_same_room_time(classroom: list[Class]) -> tuple[int, int]:
        same_room_classes = 0
        same_time_classes = 0
        N = len(classroom)
        for i in range(N):
            for j in range(i + 1, N):
                if classroom[i].name == classroom[j].name and classroom[i].instructor.id == classroom[j].instructor.id:
                    same_room_classes += 1
                if classroom[i].start_time == classroom[j].start_time:
                    same_time_classes += 1
        return same_room_classes, same_time_classes

    def violations_check(self, schedule: dict) -> tuple[int, int, int, int]:
        same_room_classes = 0
        same_time_classes = 0
        free_slot = 0
        class_overlap = 0
        for day in schedule.keys():
            for classroom in schedule[day].keys():
                for i in range(len(schedule[day][classroom]) - 1):
                    class_ = schedule[day][classroom][i]
                    next_class = schedule[day][classroom][i + 1]
                    if class_.start_time + class_.duration + Schedule.TIME_GAP != next_class.start_time:
                        free_slot += 1
                    if class_.start_time + class_.duration + Schedule.TIME_GAP > next_class.start_time:
                        class_overlap += 1
                room_classes, time_classes = self.classes_in_same_room_time(schedule[day][classroom])
                same_room_classes += room_classes
                same_time_classes += time_classes
        return same_room_classes, same_time_classes, free_slot, class_overlap

    def fitness(self, chromosome: Chromosome) -> float:
        room_clash, time_clash, free_slot, overlapping_classes = self.violations_check(chromosome.schedule)
        faculty_clash = self.faculty_clashes(chromosome.instructors_schedule)
        return self.data.TOTAL_CLASSES + free_slot - room_clash - time_clash - faculty_clash - overlapping_classes

    def crossover(self, p1: Chromosome, p2: Chromosome, num_of_mutation: int) -> tuple[Chromosome, Chromosome]:
        p1 = deepcopy(p1)
        p2 = deepcopy(p2)

        for _ in range(num_of_mutation):
            p1 = self.mutation(p1)
            p2 = self.mutation(p2)

        p1.sort()
        p2.sort()

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

    def to_csv(self, file_name: str, chromosome: Chromosome) -> None:
        days = ["M", "T", "W", "R", "F"]
        schedule = chromosome.schedule
        with open(file_name, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                ["Day", "Start Time", "End Time", "Course title", "Room", "Instructor", "Actual Class Duration"])
            for day in schedule.keys():
                for classroom in schedule[day]:
                    for course in schedule[day][classroom]:
                        writer.writerow([days[day], getTimeString(course.start_time),
                                         getTimeString(course.start_time + course.duration), course.name,
                                         classroom.name, course.instructor.name,
                                         course.duration])


population_size = 20
mutation_rate = 0.2
number_of_offspring = 5
generations = 100
num_of_mutations = 3
schedule = Schedule("../Spring 2023 Schedule.csv", population_size, number_of_offspring, mutation_rate)
schedule.initializePopulation()


def faculty_clashes(instructors_schedule: dict) -> int:
    clashes = 0
    for instructor_id in instructors_schedule.keys():
        classes = instructors_schedule[instructor_id]
        N = len(classes)
        for i in range(N):
            id_i, day_i, start_i, duration_i = classes[i]
            for j in range(i + 1, N):
                id_j, day_j, start_j, duration_j = classes[j]
                if day_i == day_j and not (start_i + duration_i < start_j or start_j + duration_j < start_i):
                    clashes += 1
    return clashes


fitness = []
clashes = []
classes_in_same_room = []
classes_in_same_time = []
free_slots = []
overlapping_classes = []
optimal_chromosome = None

for generation in range(generations):
    for i in range(number_of_offspring):
        parents = schedule.truncation_selection(True)
        # parents = schedule.binary_selection(True)
        children = schedule.crossover(parents[0], parents[1], num_of_mutations)
        schedule.population.extend(children)

    schedule.population = schedule.random_selection(False)
    # schedule.population = schedule.truncation_selection(False)

    optimal_fitness = -float("inf")
    for chromosome in schedule.population:
        if chromosome.fitness > optimal_fitness:
            optimal_chromosome = chromosome
            optimal_fitness = chromosome.fitness
    fitness.append(optimal_chromosome.fitness)
    clash = faculty_clashes(optimal_chromosome.instructors_schedule)
    room_clash, time_clash, free_slot, overlapping_class = schedule.violations_check(optimal_chromosome.schedule)
    clashes.append(clash)
    classes_in_same_room.append(room_clash)
    classes_in_same_time.append(time_clash)
    free_slots.append(free_slot)
    overlapping_classes.append(overlapping_class)
    print(
        f"{generation + 1} : {optimal_chromosome.fitness} {clash} {room_clash} {time_clash} {free_slot} {overlapping_class}")

schedule.to_csv("schedule.csv", optimal_chromosome)

fig, axs = plt.subplots()

axs.plot(range(1, generations + 1), fitness, label="Fitness")
axs2 = axs.twinx()
axs2.plot(range(1, generations + 1), clashes, label="Clashes", color="orange")
axs2.plot(range(1, generations + 1), classes_in_same_room, label="same room", color="red")
axs2.plot(range(1, generations + 1), classes_in_same_time, label="same time", color="purple")
axs2.plot(range(1, generations + 1), free_slots, label="Free slots", color="green")
axs2.plot(range(1, generations + 1), overlapping_classes, label="overlapping classes", color="brown")
axs.set_xlabel("Generation")
axs.set_ylabel("Fitness")
axs2.set_ylabel("Clashes")
axs.legend(loc="best")
axs2.legend(loc="best")
plt.savefig("test7.png")
