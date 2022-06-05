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
    sleep(2)
    #browser.find_element_by_xpath(
        #"//*[@id='react-root']/section/main/div/div/div/div/button").click()

    # Turn on notifications? Not now
    #browser.implicitly_wait(30)
    #browser.find_element_by_xpath(
        #"/html/body/div[5]/div/div/div/div[3]/button[2]").click()


def automate_instagram(browser):
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
        browser.find_elements(By.CLASS_NAME, '_a6hd')[0].click()

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


        sleep(2)

        sleep(randint(1, 2))

        # Go through x number of photos per hashtag
        for post in range(1, database['number_of_posts']):

            try:
                if database['like'] == True:
                    # Like
                    browser.implicitly_wait(30)
                    browser.find_element_by_xpath(
                        "/html/body/div/div[2]/div/article/div[3]/section[1]/span[1]/button").click()
                    logger.info("Liked")
                    likes += 1

                sleep(randint(2, 4))

                # Comment
                try:
                    browser.implicitly_wait(30)
                    browser.find_element_by_xpath("//form").click()
                    # Random chance of commenting
                    do_i_comment = randint(1, database['chance_to_comment'])
                    if do_i_comment == 1:

                        browser.implicitly_wait(30)
                        comment = browser.find_element_by_xpath("//textarea")

                        sleep(
                            randint(database['wait_to_comment']['min'], database['wait_to_comment']['max']))

                        rand_comment_index = randint(
                            0, len(database['comment_list']))
                        comment.send_keys(
                            database['comment_list'][rand_comment_index])
                        comment.send_keys(Keys.ENTER)
                        logger.info(
                            'Commented ' + database['comment_list'][rand_comment_index])
                        comments += 1
                        sleep(randint(
                            database['wait_between_posts']['min'], database['wait_between_posts']['max']))

                except Exception:
                    # Continue to next post if comments section is limited or turned off
                    pass

            except Exception:
                # Already liked it, continue to next post
                logger.info('Already liked this photo previously')
                pass

            # Go to next post
            browser.implicitly_wait(30)
            browser.find_element_by_link_text('Next').click()
            logger.info('Getting next post')
            sleep(randint(database['wait_between_posts']
                  ['min'], database['wait_between_posts']['max']))

    logger.info(f'Liked {likes} posts')
    logger.info(f'Commented on {comments} posts')

    # Close browser when done
    logger.info('Closing chrome browser...')
    browser.close()


if __name__ == "__main__":
    browser = initialize_browser()
    login_to_instagram(browser)
    sleep(10)
    automate_instagram(browser)
    browser.close()
