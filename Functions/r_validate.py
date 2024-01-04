import glob
import os

import r_main


def verifyURL(url):
    verify_url = input("\nIs this the link you want: Y/N \n" + url + "\n")
    if verify_url.lower() == 'n':
        temp_url = input("\nPlease enter the LinkedIn search URL:\n")
        return verifyURL(temp_url)
    elif verify_url.lower() == 'y':
        return url
    else:
        temp_url = input("\nPlease enter the LinkedIn search URL:\n")
        return verifyURL(temp_url)


def intValidate(x):

    try:
        return int(x)
    except ValueError:
        temp_x = (input("\nPlease only input integers integers, "
                          "please try again, enter the LinkedIn search length:\n"))
        return intValidate(temp_x)


def loadLog():
    if str(input("\nWould you like to resume a previous search using archived logs (Y/N)\n").lower() == 'Y'):
        if str(input("Load archive logs (L) or manually load using PATH (P)\nPlease respond with a 'L' or 'P'").lower() == 'l'):
            print("\n\nLoading archive logs...\n\n")
            print("Found Archived Logs:\n")
            allLogs = (glob.glob("./r_logs/*/*.txt"))
            for i in range(len(allLogs)):
                print(f"{i+1}. {allLogs[i]}\n")
            logSelect = intValidate(input(f"\nPlease input a number between 1 and {len(allLogs)}"))
            loadLogPath = allLogs[logSelect-1]

        elif str(input("\nLoad archive logs (L) or manually load using PATH (P)\nPlease respond with a 'L' or 'P'\n").lower() == 'p'):
            UIPATH = input("Please input the file PATH for the log, you'd like to use")
            loadLogPath = pathValidateLoad(UIPATH)

        else:
            print("Please respond with a valid input and try again")
            return None
        if os.path.exists(loadLogPath):
            loadedLogFile = open(loadLogPath, "r")
            r_main.profile_urls = loadedLogFile.readlines()



    else:
        return False


def pathValidateLoad(path):
    if os.path.exists(path):
        loadedLogFile = open(path)
        loadedLog = loadedLogFile.readlines()
        return loadedLog
    else:
        print("\nThe PATH you entered didn't direct to a file or directory, please try again.")
        return loadLog()

