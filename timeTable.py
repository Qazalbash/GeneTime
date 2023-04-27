import datetime
import random
from pprint import pprint
import copy
import pandas as pd

from classDetails import ClassDetails
from datacleaning import DataCleaning
from selectionSchemes import SelectionSchemes


class TimeTable(SelectionSchemes):
    TIME_GAP = 15  # 15 minutes gap between classes

    def __init__(
        self, filename, populationSize, offspringsNumber, mutationRate
    ) -> None:
        self.data = DataCleaning(filename)
        self.availableDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.population = []
        self.populationSize = populationSize
        self.offspringsNumber = offspringsNumber
        self.mutationRate = mutationRate
        self.DAY_START = "8:30"
        self.DAY_END = "18:00"
        self.NUM_ROOMS_WEEKLY = 150
        # self.initializePopulation()

    # def generate_start_time(self):
    #     hours = random.randint(8, 18)  # Schedule between 8am and 6pm
    #     minutes = random.randint(0, 11) * 5  # Schedule in multiples of 5
    #     return f'{hours:02d}:{minutes:02d}'

    # returns end time to start time using the duration
    def generate_time(self, startTime, duration):
        endTime = (
            pd.to_datetime(startTime) + pd.to_timedelta(duration, unit="m")
        ).strftime("%H:%M")
        return endTime

    # Add 5 minutes to the datetime object
    def add_five_minutes(self, time_str):
        time_obj = datetime.datetime.strptime(time_str, "%H:%M")
        new_time_obj = time_obj + datetime.timedelta(minutes=TimeTable.TIME_GAP)
        new_time_str = new_time_obj.strftime("%H:%M")
        return new_time_str

    def is_end_time_within_limit(self, start_time_str, duration_minutes):
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M")
        duration = datetime.timedelta(minutes=int(duration_minutes))
        end_time = start_time + duration
        end_time_limit = datetime.datetime.strptime(self.DAY_END, "%H:%M")
        if end_time <= end_time_limit:
            return True
        return False

    def initializeChromosome(self):
        chromosome = {}
        for day in self.availableDays:
            chromosome[day] = {room: [] for room in self.data.room_list}

        # Initialize faculty working hours for each day
        faculty_working_hours = {}
        for instructor in self.data.instructor_list:
            faculty_working_hours[instructor] = {day: [] for day in self.availableDays}

        return chromosome, faculty_working_hours

    # returns True if an instructor is teaching a class on the same day at the same time in two different rooms, otherwise returns False
    def facultyClash(self, instructor, day, start_time, end_time, faculty_working_hours):
        start_time = datetime.datetime.strptime(start_time, "%H:%M")
        end_time = datetime.datetime.strptime(end_time, "%H:%M")
        daily_schedule = faculty_working_hours[instructor][day]
        if len(daily_schedule) == 0:
            return False
        else:
            for _class in daily_schedule:
                other_start_time = datetime.datetime.strptime(_class[0], "%H:%M")
                other_end_time = datetime.datetime.strptime(_class[1], "%H:%M")
                if start_time < other_end_time and end_time > other_start_time:
                    return True
            return False

    # adds the timeslot to the instructor's weekly schedule
    def addToFacultySchedule(
        self, instructor, day, start_time, end_time, classNumber, faculty_working_hours
    ):
        faculty_working_hours[instructor][day].append([start_time, end_time, classNumber])
        return faculty_working_hours

    def initializePopulation(self):
        for i in range(self.populationSize):
            chromosome, faculty_working_hours = self.initializeChromosome()
            # self.faculty_working_hours = faculty_working_hours
            C1 = ClassDetails()
            for classNumber, data in self.data.class_nbr_dict.items():
                # assigned random days for each class
                assigned_days = random.sample(self.availableDays, data["Frequency"])
                # iterates through days to find a suitable room on each day
                for day in assigned_days:
                    is_roomfound = 0
                    room = random.sample(self.data.room_list, 1)[0]
                    if len(chromosome[day][room]) == 0:
                        current_class_start_time = self.DAY_START
                    else:
                        last_class = chromosome[day][room][-1]
                        current_class_start_time = self.add_five_minutes(last_class[1])
                    # searching for a suitable room (with no faculty clash and ending before time limit) on same day
                    end_time = self.generate_time(
                        current_class_start_time, data["Actual Class Duration"]
                    )
                    if self.facultyClash(
                        data["Instructor"], day, current_class_start_time, end_time, faculty_working_hours
                    ) == False and self.is_end_time_within_limit(
                        current_class_start_time, data["Actual Class Duration"]
                    ):
                        chromosome[day][room].append(
                            [current_class_start_time, end_time, classNumber]
                        )
                        faculty_working_hours = self.addToFacultySchedule(
                            data["Instructor"],
                            day,
                            current_class_start_time,
                            end_time,
                            classNumber,
                            faculty_working_hours,
                        )
                        is_roomfound = 1  # room found exit loop
                        C1.addClass(
                            classNumber, day, room, current_class_start_time, end_time
                        )
                    else:
                        room_number_index = self.data.room_list.index(room)
                        startIndex = room_number_index

                        while True:
                            room_number_index = (room_number_index + 1) % (
                                len(self.data.room_list)
                            )
                            next_room = self.data.room_list[room_number_index]
                            if len(chromosome[day][next_room]) == 0:
                                current_class_start_time = self.DAY_START
                            else:
                                last_class = chromosome[day][next_room][-1]
                                current_class_start_time = self.add_five_minutes(
                                    last_class[1]
                                )

                            end_time = self.generate_time(
                                current_class_start_time, data["Actual Class Duration"]
                            )
                            if self.facultyClash(
                                data["Instructor"],
                                day,
                                current_class_start_time,
                                end_time,
                                faculty_working_hours
                            ) == False and self.is_end_time_within_limit(
                                current_class_start_time, data["Actual Class Duration"]
                            ):  # add faculty
                                chromosome[day][next_room].append(
                                    [current_class_start_time, end_time, classNumber]
                                )
                                faculty_working_hours = self.addToFacultySchedule(
                                    data["Instructor"],
                                    day,
                                    current_class_start_time,
                                    end_time,
                                    classNumber,
                                    faculty_working_hours,
                                )
                                is_roomfound = 1
                                C1.addClass(
                                    classNumber,
                                    day,
                                    next_room,
                                    current_class_start_time,
                                    end_time,
                                )
                                break
                            if room_number_index == startIndex and is_roomfound == 0:
                                break
                        # if room not found on the day, then we randomly select another day and look for a suitable room on that day
                        if is_roomfound == 0:
                            potentialDays = set(self.availableDays) - set(assigned_days)
                            nextDay = random.sample(potentialDays, 1)[0]
                            assigned_days.append(nextDay)

            fitness = self.fitnessEvaluation(chromosome, C1)
            self.population.append([fitness, chromosome, C1, faculty_working_hours])


    def fitnessEvaluation(self, chromosome, C1):
        counter_same_time = self.SOFT_class_at_same_time(C1)
        counter_same_room = self.SOFT_class_in_same_room(C1)
        counter_room_withinlimit = self.SOFT_checkEndTimeLimit(chromosome)
        freeslotavailable = self.SOFT_find_free_slot(chromosome)

        fitness_same_room = (
            counter_same_room / self.data.numclasses_multipleinstances
        ) * 100
        fitness_same_time = (
            counter_same_time / self.data.numclasses_multipleinstances
        ) * 100
        fitness_withinlimit = (counter_room_withinlimit / self.NUM_ROOMS_WEEKLY) * 100

        if freeslotavailable:
            fitness_free_slot = 200
        else:
            fitness_free_slot = 0

        totalFitness = (
            fitness_same_room
            + fitness_same_time
            + fitness_withinlimit
            + fitness_free_slot
        )
        return totalFitness

    # just to check if weekly schedule has all 447 classes
    def checkClasses(self, chromosome):
        counter = 0
        for day, dayInfo in chromosome.items():
            for roomNumber, roomInfo in dayInfo.items():
                counter += len(roomInfo)
        print(counter)

    def SOFT_find_free_slot(self, chromosome):
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
                print[start_time.strftime("%H:%M"), end_slot.strftime("%H:%M")]
                return
            start_time += _delta
        # if no free timeslot is found, return None
        return None

    def SOFT_checkEndTimeLimit(self, chromosome):
        endTimes = []
        count = 0
        for day, dayInfo in chromosome.items():
            for room, roomInfo in dayInfo.items():
                if len(roomInfo) != 0:
                    lastClass = roomInfo[-1]
                    endTime = datetime.datetime.strptime(lastClass[1], "%H:%M")
                    official_day_end = datetime.datetime.strptime(self.DAY_END, "%H:%M")
                    buffer_official_day_end = official_day_end - datetime.timedelta(
                        minutes=60
                    )
                    if (
                        endTime <= official_day_end
                        and endTime >= buffer_official_day_end
                    ):
                        count += 1
        return self.NUM_ROOMS_WEEKLY - count

    def SOFT_class_in_same_room(self, C1):
        same_room_counter = 0
        for class_number, instances in C1.Class_Dict.items():
            flag = True
            if len(instances) > 1:
                room_no = instances[0][1]
                for class_instance in instances[1:]:
                    if class_instance[1] != room_no:
                        flag = False
            if len(instances) > 1 and flag == True:
                same_room_counter += 1

        return same_room_counter

    def SOFT_class_at_same_time(self, C1):
        same_time_counter = 0
        for class_number, instances in C1.Class_Dict.items():
            flag = True
            if len(instances) > 1:
                start_time = datetime.datetime.strptime(instances[0][2], "%H:%M")
                for class_instance in instances[1:]:
                    next_start_time = datetime.datetime.strptime(
                        class_instance[2], "%H:%M"
                    )
                    if next_start_time != start_time:
                        flag = False
            if flag:
                same_time_counter += 1

        return same_time_counter

    def mutation(self, chromosome, C1, faculty_working_hours, itteration=10):
    # def mutation(self, chromosome, faculty_working_hours, itteration=10):
        mutatedChromosome = copy.deepcopy(chromosome)
        if itteration == 0:
            return mutatedChromosome, C1, faculty_working_hours
            # return mutatedChromosome

        day1 = random.choice(self.availableDays)
        day2 = random.choice(self.availableDays)
        while day1 == day2:
            day2 = random.choice(self.availableDays)

        room1 = random.choice(list(chromosome[day1].keys()))

        class1 = mutatedChromosome[day1][room1]

        if len(class1) == 0:
            return self.mutation(mutatedChromosome, C1, faculty_working_hours, itteration - 1)
            # return self.mutation(mutatedChromosome, faculty_working_hours, itteration-1)
        class_index = random.randint(0, len(class1) - 1)

        start, end, number = class1[class_index]

        for room2 in mutatedChromosome[day2].keys():
            class2 = mutatedChromosome[day2][room2]
            if any(number == c[2] for c in class2):
                return self.mutation(mutatedChromosome, C1, faculty_working_hours, itteration - 1)
                # return self.mutation(mutatedChromosome, faculty_working_hours, itteration-1)

        room2 = random.choice(list(mutatedChromosome[day2].keys()))
        class2 = mutatedChromosome[day2][room2]

        # print(class1, class2, sep="\n")

        if any(number == c[2] for c in class2):
            return self.mutation(mutatedChromosome, C1, faculty_working_hours, itteration - 1)
            # return self.mutation(mutatedChromosome, faculty_working_hours, itteration-1)

        duration = instructor = self.data.class_nbr_dict[number][
            "Actual Class Duration"
        ]

        # TODO the function is returning wrong time
        if len(class2) == 0:
            start = self.DAY_START
            end = self.generate_time(start, duration)
        else:
            start = self.generate_time(class2[-1][1], TimeTable.TIME_GAP)
            end = self.generate_time(start, duration)

        if self.is_end_time_within_limit(end, duration):
            return self.mutation(mutatedChromosome, C1, faculty_working_hours, itteration - 1)
            # return self.mutation(mutatedChromosome, faculty_working_hours, itteration-1)

        instructor = self.data.class_nbr_dict[number]["Instructor"]

        if self.facultyClash(instructor, day2, start, end, faculty_working_hours):
            return self.mutation(mutatedChromosome, C1, faculty_working_hours, itteration - 1)
            # return self.mutation(mutatedChromosome, faculty_working_hours, itteration-1)

        class2.append([start, end, number])
        del class1[class_index]

        # print(class1, class2, sep="\n")

        mutatedChromosome[day1][room1] = class1
        mutatedChromosome[day2][room2] = class2

        updated_faculty_working_hours = self.updateFacultySchedule(instructor, day1, number, day2, start, end, faculty_working_hours)
        classDetails = C1.Class_Dict
        C2 = ClassDetails()
        C2.Class_Dict = self.updateClassDetails(number, day1, room1, start, end, day2, room2, classDetails)

        return mutatedChromosome, C2, updated_faculty_working_hours

        # return mutatedChromosome
    
    
    def updateFacultySchedule(self, instructor, day1, number, day2, start, end, faculty_working_hours):
        updated_faculty_working_hours = copy.deepcopy(faculty_working_hours)
        lstOfClasses = updated_faculty_working_hours[instructor][day1]
        for _class in lstOfClasses:
            if _class[2] == number:
                lstOfClasses.remove(_class)
                updated_faculty_working_hours[instructor][day1] = lstOfClasses
                break
        updated_faculty_working_hours[instructor][day2].append([start, end, number])
        return updated_faculty_working_hours
    
    def updateClassDetails(self, number, day1, room1, start, end, day2, room2, classDetails):
        updatedClassDetails = copy.deepcopy(classDetails)
        lstInstances = updatedClassDetails[number]
        for instance in lstInstances:
            if instance[0] == day1 and instance[1] == room1:
                lstInstances.remove(instance)
                updatedClassDetails[number] = lstInstances
                break
        updatedClassDetails[number].append([day2, room2, start, end])
        return updatedClassDetails


    def crossover(self, p1, p2):
        offspringOneChromosome, offspringOneClassDetails, offspringOneFacultyHours = self.mutation(p1[1], p1[2], p1[3])
        offspringTwoChromosome, offspringTwoClassDetails, offspringTwoFacultyHours = self.mutation(p2[1], p2[2], p2[3])

        # print('OFFSPRING-------------------------------------------------')

        offspringOneFitness = self.fitnessEvaluation(offspringOneChromosome, offspringOneClassDetails)
        offspringTwoFitness = self.fitnessEvaluation(offspringTwoChromosome, offspringTwoClassDetails)

        offspringOne = [offspringOneFitness, offspringOneChromosome, offspringOneClassDetails, offspringOneFacultyHours]
        offspringTwo = [offspringTwoFitness, offspringTwoChromosome, offspringTwoClassDetails, offspringTwoFacultyHours]

        return offspringOne, offspringTwo


# filename = "Spring 2023 Schedule.csv"
# populationSize = 10
# mutationRate = 0.2
# offspringsNumber = 10
# generations = 100


# T1 = TimeTable(filename, populationSize, offspringsNumber, mutationRate)
# # print(T1.population)
# chromosome = T1.population[0]
# print(chromosome[2].Class_Dict)
# print("-----------------------------------------------------------------")
# T1.mutation(chromosome[1], chromosome[2], chromosome[3])
# T1.mutation(chromosome[1], chromosome[3])
# print(T1.data)
# print(chromosome)
# T1.checkClasses(chromosome[1])
# print(T1.find_free_slot(chromosome))
# print(T1.SOFT_checkEndTimeLimit(chromosome[1]))
# print(T1.SOFT_class_in_same_room(chromosome))
