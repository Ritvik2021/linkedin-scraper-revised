import copy
import sys
import time
import datetime
import traceback

from selenium.webdriver.common.by import By
import json
import Functions.Utilities as Utilities
import Functions.Get_Profile as Get
import Functions.Generate_Insights as Insights
import os


def getProfiles(scraper):
    urls = scraper.profile_urls

    linkedIn_profiles = []
    time_taken = []
    old = datetime.datetime.now()
    for counter, each in enumerate(urls):
        if (counter%10 == 0) and (counter != 0):
            print(f"")
            new = datetime.datetime.now()
            time_taken.append((new - old))
            current_avg = sum(time_taken, datetime.timedelta(0)) / len(time_taken)
            print(f"Searching Profiles : ~{round((counter / len(urls)) * 100)}% \t Estimated time remaining: {current_avg * (len(urls) - counter)}")
            old = copy.deepcopy(new)
        try:
            scraper.driver.get(each)

            time.sleep(5)

            html = scraper.driver.page_source
            summary = Get.personal_details(html)
            potential_mentor = Insights.interested_mentoring(html)
            languages_spoken = Get.languages_list(html)
            profile_id = Get.get_id(html)
            schools = Get.education_list(html)
            work_exp = Get.work_exp_list(html)

            profile = {
                'Id': profile_id,
                'summary': summary,
                'potential_mentor': potential_mentor,
                'languages_spoken': languages_spoken,
                'schools': schools,
                'work_exp': work_exp,
                'LinkedIn url': each
            }
            linkedIn_profiles.append(profile)
        except:
            linkedIn_profiles.append('Error scrapping this profile: ' + each)
            print('Error scrapping this profile: ' + each)
            print(traceback.format_exc())
            print("\n\n")
            print(sys.exc_info()[2])
            print("\n\n")
            # print('Error scrapping this profile: ' + each)

        # print('Profile number: ' + str(counter))

    return linkedIn_profiles



def profiles(list_of_profiles, login_user, login_pass):
    driver = Utilities.init_Selenium_driver()
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    driver.find_element(By.ID, 'username').send_keys(login_user)
    driver.find_element(By.ID, 'password').send_keys(login_pass)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(5)

    urls = list_of_profiles

    linkedIn_profiles = []

    for counter, each in enumerate(urls):
        print(f"Searching Profiles : ~{round((counter/len(urls))*100)}%")
        try:
            driver.get(each)

            time.sleep(10)

            html = driver.page_source
            summary = Get.personal_details(html)
            potential_mentor = Insights.interested_mentoring(html)
            languages_spoken = Get.languages_list(html)
            profile_id = Get.get_id(html)

            time.sleep(2)

            schools = Get.education_list(html)

            time.sleep(2)

            work_exp = Get.work_exp_list(html)
            profile = {
                'Id': profile_id,
                'summary': summary,
                'potential_mentor': potential_mentor,
                'languages_spoken': languages_spoken,
                'schools': schools,
                'work_exp': work_exp,
                'LinkedIn url': each
            }
            linkedIn_profiles.append(profile)

            time.sleep(10)
        except:
            linkedIn_profiles.append('Error scrapping this profile: ' + each)
            print('Error scrapping this profile: ' + each)
            print(traceback.format_exc())
            print("\n\n")
            print(sys.exc_info()[2])
            print("\n\n")
        # print('Profile number: ' + str(counter))

    return linkedIn_profiles
