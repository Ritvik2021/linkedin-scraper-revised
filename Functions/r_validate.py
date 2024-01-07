import glob
import os



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


def loadLog(scraper):
    if str(input("\nWould you like to resume a previous search using archived logs (Y/N)\n")).lower() == 'y':
        if str(input("Load archive logs (L) or manually load using PATH (P)\nPlease respond with a 'L' or 'P'\n")).lower() == 'l':
            print("\n\nLoading archive logs...\n\n")
            print("Found Search Logs:\n")
            log_directories = [x[0] for x in os.walk("./r_logs/")]
            del log_directories[0]
            for i in range(len(log_directories)):
                print(f"{i+1}. {log_directories[i]}\n")
            dirSelect = intValidate(input(f"\nPlease input a number between 1 and {len(log_directories)}\n"))
            loadDirPath = log_directories[dirSelect-1]

            print(f"\n\nLoading all logs for {loadDirPath}...\n\n")
            allLogs = (glob.glob(f"{loadDirPath}/*.txt"))
            for i in range(len(allLogs)):
                print(f"{i+1}. {allLogs[i]}\n")
            logSelect = intValidate(input(f"\nPlease input a number between 1 and {len(allLogs)}\n"))
            loadLogPath = allLogs[logSelect-1]

        elif str(input("\nLoad archive logs (L) or manually load using PATH (P)\nPlease respond with a 'L' or 'P'\n")).lower() == 'p':
            UIPATH = input("Please input the file PATH for the log, you'd like to use")
            loadLogPath = pathValidateLoad(scraper, UIPATH)

        else:
            print("Please respond with a valid input and try again")
            return None
        if os.path.exists(loadLogPath):
            if "ALog" in loadLogPath:
                print("Log A Detected, Initiating Process B")
                scraper.logA = True
            if "BLog" in loadLogPath:
                print("Log B Detected, Initiating Process C")
                scraper.logB = True
            loadedLogFile = open(loadLogPath, "r")
            scraper.profile_urls = loadedLogFile.readlines()
            return True



    else:
        return False


def pathValidateLoad(scraper, path):
    if os.path.exists(path):
        loadedLogFile = open(path)
        loadedLog = loadedLogFile.readlines()
        return loadedLog
    else:
        print("\nThe PATH you entered didn't direct to a file or directory, please try again.")
        return loadLog(scraper)

