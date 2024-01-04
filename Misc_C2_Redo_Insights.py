

import json
import Functions.Generate_Insights as Insights
import datetime


date = str(datetime.date.today())

with open('Data/%s/M0201_profile_summaries.json' % date,  encoding="utf-8-sig") as file:
    linkedIn_profiles = json.load(file)

final_result = []

redo_profiles = []

for profile in linkedIn_profiles:

    try:
        error_detection = profile['schools'] + ' ' + profile['work_exp']


    except:
        error_detection = 'None'
        pass

    if 'Error scrapping' in error_detection:
        redo_profiles.append(profile['LinkedIn url'])
        continue


    a = Insights.primary_institution(profile)

    b = Insights.primary_job(profile)


    if profile['schools'] == 'No schools':
        additional_info = 'None'
    else:
        additional_info =  profile['schools'][3]

    school_analysis = Insights.school_status(profile)

    insight = {
        
        'Name': profile['summary'][0] + ', ' + profile['summary'][1],
        'Languages': profile['languages_spoken'],
        'Primary institution': a,
        'Years of experience': Insights.years_of_exp(profile, a, b[1]),
        'International school?': school_analysis['target'],
        'School country': school_analysis['target_country'],
        'School primary curriculum': school_analysis['target_type'],
        'More Details': school_analysis['type'],
        'Interested in mentoring?' : profile["potential_mentor"],
        'Location': profile['summary'][-1],
        'LinkedIn url': profile["LinkedIn url"],
        'Full info': profile
        

    }

    final_result.append(insight)




with open('Data/%s/M0301_profile_insights.json' % date, 'w', encoding="utf-8-sig") as file:
    file.write(json.dumps(final_result, ensure_ascii=False))
    file.close()


with open('Data/%s/M0102_search_results.json' % date, 'w', encoding="utf-8-sig") as file:
    file.write(json.dumps(redo_profiles, ensure_ascii=False))
    file.close()