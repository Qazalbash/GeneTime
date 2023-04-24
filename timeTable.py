from datacleaning import DataCleaning
import datetime
import pandas as pd
from selectionSchemes import SelectionSchemes
import random
from pprint import pprint


class TimeTable(SelectionSchemes):

    def __init__(self, filename, populationSize, offspringsNumber, mutationRate) -> None:
        self.data = DataCleaning(filename)
        self.availableDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.faculty_working_hours ={}
        self.chromosome = {'Monday':{}, 'Tuesday':{}, 'Wednesday':{}, 'Thursday':{}, 'Friday':{}}
        
        self.population = []
        self.populationSize = populationSize
        self.offspringsNumber = offspringsNumber
        self.mutationRate = mutationRate

        self.DAY_START = "8:30"
        self.DAY_END = "19:00"
        
        self.initializeChromosome()
        # self.initializePopulation()

    def generate_start_time(self):
        hours = random.randint(8, 18)  # Schedule between 8am and 6pm
        minutes = random.randint(0, 11) * 5  # Schedule in multiples of 5
        return f'{hours:02d}:{minutes:02d}'

    # returns end time to start time using the duration
    def generate_time(self,startTime,duration):
        endTime = (pd.to_datetime(startTime) + pd.to_timedelta(duration, unit='m')).strftime('%H:%M')
        return endTime

    # Add 5 minutes to the datetime object
    def add_five_minutes(self,time_str):
        time_obj = datetime.datetime.strptime(time_str, '%H:%M')
        new_time_obj = time_obj + datetime.timedelta(minutes=5)
        new_time_str = new_time_obj.strftime('%H:%M')
        return new_time_str


    def is_end_time_within_limit(self,start_time_str, duration_minutes):
        start_time = datetime.datetime.strptime(start_time_str, '%H:%M')
        duration = datetime.timedelta(minutes=int(duration_minutes))
        end_time = start_time + duration
        end_time_limit = datetime.datetime.strptime(self.DAY_END, '%H:%M')
        if end_time <= end_time_limit:
            return True
        return False

    def initializeChromosome(self):
        for day in self.chromosome:
            self.chromosome[day]={room: [] for room in self.data.room_list}
        
        # Initialize faculty working hours for each day
        for instructor in self.data.instructor_list:
            if instructor not in self.faculty_working_hours:
                self.faculty_working_hours[instructor]={day: []for day in self.availableDays}
        
        print("--------Data DICT ---------")
        print(self.data.class_nbr_dict)

        print("--------CHROMOSOME-------")
        print(self.chromosome)

        print("--------FACULTY WORKING HOURS-------")
        print(self.faculty_working_hours)
        print(len(self.faculty_working_hours))

    def initializePopulation(self):
        for i in range(self.populationSize):
            self.initializeChromosome()
            for classNumber, data in self.data.class_nbr_dict.items():
                assigned_days = random.sample(self.availableDays, data['Frequency'])
                checkedDays = []
                for i in assigned_days:
                    checkedDays.append(i)
                for day in assigned_days:
                     room = random.sample(self.data.room_list,1)[0]
                     if len(self.chromosome[day][room]) == 0: #add faculty
                        self.chromosome[day][room].append([self.DAY_START,self.generate_time(self.DAY_START,data['Actual Class Duration']),classNumber])
                     else:
                        last_class=self.chromosome[day][room][-1]
                        current_class_start_time = self.add_five_minutes(last_class[1])
                        if self.is_end_time_within_limit(current_class_start_time,data['Actual Class Duration']): #add faculty
                              self.chromosome[day][room].append([current_class_start_time,self.generate_time(current_class_start_time,data['Actual Class Duration']),classNumber])
                        else:
                            is_roomfound = 0 
                            room_number_index = self.data.room_list.index(room)
                            startIndex = room_number_index
                            while True:
                                room_number_index=(room_number_index+1)%(len(self.data.room_list))
                                next_room = self.data.room_list[room_number_index]
                                if len(self.chromosome[day][next_room]) == 0: #add faculty
                                    self.chromosome[day][next_room].append([self.DAY_START,self.generate_time(self.DAY_START,data['Actual Class Duration']),classNumber])
                                else:
                                    last_class=self.chromosome[day][next_room][-1]
                                    current_class_start_time = self.add_five_minutes(last_class[1])
                                    if self.is_end_time_within_limit(current_class_start_time,data['Actual Class Duration']): #add faculty
                                        self.chromosome[day][next_room].append([current_class_start_time,self.generate_time(current_class_start_time,data['Actual Class Duration']),classNumber])
                                        is_roomfound=1
                                        break
                                if room_number_index == startIndex and is_roomfound == 0:
                                    break
                            
                                
                            if (is_roomfound == 0):
                                checkedDays.append(day)
                                potentialDays = set(self.data.room_list) - set(checkedDays)
                                nextDay = random.sample(potentialDays, 1)[0]
                                assigned_days.append(nextDay)

            self.population.append(self.chromosome)             
                                

         
        print(self.population[0])
        print(len(self.population))
    
    def checkClasses(self):
        counter = 0
        for day, dayInfo in self.chromosome.items():
            for roomNumber, roomInfo in dayInfo.items():
                counter+=len(roomInfo)
        print(counter)



filename = 'Spring 2023 Schedule.csv'
populationSize = 20
mutationRate = 0.2
offspringsNumber = 10
generations = 100


T1=TimeTable(filename, populationSize, offspringsNumber, mutationRate)
# T1.checkClasses()

    # def initeializePopulation(self):
    #     for i in range(self.populationSize):
    #         chromosome = {'Monday':{}, 'Tuesday':{}, 'Wednesday':{}, 'Thursday':{}, 'Friday':{}}
    #         for classNumber, data in self.dc.class_nbr_dict.items():
    #             days = random.sample(self.availableDays, data['Frequency'])
    #             for day in days:
    #                 room = random.sample(self.dc.room_list,1)[0]
    #                 startTime = self.generate_start_time()
    #                 endTime = (pd.to_datetime(startTime) + pd.to_timedelta(data['Actual Class Duration'], unit='m')).strftime('%H:%M')
    #                 chromosome[day][classNumber] = [data['Course title'], data['Instructor'], room, startTime, endTime]
    #         self.population.append(chromosome)

    # def fitnessEvaluation(self, chromosome):
    #     roomConflicts = 0
    #     facultyClashes = 0
    #     for day in chromosome.keys():
    #         classes = list(chromosome[day].values())
    #         # print(classes)
    #         for i in range(len(classes)):
    #             class_data = classes[i]
    #             room = class_data[2]
    #             instructor = class_data[1]
    #             start_time = datetime.strptime(class_data[3], '%H:%M')
    #             end_time = datetime.strptime(class_data[4], '%H:%M')
    #             for j in range(i+1, len(classes)):
    #                 other_class_data = classes[j]
    #                 if other_class_data[2] == room:
    #                     other_start_time = datetime.strptime(other_class_data[3], '%H:%M')
    #                     other_end_time = datetime.strptime(other_class_data[4], '%H:%M')
    #                     if start_time < other_end_time and end_time > other_start_time:
    #                         roomConflicts += 1
    #                 if other_class_data[1] == instructor:
    #                     other_start_time = datetime.strptime(other_class_data[3], '%H:%M')
    #                     other_end_time = datetime.strptime(other_class_data[4], '%H:%M')
    #                     if start_time < other_end_time and end_time > other_start_time:
    #                         facultyClashes += 1

    #     conflicts = roomConflicts+facultyClashes
    #     fitness = 1/(1+conflicts)
    #     return fitness

        # print(f'Total number of Room conflicts: {roomConflicts}')
        # print(f'Total number of Faculty conflicts: {facultyClashes}')
        # print(f'Total number of conflicts: {conflicts}')