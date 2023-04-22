from datacleaning import DataCleaning
import random
from datetime import datetime, timedelta
import pandas as pd


class GeneticAlgorithm:

    def __init__(self) -> None:
        self.dc = DataCleaning()
        self.availableDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.population = []
        # self.chromosome = {'Monday':{}, 'Tuesday':{}, 'Wednesday':{}, 'Thursday':{}, 'Friday':{}}
        self.populationSize = 20
        # print(self.dc.class_nbr_dict)

    def generate_start_time(self):

        hours = random.randint(8, 18)  # Schedule between 8am and 6pm
        minutes = random.randint(0, 11) * 5  # Schedule in multiples of 5
        return f'{hours:02d}:{minutes:02d}'


    def initializePopulation(self):
        for i in range(self.populationSize):
            chromosome = {'Monday':{}, 'Tuesday':{}, 'Wednesday':{}, 'Thursday':{}, 'Friday':{}}
            for classNumber, data in self.dc.class_nbr_dict.items():
                days = random.sample(self.availableDays, data['Frequency'])
                for day in days:
                    room = random.sample(self.dc.room_list,1)[0]
                    startTime = self.generate_start_time()
                    endTime = (pd.to_datetime(startTime) + pd.to_timedelta(data['Actual Class Duration'], unit='m')).strftime('%H:%M')
                    chromosome[day][classNumber] = [data['Course title'], data['Instructor'], room, startTime, endTime]
            self.population.append(chromosome)


    def fitnessEvaluation(chromosome):
        roomConflicts = 0
        facultyClashes = 0
        for day in chromosome.keys():
            classes = list(chromosome[day].values())
            # print(classes)
            for i in range(len(classes)):
                class_data = classes[i]
                room = class_data[2]
                instructor = class_data[1]
                start_time = datetime.strptime(class_data[3], '%H:%M')
                end_time = datetime.strptime(class_data[4], '%H:%M')
                for j in range(i+1, len(classes)):
                    other_class_data = classes[j]
                    if other_class_data[2] == room:
                        other_start_time = datetime.strptime(other_class_data[3], '%H:%M')
                        other_end_time = datetime.strptime(other_class_data[4], '%H:%M')
                        if start_time < other_end_time and end_time > other_start_time:
                            roomConflicts += 1
                    if other_class_data[1] == instructor:
                        other_start_time = datetime.strptime(other_class_data[3], '%H:%M')
                        other_end_time = datetime.strptime(other_class_data[4], '%H:%M')
                        if start_time < other_end_time and end_time > other_start_time:
                            facultyClashes += 1

        conflicts = roomConflicts+facultyClashes

        print(f'Total number of Room conflicts: {roomConflicts}')
        print(f'Total number of Faculty conflicts: {facultyClashes}')
        print(f'Total number of conflicts: {conflicts}')
    


ga = GeneticAlgorithm()
ga.initializePopulation()
chromosome = ga.population[0]
# print(chromosome)
ga.fitnessEvaluation(chromosome)
# ga.getAvailableTimes()
# print(ga)