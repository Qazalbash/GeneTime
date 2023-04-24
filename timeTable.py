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
        self.population = []
        self.populationSize = populationSize
        self.offspringsNumber = offspringsNumber
        self.mutationRate = mutationRate
        self.DAY_START = "8:30"
        self.DAY_END = "19:00"
        self.initializePopulation()

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
        new_time_obj = time_obj + datetime.timedelta(minutes=15)
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
        chromosome = {'Monday':{}, 'Tuesday':{}, 'Wednesday':{}, 'Thursday':{}, 'Friday':{}}
        for day in chromosome:
            chromosome[day]={room: [] for room in self.data.room_list}
        
        # Initialize faculty working hours for each day
        faculty_working_hours = {}
        for instructor in self.data.instructor_list:
            faculty_working_hours[instructor]={day: []for day in self.availableDays}

        return chromosome, faculty_working_hours
        
    # returns True if an instructor is teaching a class on the same day at the same time in two different rooms, otherwise returns False
    def facultyClash(self, instructor,day, start_time, end_time, faculty_working_hours):
        start_time = datetime.datetime.strptime(start_time, '%H:%M')
        end_time = datetime.datetime.strptime(end_time, '%H:%M')
        daily_schedule=faculty_working_hours[instructor][day]
        if len(daily_schedule) == 0:
                return False
        else:
            for _class in daily_schedule:
                other_start_time = datetime.datetime.strptime(_class[0], '%H:%M')
                other_end_time =  datetime.datetime.strptime(_class[1], '%H:%M')
                if start_time < other_end_time and end_time > other_start_time:
                    return True
            return False
        
    # adds the timeslot to the instructor's weekly schedule
    def addToFacultySchedule(self, instructor, day, start_time, end_time, faculty_working_hours):
        faculty_working_hours[instructor][day].append([start_time,end_time])
        return faculty_working_hours


    def initializePopulation(self):
        for i in range(self.populationSize):
            chromosome, faculty_working_hours = self.initializeChromosome()

            for classNumber, data in self.data.class_nbr_dict.items():
                assigned_days = random.sample(self.availableDays, data['Frequency'])  # assigned random days for each class       
                for day in assigned_days:  # iterates through days to find a suitable room on each day
                    is_roomfound = 0
                    room = random.sample(self.data.room_list,1)[0]
                    if len(chromosome[day][room]) == 0:           
                        current_class_start_time = self.DAY_START
                    else:
                        last_class = chromosome[day][room][-1]
                        current_class_start_time = self.add_five_minutes(last_class[1])
                    # searching for a suitable room (with no faculty clash and ending before time limit) on same day
                    end_time = self.generate_time(current_class_start_time,data['Actual Class Duration'])
                    if  self.facultyClash(data["Instructor"], day,current_class_start_time, end_time, faculty_working_hours) == False and self.is_end_time_within_limit(current_class_start_time,data['Actual Class Duration']):
                        chromosome[day][room].append([current_class_start_time,end_time,classNumber])
                        faculty_working_hours = self.addToFacultySchedule(data["Instructor"],day, current_class_start_time, end_time, faculty_working_hours)
                        is_roomfound = 1  # room found exit loop
                    else:                             
                        room_number_index = self.data.room_list.index(room)
                        startIndex = room_number_index
                        
                        while True:
                            room_number_index=(room_number_index+1)%(len(self.data.room_list))
                            next_room = self.data.room_list[room_number_index]
                            if len(chromosome[day][next_room]) == 0:
                                current_class_start_time = self.DAY_START
                            else:
                                last_class = chromosome[day][next_room][-1]
                                current_class_start_time = self.add_five_minutes(last_class[1])

                            end_time = self.generate_time(current_class_start_time,data['Actual Class Duration'])
                            if  self.facultyClash(data["Instructor"], day,current_class_start_time, end_time, faculty_working_hours) == False and  self.is_end_time_within_limit(current_class_start_time,data['Actual Class Duration']): #add faculty
                                chromosome[day][next_room].append([current_class_start_time,end_time,classNumber])
                                faculty_working_hours = self.addToFacultySchedule(data["Instructor"],day, current_class_start_time, end_time,faculty_working_hours)
                                is_roomfound=1
                                break
                            if room_number_index == startIndex and is_roomfound == 0:
                                break
                        # if room not found on the day, then we randomly select another day and look for a suitable room on that day
                        if (is_roomfound == 0):
                            potentialDays = set(self.availableDays) - set(assigned_days)
                            nextDay = random.sample(potentialDays, 1)[0]
                            assigned_days.append(nextDay)

            self.population.append(chromosome)             
                                
    # just to check if weekly schedule has all 447 classes
    def checkClasses(self, chromosome):
        counter = 0
        for day, dayInfo in chromosome.items():
            for roomNumber, roomInfo in dayInfo.items():
                counter+=len(roomInfo)
        print(counter)



filename = 'Spring 2023 Schedule.csv'
populationSize = 20
mutationRate = 0.2
offspringsNumber = 10
generations = 100


T1=TimeTable(filename, populationSize, offspringsNumber, mutationRate)
chromosome = T1.population[19]
print(chromosome)
T1.checkClasses(chromosome)
