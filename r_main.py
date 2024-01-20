import csv
import os
import A_Search as A
import B_Profiles as B
import C_Insights as C
from Functions import Utilities
from Functions import r_validate
from datetime import datetime

class linkedIn_Scraper:

    def __init__(self):
        self.search_name = None
        self.search_url = None
        self.search_len = None
        self.search_user = None
        self.search_pass = None
        self.driver = None
        self.logEntries = None
        self.profile_urls = None
        self.logA = False
        self.logB = False

        if not os.path.exists("r_logs"):
            os.makedirs("r_logs")

        self.driver = Utilities.init_Selenium_driver()

        # self.initUI()
        self.search_name = "test_v1"
        self.search_url = ("https://www.linkedin.com/search/results/people/?geoUrn=%5B%22102299470%22%5D&keywords"
                           "=%224th%20year%22%20medical%20%22international%20baccalaureate%22&origin"
                           "=GLOBAL_SEARCH_HEADER")
        self.search_len = 10
        self.search_user = "Ritvik.2021@gmail.com"
        self.search_pass = "XzY@12Iq9746bwC1"

        if self.logA:
            print(self.profile_urls)
        else:

            if not os.path.exists(f"r_logs/{self.search_name}"):
                os.makedirs(f"r_logs/{self.search_name}")

            self.logEntries = open(f"r_logs/{self.search_name}/logEntries.txt", "w+")
            self.logEntries.write("Timestamp|status\n")

            self.start()

    def initUI(self):

        if not (r_validate.loadLog(self)):
            self.search_url = input("Please enter the LinkedIn search URL:\n")
            self.search_url = r_validate.verifyURL(self.search_url)

            self.search_len = input("\nPlease enter the LinkedIn search length. Recommended length is below 150. \n")
            self.search_len = r_validate.intValidate(self.search_len)

            self.search_user = input("\nPlease enter the LinkedIn username/email:\n")
            self.search_pass = input("\nPlease enter the LinkedIn passwords:\n")
            self.search_name = input(
                "\nFinally, please enter the name of this search, e.g. Italian Universities. This is used for the "
                "folder name.\n")

    def start(self):
        self.profile_urls = A.performSearch(self)
        if self.profile_urls:
            ALog = open(
                f"r_logs/{self.search_name}/{str(datetime.strftime(datetime.now(), '%d-%m-%y'))}_{self.search_name}_ALog.txt",
                "w+")
            ALog.writelines(self.profile_urls)
            self.logEntries.write(f"{str(datetime.now())}|Log excepted successfully\n")
            bout = B.getProfiles(self)
            cout = C.insights(bout)
            with open("./Data/final_v1.csv", 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                fields = ["Name", "Languages", "Primary institution", "Years of experience", "International school?",
                          "School country", "School primary curriculum", "More Details", "Interested in mentoring?",
                          "Location"]
                writer.writerow(fields)
                for each in cout:
                    writer.writerow(
                        [each["name"], each["languages"], each["primaryInstitution"], each["yearsOfExperience"],
                         each["internationalSchool"], each["schoolCountry"], each["schoolPrimaryCurriculum"],
                         each["moreDetails"], each["interestedInMentoring"], each["location"]])
                file.close()


            # for each in profiles:
            #     print(each)


runtime = linkedIn_Scraper()
print(runtime.profile_urls)
