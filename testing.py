import datetime
import copy

# def find_free_slot(schedule):
#     days = ["Monday", "Tuesday"]
#     start_time = datetime.datetime.strptime("08:00", "%H:%M")
#     end_time = datetime.datetime.strptime("18:00", "%H:%M")
#     _delta = datetime.timedelta(minutes=5)
#     delta = datetime.timedelta(hours=1)

#     # iterate over all possible timeslots
#     while start_time + delta <= end_time:
#         end_slot = start_time + delta
#         free = True
#         # check if the timeslot overlaps with any existing classes
#         for day in days:
#             for room in schedule[day]:
#                 for slot in schedule[day][room]:
#                     slot_start = datetime.datetime.strptime(slot[0], "%H:%M")
#                     slot_end = datetime.datetime.strptime(slot[1], "%H:%M")
#                     if (start_time < slot_end) and (slot_start < end_slot):
#                         free = False
#                         break
#                 if not free:
#                     break
#             if not free:
#                 break
#         # if the timeslot is free, return it
#         if free:
#             return [start_time.strftime("%H:%M"), end_slot.strftime("%H:%M")]
#         start_time += _delta
#     # if no free timeslot is found, return None
#     return None


# schedule = {
#     "Monday": {
#         "room1": [["08:00", "09:00"], ["09:05", "10:30"]],
#         "room2": [["08:30", "9:45"], ["09:50", "10:40"], ["10:50", "12:40"]],
#     },
#     "Tuesday": {
#         "room1": [["09:30", "10:30"], ["15:50", "16:30"]],
#         "room2": [["13:50", "14:45"]],
#     },
# }

# free_slot = find_free_slot(schedule)
# if free_slot:
#     print("Free one-hour time slot:", free_slot)
# else:
#     print("No free one-hour time slot found in the week.")


# lst = [3, 48, 91]
# lst.insert(0, 10)
# print(lst)

studentSchedules = {'Student 1': {'Monday': [["8:30", "9:45", 1090]], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 2': {'Monday': [["8:30", "9:45", 1090]], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 3': {'Monday': [], 'Tuesday': [['14:00', '15:00', 1091], ['15:05', '16:00', 1092]], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 4': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 5': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 6': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 7': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 8': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 9': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 10': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 11': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 12': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 13': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 14': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 15': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 16': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 17': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 18': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 19': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 20': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 21': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 22': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 23': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 24': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 25': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 26': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 27': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 28': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}, 'Student 29': {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}}

def updateStudentSchedules(number, day1, day2, start, end, studentSchedules, lst):
    updatedStudentSchedules = copy.deepcopy(studentSchedules)
    lstStudents = lst[number]
    for student in lstStudents:
        studentDaySchedule = studentSchedules[student][day1]
        for _class in studentDaySchedule:
            if _class[2] == number:
                studentDaySchedule.remove(_class)
                updatedStudentSchedules[student][day1] = studentDaySchedule
                break
        updatedStudentSchedules[student][day2].append([start, end, number])
    return updatedStudentSchedules

lst = {1090: ['Student 1', 'Student 2', 'Student 3', 'Student 4', 'Student 5', 'Student 6', 'Student 7', 'Student 8', 'Student 9', 'Student 10', 'Student 11', 'Student 12', 'Student 13', 'Student 14', 'Student 15', 'Student 16', 'Student 17', 'Student 18', 'Student 19', 'Student 20', 'Student 21', 'Student 22', 'Student 23', 'Student 24', 'Student 25', 'Student 26', 'Student 27', 'Student 28', 'Student 29']}

print(updateStudentSchedules(1090, 'Monday', 'Tuesday', '8:30', '9:45', studentSchedules, lst))
