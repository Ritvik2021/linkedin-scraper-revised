import json
import time
import datetime


# print(str(datetime.strftime(datetime.now(), '%d-%m-%y')))
#
# login_file = open("logins.txt", "r+")
# temp_data = json.loads(login_file.read())
# print(temp_data[0])

def avg(coll):
    return sum(tuple(coll)) / len(coll)
#
#
# time_taken = []
# for i in range(11):
#     old = datetime.datetime.now()
#     time.sleep(1)
#     new = datetime.datetime.now()
#     time_taken.append((new - old))
#
#     current_avg = average_timedelta = sum(time_taken, datetime.timedelta(0)) / len(time_taken)
#     print(f"{i}/10 \t Estimated time remaining: {current_avg * (10 - i)}")
