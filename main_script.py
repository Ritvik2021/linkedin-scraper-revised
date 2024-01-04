import A_Search as A
import B_Profiles as B
import C_Insights as C
import json

print("start")

#Example variable values:
# url = 'https://www.linkedin.com/search/results/people/?keywords=%22undergraduate%20student%20at%20university%20of%20British%20Columbia%22%20%22international%22&origin=GLOBAL_SEARCH_HEADER&sid=2cf'
# length = 1
# user = 'g.iademarco@yahoo.it'
# password = 'Millie2020'

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("url", type=str)
parser.add_argument("length", type=int)
parser.add_argument("email", type=str)
parser.add_argument("pw", type=str)
args = parser.parse_args()

url = args.url
length = args.length
user = args.email
password = args.pw

# print((url, length, user, password))

list_of_profiles = A.search(url,length,user,password)
print(len(list_of_profiles))
linkedIn_profiles = B.profiles(list_of_profiles[:length],user,password)
print(len(linkedIn_profiles))
analysed = C.insights(linkedIn_profiles) #This returns a JSON formatted string.
print(len(analysed))

# import csv
# import json
# import io
# iofile = io.StringIO()
# analysed = json.loads(analysed)
# writer = csv.writer(iofile)
# writer.writerow([
#   'Id',
#   'Name',
#   'Languages',
#   'Primary institution',
#   'Years of experience',
#   'International school?',
#   'School country',
#   'School primary curriculum',
#   'More Details',
#   'Interested in mentoring?',
#   'Location',
#   'LinkedIn url',
#   'Full info'  
# ])
# for each in analysed:
#   writer.writerow(each.values())
print("DATA_START" + analysed + "DATA_END")
print("end")

# Should you want to visualise the result as a csv file instead of a JSON string:

