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


lst = [3, 48, 91]
lst.insert(0, 10)
print(lst)
