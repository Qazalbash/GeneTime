import random
from pprint import pprint

from datacleaning import DataCleaning


def add24Hours(time1: int, time2: int) -> int:
    """Add 24 hours to a time

    Args:
        time1 (int): The time to add 24 hours to

    Returns:
        int: The time after adding 24 hours
    """
    minute1 = time1 % 100
    hour1 = time1 // 100

    minute2 = time2 % 100
    hour2 = time2 // 100

    totalMinutes = minute1 + minute2
    totalHours = hour1 + hour2 + totalMinutes // 60
    totalMinutes %= 60

    return totalHours * 100 + totalMinutes


def extend24Hours(time: int, minutes: int) -> int:
    """Add 24 hours to a time

    Args:
        time1 (int): The time to add 24 hours to

    Returns:
        int: The time after adding 24 hours
    """
    minute = time % 100
    hour = time // 100
    totalMinutes = minute + minutes
    totalHours = hour + totalMinutes // 60
    totalMinutes = totalMinutes % 60
    return totalHours * 100 + totalMinutes


class GeneticAlgorithm:
    """Class to implement the Genetic Algorithm"""

    def __init__(self) -> None:
        """Initialize the Genetic Algorithm class"""
        self.dc = DataCleaning("Spring 2023 Schedule.csv")
        self.availableDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.population = []
        self.populationSize = 20

    def generate_start_time(self) -> int:
        """Generate a random start time for a class

        Returns:
            int: The start time for a class
        """
        hours = random.randint(8, 18)  # Schedule between 8am and 6pm
        minutes = random.randint(0, 11) * 5  # Schedule in multiples of 5
        return hours * 100 + minutes

    def initializePopulation(self) -> None:
        """Initialize the population of chromosomes"""
        for i in range(self.populationSize):
            chromosome = {day: {} for day in self.availableDays}
            for classNumber, data in self.dc.class_nbr_dict.items():
                days = random.sample(self.availableDays, data["Frequency"])
                for day in days:
                    room = random.sample(self.dc.room_list, 1)[0]
                    chromosome[day][classNumber] = [
                        data["Course title"],  # course_name
                        data["Instructor"],  # instructor
                        room,  # room
                        self.generate_start_time(),  # start_time
                        data["Actual Class Duration"],  # duration
                    ]
            self.population.append(chromosome)

    @staticmethod
    def fitnessEvaluation(chromosome: dict) -> None:
        """Evaluate the fitness of a chromosome

        Args:
            chromosome (dict): The chromosome to evaluate the fitness of
        """
        roomConflicts = 0
        facultyClashes = 0

        for day in chromosome.keys():
            classes = list(chromosome[day].values())
            for i in range(len(classes)):
                course_name, instructor, room, start_time, duration = classes[i]
                end_time = extend24Hours(start_time, duration)

                for j in range(i + 1, len(classes)):
                    (
                        other_course_name,
                        other_instructor,
                        other_room,
                        other_start_time,
                        other_duration,
                    ) = classes[j]

                    other_end_time = extend24Hours(other_start_time, other_duration)

                    if start_time < other_end_time and end_time > other_start_time:
                        if other_room == room:
                            roomConflicts += 1
                        if other_instructor == instructor:
                            facultyClashes += 1

        conflicts = roomConflicts + facultyClashes

        print(f"Total number of Room conflicts: {roomConflicts}")
        print(f"Total number of Faculty conflicts: {facultyClashes}")
        print(f"Total number of conflicts: {conflicts}")


ga = GeneticAlgorithm()
ga.initializePopulation()
chromosome = ga.population[0]
# pprint(chromosome)
ga.fitnessEvaluation(chromosome)
# print(ga.population)

# ga.getAvailableTimes()
# print(ga)
