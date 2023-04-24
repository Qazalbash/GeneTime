# import datetime

# def is_end_time_within_limit(start_time_str, duration_minutes, end_time_limit_str):
#     # Convert start time string to datetime object
#     start_time = datetime.datetime.strptime(start_time_str, '%H:%M')
    
#     # Convert duration to timedelta object
#     duration = datetime.timedelta(minutes=int(duration_minutes))
    
#     # Calculate end time
#     end_time = start_time + duration
    
#     # Convert end time limit string to datetime object
#     end_time_limit = datetime.datetime.strptime(end_time_limit_str, '%H:%M')
    
#     # Compare end time to end time limit
#     if end_time <= end_time_limit:
#         return True
#     else:
#         return False


# print(is_end_time_within_limit("8:00",50,"9:00"))
import numpy as np
import random

lst1 = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
lst2 = ['Monday', 'Wednesday']
lst3 = set(lst1)-set(lst2)
print(random.sample(lst3, 1)[0])


