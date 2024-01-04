import os
import A_Search as A
import B_Profiles as B
import C_Insights as C
from Functions import Utilities
from Functions import r_validate
from datetime import datetime


def processing():
    global search_name, search_url, search_len, search_user, search_pass, driver, logEntries, profile_urls
    profile_urls = A.performSearch(search_url, search_len, search_user, search_pass, driver)
    if profile_urls:

        ALog = open(f"r_logs/{search_name}/{str(datetime.strftime(datetime.now(), '%d-%m-%y'))}_{search_name}_ALog","w+")
        ALog.writelines(profile_urls)
        logEntries.write(f"{str(datetime.now())}|Log excepted successfully\n")


def initUI():
    global search_name, search_url, search_len, search_user, search_pass, driver, logEntries, profile_urls

    if not (r_validate.loadLog()):
        search_url = input("Please enter the LinkedIn search URL:\n")
        search_url = r_validate.verifyURL(search_url)

        search_len = input("\nPlease enter the LinkedIn search length. Recommended length is below 150. \n")
        search_len = r_validate.intValidate(search_len)

        search_user = input("\nPlease enter the LinkedIn username/email:\n")
        search_pass = input("\nPlease enter the LinkedIn passwords:\n")
        search_name = input(
            "\nFinally, please enter the name of this search, e.g. Italian Universities. This is used for the folder "
            "name.\n")
    else:
        r_validate.loadLog()


class linkedIn_Scraper:
    global search_name, search_url, search_len, search_user, search_pass, driver, logEntries, profile_urls

    def __init__(self):
        global search_name, search_url, search_len, search_user, search_pass, driver, logEntries, profile_urls

        if not os.path.exists("r_logs"):
            os.makedirs("r_logs")

        driver = Utilities.init_Selenium_driver()

         initUI()

        if not os.path.exists(search_name):
            os.makedirs(search_name)

        logEntries = open(f"r_logs/{search_name}/logEntries.txt", "w+")
        logEntries.write("Timestamp|status\n")

        processing()


runtime = linkedIn_Scraper()
