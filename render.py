from cmath import log
from time import sleep
import logging
import json
from random import randint
import os
from os.path import exists
import multiprocessing


# Library Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager as CM
import chromedriver_autoinstaller


with open(r".\database.json" , "r") as file:
    database = json.load(file)

#close file
file.close()

numberOfAccounts = len(database['accounts'])
account_info = [database['accounts'][i] + [database['hashtags'][i]] for i in range(numberOfAccounts)]

frame_styles = {"relief": "groove",
                "bd": 3, "bg": "#BEB2A7",
                "fg": "#073bb3", "font": ("Arial", 9, "bold")}

last_info = "Starting up... (logs will be saved to logs.txt)"


logging.basicConfig(
    format='%(levelname)s [%(asctime)s] %(message)s', datefmt='%m/%d/%Y %r', level=logging.INFO)
logger = logging.getLogger()



def printLogtoFile(log, path):
    f = open(path, 'w+')
    f.write(log)
    f.close()


def initialize_browser():

    # Do this so we don't get DevTools and Default Adapter failure
    options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")

    # Initialize chrome driver and set chrome as our browser
    browser = webdriver.Chrome(executable_path=CM().install(), options=options)

    return browser


def login_to_instagram(browser, account):
    browser.get('https://www.instagram.com/')

    sleep(2)

    # Get the login elements and type in your credentials

    browser.implicitly_wait(30)
    username = browser.find_element(By.NAME, 'username')
    username.send_keys(account[0])
    browser.implicitly_wait(30)
    password = browser.find_element(By.NAME, 'password')
    password.send_keys(account[1])
    password.submit()

    sleep(2)
    printLogtoFile("Logged in to account " + account[0] + "\n", r".\logs\log.txt")
    logger.info("Logged in to account " + account[0])


def comment_instagram(browser, hashtag, comment_to_send, post_count):
    # Keep track of how many you like and comment
    likes = 0
    comments = 0

    with open(r".\database.json" , "r") as file:
        database = json.load(file)

    browser.implicitly_wait(30)
    browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
    printLogtoFile(f'Exploring #{hashtag} \n', r".\logs\log.txt")
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
            comment.send_keys(comment_to_send, Keys.ENTER)
            printLogtoFile(f'Commented on post #{post_count} \n', r".\logs\log.txt")
            logger.info(f'Commented on post #{post_count}')
            commented = True
        except WebDriverException:
            printLogtoFile("Could not comment on post\n", r".\logs\log.txt")
            logger.info("Could not comment on post")



def getCommentedPosts(account):
    if exists(account[0]+".txt"):            # if file exists, open it on r+
        file = open(account[0]+".txt","r+")
    else:
        file = open(account[0]+".txt", "w+") # else, create it and open it

    lines = file.readlines()
    return lines



def launch_bot_instance(accountIndex):
    browser = initialize_browser()
    account = database['accounts'][accountIndex]
    hashtag = database['hashtags'][accountIndex]

    print(getCommentedPosts(account))

    login_to_instagram(browser, account)
    sleep(5)
    for post in range(int(database['number_of_comments'])):
        comment = database['comment_list'][randint(0, len(database['comment_list']) - 1)]
        comment_instagram(browser, hashtag, comment, post)
    
    printLogtoFile(f'[INFO]: Finished commenting on {account[0]}', r".\logs\log.txt")
    logger.info(f'[INFO]: Finished commenting on {account[0]}')
    browser.close()


def parentBot(number_of_accounts):
    for i in range(number_of_accounts):
        pid = multiprocessing.Process(target=launch_bot_instance, args=(i,))
        pid.start()