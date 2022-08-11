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
# ITERATES THROUGH GOOGLE SHEETS
# OPENS WEBSITE AND CRAWLS ITS VARIOUS PAGES
# FIND EMAIL ADDRESSES
# WRITE EMAIL ADDRESSES TO GOOGLE SHEETS

def globalVars():
    global driver, email_regex, chrome_options
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    email_regex = r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

def consoleSetup():
    clear = lambda: os.system('cls')
    clear()
    print("*********************************************")
    print("************LETS GET THOSE EMAILS************")
    print("*********************************************")

def initializeSheets():
    global scope, creds, client, sheet
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Leads").sheet1

def obtainSheetLength():
    global sheetLength
    sheetData = sheet.get_all_records()
    sheetLength = len(sheetData)

def obtainEmails(webAddress, currentIteration):
    try:
        driver.get(webAddress)
        page_source = driver.page_source
        list_of_emails = []
        list_of_emails_string = ""
        for re_match in re.finditer(email_regex, page_source):
            list_of_emails.append(re_match.group() + " ")
        if list_of_emails != []:
            sheet.update_cell(currentIteration + 2, 4, list_of_emails_string.join(list_of_emails))
        else:
            try:
                try:
                    contact_us = driver.find_element(By.PARTIAL_LINK_TEXT, "ontact")
                except NoSuchElementException:
                    contact_us = driver.find_element(By.PARTIAL_LINK_TEXT, "ONTACT")
                ActionChains(driver)\
                    .click(contact_us)\
                    .perform()
                #time.sleep(0.5)
                contact_us_source = driver.page_source
                for re_match in re.finditer(email_regex, contact_us_source):
                    list_of_emails.append(re_match.group() + " ")
                if list_of_emails != []:
                    sheet.update_cell(currentIteration + 2, 4, list_of_emails_string.join(list_of_emails))
            except NoSuchElementException:
                print("NO CONTACT US PAGE")
    except WebDriverException:
        print("Web Driver Exception")
        
def searchSheetData():
    for x in range(sheetLength):
        row = sheet.row_values(x + 2)
        websiteAddress = row[1]
        if "#" in websiteAddress:
            websiteAddress = "https://google.com"
        obtainEmails(websiteAddress, x)

def main():
    globalVars(), consoleSetup(), initializeSheets(), obtainSheetLength(), searchSheetData()

if __name__ == '__main__':
    main()
