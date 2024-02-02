import sys
import os
import time
from selenium.webdriver.common.by import By
import json
import Functions.Utilities as Utilities
from bs4 import BeautifulSoup

'''
login_user =  'g.iademarco@yahoo.it' or "jenna.ahn71@gmail.com"
login_pass = 'Millie2020' or "Millie2022!"
sample search: https://www.linkedin.com/search/results/people/?keywords=%22undergraduate%20student%20at%20university%20of%20British%20Columbia%22%20%22international%22&origin=GLOBAL_SEARCH_HEADER&sid=2cf
'''


def login(scraper):
    print("init successful")

    scraper.driver.get("https://www.linkedin.com/login")
    time.sleep(1)

    scraper.driver.find_element(By.NAME, 'session_key').send_keys(scraper.search_user)
    scraper.driver.find_element(By.NAME, 'session_password').send_keys(scraper.search_pass)
    scraper.driver.find_element(By.XPATH, "//button[@class='btn__primary--large from__button--floating']").click()

    print("Attempting log in. Checking if verification code is necessary.")

    time.sleep(
        15)  # Must wait for a CAPTCHA page to load. This takes a while, ie. more than 5 seconds. But it cannot be too long otherwise linkedin will direct the browser back to the standard login page.

    search_page: str = scraper.driver.find_element(By.XPATH, "//html").get_attribute('outerHTML')
    soup = BeautifulSoup(search_page, "html5lib")
    title = str(soup.find('title'))
    input_exist = soup.find('input', {'class': 'form__input--text input_verification_pin'})
    captcha_exist = soup.find('form', {'id': 'captcha-challenge'})

    time.sleep(10)
    if 'Verification' in title and input_exist and not captcha_exist:
        print('AWAIT_PIN')
        for _ in range(5):
            inp = input()
            if inp.startswith("RESEND_PIN"):
                pass
            elif inp.startswith("SUBMIT_PIN"):
                verification_code = inp[len("SUBMIT_PIN") + 1:]
                scraper.driver.find_element(By.ID, 'input__email_verification_pin').send_keys(verification_code)
                scraper.driver.find_element(By.ID, 'email-pin-submit-button').click()
                time.sleep(15)
            else:
                raise Exception("Incorrect stdin format")
        else:
            raise Exception("Too many email resends")
    elif 'Verification' in title and captcha_exist and not input_exist:
        raise Exception("CAPTCHA detected")

    print('LOGGED_IN')


def search(search_url, linkedin_length, login_user, login_pass, driver):
    print("init successful")

    driver.get("https://www.linkedin.com/login")
    time.sleep(5)

    driver.find_element(By.NAME, 'session_key').send_keys(login_user)
    driver.find_element(By.NAME, 'session_password').send_keys(login_pass)
    driver.find_element(By.XPATH, "//button[@class='btn__primary--large from__button--floating']").click()

    print("Attempting log in. Checking if verification code is necessary.")

    time.sleep(
        5)  # Must wait for a CAPTCHA page to load. This takes a while, ie. more than 5 seconds. But it cannot be too long otherwise linkedin will direct the browser back to the standard login page.

    search_page: str = driver.find_element(By.XPATH, "//html").get_attribute('outerHTML')
    soup = BeautifulSoup(search_page, "html5lib")
    title = str(soup.find('title'))
    input_exist = soup.find('input', {'class': 'form__input--text input_verification_pin'})
    captcha_exist = soup.find('form', {'id': 'captcha-challenge'})

    if 'Verification' in title and input_exist and not captcha_exist:
        print('AWAIT_PIN')
        for _ in range(5):
            inp = input()
            if inp.startswith("RESEND_PIN"):
                pass
            elif inp.startswith("SUBMIT_PIN"):
                verification_code = inp[len("SUBMIT_PIN") + 1:]
                driver.find_element(By.ID, 'input__email_verification_pin').send_keys(verification_code)
                driver.find_element(By.ID, 'email-pin-submit-button').click()
                time.sleep(15)
            else:
                raise Exception("Incorrect stdin format")
        else:
            raise Exception("Too many email resends")
    elif 'Verification' in title and captcha_exist and not input_exist:
        raise Exception("CAPTCHA detected")

    print('LOGGED_IN')

    print('You have successfully logged in. Searching the provided link.')
    driver.get(search_url)
    time.sleep(5)

    search_page: str = driver.find_element(By.XPATH, "//html").get_attribute('outerHTML')

    # print(search_page)

    html = BeautifulSoup(search_page, "html5lib")

    search_results = html.find('div', {'class': 'search-results-container'})

    if "No results found" in search_results.text:
        sys.exit("No results found")
    else:
        # print('Search results found. Scrapping links.')
        urls = Utilities.get_urls(driver, 0, linkedin_length)

    urls = list(set(urls))

    print(urls)
    return urls


# search("https://www.linkedin.com/search/results/people/?keywords=tutor&origin=SWITCH_SEARCH_VERTICAL&sid=YYr", 10,
#        "ritvik.2021@gmail.com", "XzY@12Iq9746bwC1")

def performSearch(scraper):
    try:
        return search(scraper.search_url, scraper.search_len, scraper.search_user, scraper.search_pass, scraper.driver)
    except:
        tempInput = input(
            "Step A: Unsuccessful Search, would you like to try again? (Y-yes, N-no, x-change parameters)")
        if tempInput.lower() == 'y':
            return performSearch(scraper)
        elif tempInput.lower() == 'n':
            return None
        elif tempInput.lower() == 'x':
            scraper.initUI()
            performSearch(scraper)
        else:
            return None
