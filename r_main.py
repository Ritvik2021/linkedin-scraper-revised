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
        # self.logA = False
        # self.logB = False

        if not os.path.exists("r_logs"):
            os.makedirs("r_logs")

        self.driver = Utilities.init_Selenium_driver()

        self.initUI()
        # self.search_name = "test_v1"
        # self.search_url = ("https://www.linkedin.com/search/results/people/?keywords=game%20design%2C%20%27%27international%20Baccalaureate%27%27&origin=FACETED_SEARCH&sid=2z0")
        # self.search_len = 10
        # self.search_user = "Ritvik.2021@gmail.com"
        # self.search_pass = "XzY@12Iq9746bwC1"

        # if self.logA:
        #     print(self.profile_urls)
        # else:
        #
        #     if not os.path.exists(f"r_logs/{self.search_name}"):
        #         os.makedirs(f"r_logs/{self.search_name}")
        #
        #     self.logEntries = open(f"r_logs/{self.search_name}/logEntries.txt", "w+")
        #     self.logEntries.write("Timestamp|status\n")
        #
        self.start()

    def initUI(self):

        # if not (r_validate.loadLog(self)):
        self.search_url = input("Please enter the LinkedIn search URL:\n")
        self.search_url = r_validate.verifyURL(self.search_url)

        self.search_len = input("\nPlease enter the LinkedIn search length. Recommended length is below 150. \n")
        self.search_len = r_validate.intValidate(self.search_len)

        self.search_user = input("\nPlease enter the LinkedIn username/email:\n")
        self.search_pass = input("\nPlease enter the LinkedIn passwords:\n")
        self.search_name = input(
            "\nFinally, please enter the name of this search, e.g. Italian Universities. This is used for the "
            "file name, therefore any existing file with the same name will be overwritten.\n")

    def test(self):
        A.login(self)
        while True:
            c_url = input("URL : ")
            self.profile_urls = [c_url]
            bout = B.getProfiles(self)
            cout = C.insights(bout)

            print(bout)
            print("\n\n")
            print(cout)

    def start(self):
        self.profile_urls = A.performSearch(self)
        if self.profile_urls:
            # ALog = open(
            #     f"r_logs/{self.search_name}/{str(datetime.strftime(datetime.now(), '%d-%m-%y'))}_{self.search_name}_ALog.txt",
            #     "w+")
            # ALog.writelines(self.profile_urls)
            # self.logEntries.write(f"{str(datetime.now())}|Log excepted successfully\n")
            bout = B.getProfiles(self)
            print(bout)
            print("\n")
            cout = C.insights(bout)
            print(cout)
            print("\n")
            with open("./Data/final_v1.csv", 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                fields = ["LinkedIn URL", "Full Name", "Distance", "Headline", "First Name", "Last Name", "Location",
                          "Other Locations", "Undergrad", "Other Schools", "Yrs Exp", "Int HS?", "Languages"]
                writer.writerow(fields)
                for i in range(len(cout)):
                    try:
                        print(cout[i]["languages"])
                        print(cout[i]["primaryInstitution"])
                        print(cout[i]["yearsOfExperience"])
                        print(cout[i]["internationalSchool"])
                        # print(cout[i]["schoolCountry"])
                        # print(cout[i]["schoolPrimaryCurriculum"])
                        # print(cout[i]["moreDetails"])
                        # print(cout[i]["interestedInMentoring"])
                        # print(cout[i]["location"])
                    except:
                        if not cout[i]["name"]:
                            cout[i]["name"] = ''
                        elif not cout[i]["languages"]:
                            cout[i]["languages"] = ''
                        elif not cout[i]["primaryInstitution"]:
                            cout[i]["primaryInstitution"] = ''
                        elif not cout[i]["yearsOfExperience"]:
                            cout[i]["yearsOfExperience"] = ''
                        elif not cout[i]["internationalSchool"]:
                            cout[i]["internationalSchool"] = ''
                        # elif not cout[i]["schoolCountry"]:
                        #     cout[i]["schoolCountry"] = ''
                        # elif not cout[i][["schoolPrimaryCurriculum"]]:
                        #     cout[i][["schoolPrimaryCurriculum"]] = ''
                        # elif not cout[i]["moreDetails"]:
                        #     cout[i]["moreDetails"] = ''
                        # elif not cout[i]["interestedInMentoring"]:
                        #     cout[i]["interestedInMentoring"] = ''
                        # elif not cout[i]["location"]:
                        #     cout[i]["location"] = ''

                    # ["LinkedIn URL","Full Name","Distance","Headline","First Name","Last Name","Location",
                    # "Other Locations","Undergrad","Other Schools","Yrs Exp","Int HS?","Languages"]

                    # print([bout[i]["LinkedIn url"]
                    #           , bout[i]["summary"][0]
                    #           , bout[i]["summary"][2]
                    #           , bout[i]["summary"][1]
                    #           , bout[i]["summary"][0].split(" ")[0]
                    #           , bout[i]["summary"][0].split(" ")[-1]
                    #           , bout[i]["summary"][-1]
                    #           , Utilities.location_strip(bout[i]["work_exp"][3],bout[i]["summary"][-1])
                    #           , cout[i]["primaryInstitution"]
                    #           , Utilities.location_strip(bout[i]["schools"][0],cout[i]["primaryInstitution"])
                    #           , cout[i]["yearsOfExperience"],cout[i]["internationalSchool"]
                    #           , bout[i]["languages_spoken"]])
                    try:
                        writer.writerow(
                            [bout[i]["LinkedIn url"], bout[i]["summary"][0], bout[i]["summary"][2], bout[i]["summary"][1],
                             bout[i]["summary"][0].split(" ")[0], bout[i]["summary"][0].split(" ")[-1],bout[i]["summary"][-1],
                             Utilities.location_strip(bout[i]["work_exp"][3],bout[i]["summary"][-1]), cout[i]["primaryInstitution"], Utilities.location_strip(bout[i]["schools"][0],cout[i]["primaryInstitution"]), cout[i]["yearsOfExperience"],cout[i]["internationalSchool"],
                             ", ".join( repr(e) for e in bout[i]["languages_spoken"] )])
                    except:
                        print("DOnes")
                file.close()

            # for each in profiles:
            #     print(each)


runtime = linkedIn_Scraper()
# print(runtime.test())
