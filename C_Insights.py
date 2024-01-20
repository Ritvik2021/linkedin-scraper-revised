

import json
import Functions.Generate_Insights as Insights
import datetime
import os


def insights(linkedIn_profiles):

    final_result = []

    redo_profiles = []

    for profile in linkedIn_profiles:

        if "Error scrapping this profile" in profile:
            redo_profiles.append(profile.split("Error scrapping this profile: ")[1])
            continue

        error_detection1 = profile['schools']

        error_detection2 =  profile['work_exp']

        if isinstance(error_detection1, str) or isinstance(error_detection2, str):

            if error_detection1 == 'No education section' and error_detection2 =='No work experience section':
                redo_profiles.append(profile['LinkedIn url'])
                continue

        a = Insights.primary_institution(profile)

        b = Insights.primary_job(profile)

        if b == 'None':
            b = [0,'None']

        if profile['schools'] == 'No schools':
            additional_info = 'None'
        else:
            additional_info =  profile['schools'][3]

        school_analysis = Insights.school_status(profile)

        insight = {
            'id': profile['Id'],
            'name': profile['summary'][0] + ', ' + profile['summary'][1],
            'languages': profile['languages_spoken'],
            'primaryInstitution': a,
            'yearsOfExperience': Insights.years_of_exp(profile, a, b[1]),
            'internationalSchool': school_analysis['target'],
            'schoolCountry': school_analysis['target_country'],
            'schoolPrimaryCurriculum': school_analysis['target_type'],
            'moreDetails': school_analysis['type'],
            'interestedInMentoring' : profile["potential_mentor"],
            'location': profile['summary'][-1],
            'linkedInUrl': profile["LinkedIn url"],
            'fullInfo': profile
            
        }

        final_result.append(insight)

    with open('./Data/06-01-24_M0101_search_results.json', 'w',
              encoding="utf-8-sig") as file:
        file.write(json.dumps(final_result, ensure_ascii=False))
        file.close()

    print(
        f'\nProfile insight generation procedure done. To continue running the LinkedIn scraper process, please enter \"poetry run python D_Make_File.py\" in the terminal.\nRemember to supply the folder name in the next procedure:\n{os.environ.get("linkedin_search_folder_name")}\n')

    return final_result
 
'''

'''