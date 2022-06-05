from time import sleep
import logging
import sys
import json
from random import randint

# Library Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager as CM
from tkinter import *
from tkinter.scrolledtext import ScrolledText


logging.basicConfig(
    format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()

# GUI


def insert_entry(container, string_to_i, row, column):
    entry_widget = Entry(container)
    entry_widget.insert("end", string_to_i)
    entry_widget.grid(row=row, column=column)
    return entry_widget


def initialize_browser():

    # Do this so we don't get DevTools and Default Adapter failure
    options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")

    # Initialize chrome driver and set chrome as our browser
    browser = webdriver.Chrome(executable_path=CM().install(), options=options)

    return browser


def login_to_instagram(browser):
    browser.get('https://www.instagram.com/')

    sleep(2)

    # Get the login elements and type in your credentials
    with open("data/database.json", "r") as file:
        database = json.load(file)

    browser.implicitly_wait(30)
    username = browser.find_element_by_name('username')
    username.send_keys(database['credentials']['username'])
    browser.implicitly_wait(30)
    password = browser.find_element_by_name('password')
    password.send_keys(database['credentials']['password'])

    sleep(2)

    # Click the login button
    browser.implicitly_wait(30)
    browser.find_element(By.CLASS_NAME, 'HoLwm').click()

    sleep(2)

    browser.implicitly_wait(30)
    browser.find_element(By.XPATH, "//*[@id='loginForm']/div/div[3]/button").click()


    browser.implicitly_wait(30)

    logger.info('Logged in to ' + database['credentials']['username'])



    # Save your login info? Not now
    #browser.find_element_by_xpath(
        #"//*[@id='react-root']/section/main/div/div/div/div/button").click()

    # Turn on notifications? Not now
    #browser.implicitly_wait(30)
    #browser.find_element_by_xpath(
        #"/html/body/div[5]/div/div/div/div[3]/button[2]").click()


def automate_instagram(browser, post_count):
    # Keep track of how many you like and comment
    likes = 0
    comments = 0

    with open("data/database.json", "r") as file:
        database = json.load(file)

    for hashtag in database['hashtags']:
        browser.implicitly_wait(30)
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        logger.info(f'Exploring #{hashtag}')
        sleep(randint(1, 2))

        # Click first thumbnail to open
        browser.implicitly_wait(30)
        browser.find_elements(By.CLASS_NAME, '_a6hd')[post_count].click()

        sleep(2)
        commented = False
        while not commented:
            try:
                comment = browser.find_element(By.CLASS_NAME, '_aaoc')
                comment.send_keys(database['comment_list'][0], Keys.ENTER)
                logger.info("Commented on a post")
                commented = True
            except WebDriverException:
                logger.info('Could not comment')




if __name__ == "__main__":
    browser = initialize_browser()
    login_to_instagram(browser)
    sleep(5)
    for i in range(2):
        automate_instagram(browser, i)
    browser.close()
