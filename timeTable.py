from datacleaning import DataCleaning
import datetime
import pandas as pd
from selectionSchemes import SelectionSchemes
import random
from pprint import pprint
from classDetails import ClassDetails


class TimeTable(SelectionSchemes):

    def __init__(self, filename, populationSize, offspringsNumber, mutationRate) -> None:
        self.data = DataCleaning(filename)
        self.availableDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.population = []
        self.populationSize = populationSize
        self.offspringsNumber = offspringsNumber
        self.mutationRate = mutationRate
        self.DAY_START = "8:30"
        self.DAY_END = "18:00"
        self.NUM_ROOMS_WEEKLY = 150
        self.initializePopulation()

    # def generate_start_time(self):
    #     hours = random.randint(8, 18)  # Schedule between 8am and 6pm
    #     minutes = random.randint(0, 11) * 5  # Schedule in multiples of 5
    #     return f'{hours:02d}:{minutes:02d}'

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
            C1=ClassDetails()
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
                        C1.addClass(classNumber, day, room, current_class_start_time, end_time )
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
                                C1.addClass(classNumber, day,  next_room, current_class_start_time, end_time )
                                break
                            if room_number_index == startIndex and is_roomfound == 0:
                                break
                        # if room not found on the day, then we randomly select another day and look for a suitable room on that day
                        if (is_roomfound == 0):
                            potentialDays = set(self.availableDays) - set(assigned_days)
                            nextDay = random.sample(potentialDays, 1)[0]
                            assigned_days.append(nextDay)

            fitness=self.fitnessEvaluation(chromosome,C1)
            self.population.append([fitness,chromosome])   
            

    def fitnessEvaluation(self,chromosome, C1):
        counter_same_time=self.SOFT_class_at_same_time(C1)
        counter_same_room=self.SOFT_class_in_same_room(C1)
        counter_room_withinlimit = self.SOFT_checkEndTimeLimit(chromosome)
        freeslotavailable=self.SOFT_find_free_slot(chromosome)

        fitness_same_room = (counter_same_room/self.data.numclasses_multipleinstances)*100
        fitness_same_time = (counter_same_time/self.data.numclasses_multipleinstances)*100
        fitness_withinlimit = (counter_room_withinlimit/self.NUM_ROOMS_WEEKLY)*100
        
        if freeslotavailable:
            fitness_free_slot = 200
        else:
            fitness_free_slot=0


        totalFitness = fitness_same_room+fitness_same_time+fitness_withinlimit+fitness_free_slot
        return totalFitness
        
                                
    # just to check if weekly schedule has all 447 classes
    def checkClasses(self, chromosome):
        counter = 0
        for day, dayInfo in chromosome.items():
            for roomNumber, roomInfo in dayInfo.items():
                counter+=len(roomInfo)
        print(counter)

    
    def SOFT_find_free_slot(self,chromosome):
        # days = ["Monday", "Tuesday"]
        start_time = datetime.datetime.strptime(self.DAY_START, "%H:%M")
        end_time = datetime.datetime.strptime(self.DAY_END, "%H:%M")
        _delta = datetime.timedelta(minutes=5)
        delta = datetime.timedelta(hours=1)

        # iterate over all possible timeslots
        while start_time + delta <= end_time:
            end_slot = start_time + delta
            free = True
            # check if the timeslot overlaps with any existing classes
            for day in self.availableDays:
                for room in chromosome[day]:
                    for slot in chromosome[day][room]:
                        slot_start = datetime.datetime.strptime(slot[0], "%H:%M")
                        slot_end = datetime.datetime.strptime(slot[1], "%H:%M")
                        if (start_time < slot_end) and (slot_start < end_slot):
                            free = False
                            break
                    if not free:
                        break
                if not free:
                    break
            # if the timeslot is free, return it
            if free:
                print [start_time.strftime("%H:%M"), end_slot.strftime("%H:%M")]
                return
            start_time += _delta
        # if no free timeslot is found, return None
        return None
        
    
    def SOFT_checkEndTimeLimit(self, chromosome):
        endTimes = []
        count =0
        for day, dayInfo in chromosome.items():
            for room, roomInfo in dayInfo.items():
                if len(roomInfo) != 0:
                    lastClass = roomInfo[-1]
                    endTime = datetime.datetime.strptime(lastClass[1], '%H:%M')
                    official_day_end = datetime.datetime.strptime(self.DAY_END, '%H:%M')
                    buffer_official_day_end = official_day_end - datetime.timedelta(minutes=60)
                    if endTime <= official_day_end  and endTime >= buffer_official_day_end:
                        count+=1
        return (self.NUM_ROOMS_WEEKLY-count)

    def SOFT_class_in_same_room(self,C1):
        same_room_counter=0
        for class_number , instances in C1.Class_Dict.items():
            flag=True
            if len(instances) > 1:
                room_no=instances[0][1]
                for class_instance in instances[1:]:
                    if class_instance[1] != room_no:
                        flag=False
            if len(instances) > 1 and flag == True:
                same_room_counter+=1

        return same_room_counter

    def SOFT_class_at_same_time(self,C1):
        same_time_counter=0
        for class_number , instances in C1.Class_Dict.items():
            flag=True
            if len(instances) > 1:
                start_time=datetime.datetime.strptime(instances[0][2], '%H:%M')
                for class_instance in instances[1:]:
                    next_start_time=datetime.datetime.strptime(class_instance[2], '%H:%M')
                    if next_start_time!= start_time:
                        flag = False
            if flag:
                same_time_counter+=1

        return same_time_counter

        

filename = 'Spring 2023 Schedule.csv'
populationSize = 10
mutationRate = 0.2
offspringsNumber = 10
generations = 100


T1=TimeTable(filename, populationSize, offspringsNumber, mutationRate)
# print(T1.population)
chromosome = T1.population[0]
print(chromosome)
# print(chromosome)
# T1.checkClasses(chromosome[1])
# print(T1.find_free_slot(chromosome))
# print(T1.SOFT_checkEndTimeLimit(chromosome[1]))
# print(T1.SOFT_class_in_same_room(chromosome))
