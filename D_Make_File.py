
import json
import csv
import datetime
import os


'''


#with open('Data/%s/M0102_search_results.json' % date,  encoding="utf-8-sig") as file3:
    #missing_urls = json.load(file3)
    #file3.close()


#summary_full = summary + summary2
def make(summary_full):

#Generate headings
headings = list(summary_full[0].keys())

with open(f'Data/{date}_{os.environ["linkedin_search_folder_name"]}/M0400_report.csv', 'w', newline='',encoding="utf_8_sig") as file:
    writer = csv.writer(file)
    writer.writerow(headings)

    for each in summary_full:
        writer.writerow(each.values())
    
    #for each in missing_urls:
        #writer.writerow([each])

    file.close

print(f'\nFile generation is complete.\nProfile data ready for Monday upload.\n')
'''