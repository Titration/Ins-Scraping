from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from instascrape import Profile, scrape_posts
import os
import wget
import time
import logging
from urllib.parse import urlparse
from instascrape import Location
from pathlib import Path


URL = 'https://www.instagram.com/explore/tags/XXX'
SESSION_ID = "it can be found when your log in"
USERNAME = "put your Instagram username here"
PASSWORD = "type in the password of your Instagram account"
driver = webdriver.Chrome('./chromedriver')

LINKS = []
SCROLL_PAUSE_TIME = 3
CURRENT_NUMBER_OF_POST = 0;
headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.57",
    "cookie": "sessionid="+SESSION_ID+";"
}
Path("./log").mkdir(parents=True, exist_ok=True)

log_file_name = URL.split('/')[-1:][0] + '.log'
logging.basicConfig(filename = './log/'+log_file_name, level=logging.INFO,
    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

#open the webpage
driver.get("http://www.instagram.com")
#target username
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
#enter username and password
username.clear()
username.send_keys(USERNAME)
password.clear()
password.send_keys(PASSWORD)
#target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
#We are logged in!
#handle NOT NOW
not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

driver.get(URL)
logging.info("Scrape the link: {}".format(URL))
#scroll down to scrape more images
# TOTAL_NUMBER_OF_POST = location.amount_of_posts
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    elements = driver.find_elements_by_xpath("//a[@href]")
    for elem in elements:
        urls = elem.get_attribute("href")
        if "p" in urls.split("/"):
            CURRENT_NUMBER_OF_POST = CURRENT_NUMBER_OF_POST + 1
            print(urls)
            logging.info(urls)
            if (urls not in LINKS):
                LINKS.append(urls)
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print(CURRENT_NUMBER_OF_POST)
print("Total number of Post in location: {}".format(len(LINKS)))
logging.info("Total number of Post in location: {}".format(len(LINKS)))
