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

lst1 = set(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
lst2 = set(['Monday', 'Wednesday'])
lst3 = lst1-lst2
print(lst3)