import csv
import glob
import json
import os
from datetime import datetime

search_name = "test0"
#
# if not os.path.exists("r_logs"):
#     os.makedirs("r_logs")
#
# if not os.path.exists(f"./r_logs/{search_name}"):
#     os.makedirs(f"./r_logs/{search_name}")
#
#
#
# profile_urls = (("['https://www.linkedin.com/in/dhruvnaheta?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADI99DUBZ-jmmvPM2QrikJHB9OdAYaFqmiQ', 'https://www.linkedin.com/in/anagh-agarwal-80265314b?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACQ5pcIBf4NmiCyJXDrV0NuVUrXyj-cL0nc', 'https://www.linkedin.com/in/panat-wareerinsiri-titan-2868b11a2?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC95g0YBzQAAcWv4M_7RLgUUREtF53fXAGs', 'https://www.linkedin.com/in/charles-chansa-1186ba125?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAB7k1yQB2bwectLSdjtco2j-xcG-CVr0yvA', 'https://www.linkedin.com/in/kohei-hayakawa-72340b149?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACPVjksBxLJ6oTqmZt5XTktzOJa05GfmxDY', 'https://www.linkedin.com/in/joshuafsacks?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABWYatIBR8QFuDy8lphBPll3KGSXlKhUhN0', 'https://www.linkedin.com/in/kchotita?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADVBqckBe17girBGBqP1JT3b-_0vQR71_nQ', 'https://www.linkedin.com/in/prim-phongprapat?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC5Db_ABAiWuO2jYije7hby7pUxC9ZmOgCU', 'https://www.linkedin.com/in/motoioyane?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACHYHz8BdO1dcTrcg9Q_i2D3O0C0VnKFoF4', 'https://www.linkedin.com/in/luke-rivers?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACqEzBABER39UXUPXzln7sEQWV5scK4ggDE']").split(","))
# for i in range(len(profile_urls)):
#     profile_urls[i] = profile_urls[i].replace("'","").replace("[","").replace("]","")
#
# print(profile_urls)
#
# ALog = open(f"r_logs/{search_name}/{str(datetime.strftime(datetime.now(), '%d-%m-%y'))}_{search_name}_ALog.txt","w+")
# ALog.writelines(profile_urls)

# if os.path.exists("./r_logs/test0/02-01-24_test0_ALog.txt"):
#     loadedLogFile = open("./r_logs/test0/02-01-24_test0_ALog.txt", "r")
#     loadedLog = loadedLogFile.readlines()
#
#     print(loadedLog)


# with open('./Data/06-01-24_M0101_search_results.json', 'w',
#           encoding="utf-8-sig") as file:
#     file.write(json.dumps(final_result, ensure_ascii=False))
#     file.close()


with open('./Data/06-01-24_M0101_search_results.json', 'r', encoding="utf-8-sig") as file:
    x = file.read()
    y = json.loads(x)
    print(len(y))
    file.close()

# with open("./Data/final_v1.csv", "w", encoding="utf-8-sig") as out:
#     out.write("Name,Languages,Primary institution,Years of experience,International school?,School country,"
#               "School primary curriculum,More Details,Interested in mentoring?,Location\n")
#     for each in y:
#         out.write(f"{each['name']},{each['languages']},{each['primaryInstitution']},{each['yearsOfExperience']},{each['internationalSchool']},{each['schoolCountry']},{each['schoolPrimaryCurriculum']},{each['moreDetails']},{each['interestedInMentoring']},{each['location']}\n")
#     out.close()

with open("./Data/final_v1.csv", 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    fields = ["Name", "Languages", "Primary institution", "Years of experience", "International school?",
              "School country", "School primary curriculum", "More Details", "Interested in mentoring?", "Location"]
    writer.writerow(fields)
    for each in y:
        writer.writerow([each["name"], each["languages"], each["primaryInstitution"], each["yearsOfExperience"],
                         each["internationalSchool"], each["schoolCountry"], each["schoolPrimaryCurriculum"],
                         each["moreDetails"], each["interestedInMentoring"], each["location"]])
    file.close()
