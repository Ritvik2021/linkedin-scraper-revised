
import sys
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json
import Functions.Utilities as Utilities
from bs4 import BeautifulSoup
import Functions.Get_Profile as Get
import Functions.Generate_Insights as Insights


date = str(datetime.date.today())

with open('Data/%s/M0101_search_results.json' % date) as file:
    urls = json.load(file)

if len(urls) == 0:
    sys.exit('Urls have all been scrapped.')



#with open('urls.json', 'r') as f:
#  urls = json.loads(str(f))

#login_user = "jenna.ahn71@gmail.com"
#login_pass = "Millie2020!"

login_user =  'g.iademarco@yahoo.it'
login_pass = 'Millie2020'

main_url = "https://www.linkedin.com/login"
#path = r"C:\Users\Aaron_Admin\Downloads\chromedriver.exe"
path= '/Users/aaron_admin/Downloads/chromedriver'
driver = Utilities.init_Selenium_driver()
driver.get(main_url)
time.sleep(2)


driver.find_element(By.ID,'username').send_keys(login_user)
driver.find_element(By.ID,'password').send_keys(login_pass)
driver.find_element(By.XPATH,"//button[@type='submit']").click()


time.sleep(10)


linkedIn_profiles = []

print('Starting procedure')
for counter,each in enumerate(urls):

    try:
        
        driver.get(each)

        time.sleep(10)

        html = driver.page_source

        summary =  Get.personal_details(html)

        potential_mentor =  Insights.interested_mentoring(html)

        languages_spoken = Get.languages_list(html)

        time.sleep(2)
        
        schools = Get.education_list(html)

        time.sleep(2)

        work_exp = Get.work_exp_list(html)
        
        profile = {

            'summary':  summary,
            'potential_mentor': potential_mentor,
            'languages_spoken': languages_spoken,
            'schools': schools,
            'work_exp':  work_exp,
            'LinkedIn url': each
        }

        linkedIn_profiles.append(profile)

        time.sleep(10)
    except:
        linkedIn_profiles.append('Error scrapping this profile: ' + each)
        print('Error scrapping this profile: ' + each)
    
    print(counter)


with open('Data/%s/M0201_profile_summaries.json' % date, 'w', encoding="utf-8-sig") as file:
    file.write(json.dumps(linkedIn_profiles, ensure_ascii=False))

sys.exit('Finished scrapping profiles')








