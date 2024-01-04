

from calendar import c
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os



#Utilities
def init_Selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    WINDOW_SIZE = "1920,1080"
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--no-sandbox")
    # ser = Service(ChromeDriverManager().install())
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options) 
    return driver


def get_urls(driver, length, max_len,urls):
    # print('Next page')
    collection = urls
    time.sleep(5)
    ## Ask user for lenght
    if length >= max_len:
        # print('LinkedIn profile scraping length reached. Search is done.')
        return collection

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    html = driver.page_source

    soup = BeautifulSoup(html, "html5lib")

    search_results_container = soup.find('div', {'class': 'search-results-container'})

    search_results = search_results_container.find('ul')
   
    results_list = search_results.findChildren('li', recursive=False)
    
    for each in results_list:
        link_to_profile = each.find_all("a", href=True)
        collection.append(link_to_profile[0]['href'])

    # print('Number of profiles scraped: ' + str(len(collection)))
    
    time.sleep(5)

    try:
        # print("Trying to find next button")
        driver.find_element(By.XPATH,"//button[@aria-label='Next']").click()
        # print("Found next button")
        collection = get_urls(driver, len(collection), max_len, collection)
    except Exception as e:
        # print(e)
        # print('No more pages. Search is done')
        return collection
    
    return collection

