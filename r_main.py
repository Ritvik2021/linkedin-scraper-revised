import csv
import json
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

        # self.initUI()
        self.search_name = "test_v1"
        self.search_url ="https://www.linkedin.com/search/results/people/?geoUrn=%5B%22103644278%22%5D&industry=%5B%221594%22%2C%226%22%2C%224%22%5D&keywords=AI%20computer%20science&network=%5B%22F%22%2C%22S%22%5D&origin=FACETED_SEARCH&schoolFilter=%5B%221792%22%2C%222517%22%2C%221646%22%2C%221503%22%2C%22157343%22%5D&sid=3P~"
        self.search_len = 35
        self.search_user = "Ritvik.2021@gmail.com"
        self.search_pass = "XzY@12Iq9746bwC1"

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

    def saveLogin(self):
        temp_input = input("\nWould you like to save this login info? (y/n)\n")
        if temp_input.lower() == "y":
            with open("logins.txt", "r+") as login_file:
                login_data = json.loads(login_file.read())
                login_data.append([self.search_user, self.search_pass])
                login_file.close()
            with open("logins.txt", "w+") as login_file:
                login_file.write((json.dumps(login_data)))
                login_file.close()

    def loginINIT(self):
        saved_login = input("\nWould you like to use a saved login? [Only one login can be saved at a time] (y/n)\n")
        if saved_login.lower() == "y":
            login_file = open("logins.txt", "r+")
            temp_data = json.loads(login_file.read())
            print("\nWhich Account would you like to use\n")
            for i in range(len(temp_data)):
                print(f"{i + 1}: {temp_data[i][0]}")
            temp_in = 0
            print("\n")
            while temp_in not in list(range(1, len(temp_data) + 1)):
                temp_in = input(f"Please input a number between 1 and {len(temp_data)}\n")
                try:
                    temp_in = int(temp_in)
                except:
                    print("\nPlease only input Integers and try again.")
                else:
                    if temp_in not in list(range(1, len(temp_data) + 1)):
                        print("Please try again.")

            self.search_user = temp_data[temp_in - 1][0]
            self.search_pass = temp_data[temp_in - 1][1]
            login_file.close()
        elif saved_login.lower() == "n":
            self.search_user = input("\nPlease enter the LinkedIn username/email:\n")
            self.search_pass = input("\nPlease enter the LinkedIn passwords:\n")
            self.saveLogin()
        else:
            print("\nPlease try again.")
            self.loginINIT()

    def initUI(self):

        # if not (r_validate.loadLog(self)):
        self.search_url = input("Please enter the LinkedIn search URL:\n")
        self.search_url = r_validate.verifyURL(self.search_url)

        self.search_len = input("\nPlease enter the LinkedIn search length. Recommended length is below 150. \n")
        self.search_len = r_validate.intValidate(self.search_len)
        self.loginINIT()

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
            date_now = str(datetime.strftime(datetime.now(), '%d-%m-%y'))
            with open(f"./Data/{date_now}_{self.search_name}.csv", 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                fields = ["LinkedIn URL", "Full Name", "Distance", "Headline", "First Name", "Last Name", "Location",
                          "Other Locations", "Undergrad", "Other Schools", "Yrs Exp", "Int HS?", "Languages"]
                writer.writerow(fields)
                for i in range(len(cout)):
                    if bout[i]["languages_spoken"] == 'No languages':
                        bout[i]["languages_spoken"] = ""
                #     try:
                #         print(cout[i]["languages"])
                #         print(cout[i]["primaryInstitution"])
                #         print(cout[i]["yearsOfExperience"])
                #         print(cout[i]["internationalSchool"])
                        # print(cout[i]["schoolCountry"])
                        # print(cout[i]["schoolPrimaryCurriculum"])
                        # print(cout[i]["moreDetails"])
                        # print(cout[i]["interestedInMentoring"])
                        # print(cout[i]["location"])
                    # except:
                    #     if not cout[i]["name"]:
                    #         cout[i]["name"] = ''
                    #     elif not cout[i]["languages"]:
                    #         cout[i]["languages"] = ''
                    #     elif not cout[i]["primaryInstitution"]:
                    #         cout[i]["primaryInstitution"] = ''
                    #     elif not cout[i]["yearsOfExperience"]:
                    #         cout[i]["yearsOfExperience"] = ''
                    #     elif not cout[i]["internationalSchool"]:
                    #         cout[i]["internationalSchool"] = ''
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
                            [bout[i]["LinkedIn url"], bout[i]["summary"][0], bout[i]["summary"][2],
                             bout[i]["summary"][1],
                             bout[i]["summary"][0].split(" ")[0], bout[i]["summary"][0].split(" ")[-1],
                             bout[i]["summary"][-1],
                             Utilities.location_strip(bout[i]["work_exp"][3], bout[i]["summary"][-1]),
                             cout[i]["primaryInstitution"],
                             Utilities.location_strip(bout[i]["schools"][0], cout[i]["primaryInstitution"]),
                             cout[i]["yearsOfExperience"], cout[i]["internationalSchool"],
                             ", ".join(repr(e) for e in bout[i]["languages_spoken"])])
                    except:
                        print("DOnes")
                file.close()

            # for each in profiles:
            #     print(each)


runtime = linkedIn_Scraper()
# print(runtime.test())
