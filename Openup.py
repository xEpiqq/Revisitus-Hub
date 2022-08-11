from lib2to3.pgen2 import driver
from selenium.webdriver.chrome.options import Options
import os
import re
import time
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

email = "revisitus.web@gmail.com"
password = "Sugar000!"


def openVoice():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=350,830")
    chrome_options.add_argument("--window-position=0,0")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    global secondDriver
    secondDriver = webdriver.Chrome(options=chrome_options)
    newWait = WebDriverWait(secondDriver, timeout=10, poll_frequency=1)
    voiceWebsite = "https://accounts.google.com/signin/v2/identifier?service=grandcentral&passive=1209600&osid=1&continue=https%3A%2F%2Fvoice.google.com%2Fsignup&followup=https%3A%2F%2Fvoice.google.com%2Fsignup&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
    secondDriver.get(voiceWebsite)
    newEmailField = secondDriver.find_element(By.XPATH, "//input[@type='email']")
    ActionChains(secondDriver)\
        .send_keys_to_element(newEmailField, email)\
        .key_down(Keys.ENTER)\
        .perform()
    newWait = WebDriverWait(secondDriver, timeout=10, poll_frequency=1)
    newWait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    newPasswordField = secondDriver.find_element(By.XPATH, "//input[@type='password']")
    ActionChains(secondDriver)\
        .send_keys_to_element(newPasswordField, password)\
        .key_down(Keys.ENTER)\
        .perform()


def openSheets():
    global driver
    chrome_options_two = Options()
    chrome_options_two.add_argument("--window-size=1040,830")
    chrome_options_two.add_argument("--window-position=502,0")
    driver = webdriver.Chrome(options=chrome_options_two)
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
    sheetsWebsite = "https://docs.google.com/spreadsheets/d/1Q6LpdDR9xhDlxV2b1GrJxSPHWd2OCOqgTRI2gzKIo28/edit#gid=2020274513"
    driver.get(sheetsWebsite)
    emailField = driver.find_element(By.XPATH, "//input[@type='email']")
    ActionChains(driver)\
        .send_keys_to_element(emailField, email)\
        .key_down(Keys.ENTER)\
        .perform()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']")))
    passwordField = driver.find_element(By.XPATH, "//input[@type='password']")
    ActionChains(driver)\
        .send_keys_to_element(passwordField, password)\
        .key_down(Keys.ENTER)\
        .perform()

def main():
    openVoice()
    openSheets()

if __name__ == '__main__':
    main()
