from argparse import Action
import os
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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

def sheetsApi():
    global scope, creds, client, sheet
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Leads").sheet1

def navigateToListings(entryBox):
    global driver, wait
    whatToSearch = entryBox
    driver = webdriver.Chrome()
    driver.get("https://google.com")
    searchBar = driver.find_element(By.XPATH, "//input[@class='gLFyf gsfi']")
    ActionChains(driver)\
        .send_keys_to_element(searchBar, whatToSearch)\
        .key_down(Keys.ENTER)\
        .perform()
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='MXl0lf tKtwEb wHYlTd']")))
    morePlaces = driver.find_element(By.XPATH, "//div[@class='MXl0lf tKtwEb wHYlTd']")
    ActionChains(driver)\
        .click(morePlaces)\
        .perform()

def pageCounter():
    # time.sleep might be a lil unreliable for page loading
    time.sleep(3)
    pages = driver.find_elements(By.XPATH, "//a[@class='fl']")
    pages_num = len(pages) - 1
    ActionChains(driver)\
        .click(pages[pages_num])\
        .perform()
    time.sleep(3)
    new_pages = driver.find_elements(By.XPATH, "//a[@class='fl']")
    new_pages_length = len(new_pages) - 1
    final_element_number = int(new_pages[new_pages_length].text)
    
    if final_element_number <= 10:
        page_one = driver.find_element(By.LINK_TEXT, "1")
        ActionChains(driver)\
            .click(page_one)\
            .perform()
        scrapeCity((pages_num + 2))
    else:
        ActionChains(driver)\
            .click(new_pages[0])\
            .perform()
        time.sleep(3)
        page_zero = driver.find_elements(By.XPATH, "//a[@class='fl']")
        ActionChains(driver)\
            .click(page_zero[0])\
            .perform()
        scrapeCity(final_element_number)

def scrapeCity(final_element_number): 
    mapData = []
    for n in range(0, final_element_number):
        time.sleep(4)
        mapLength = len(driver.find_elements(By.XPATH, "//span[@class='OSrXXb']"))
        mapElements = driver.find_elements(By.XPATH, "//span[@class='OSrXXb']")
        for x in range(0, mapLength):
            ActionChains(driver)\
                .click(mapElements[x])\
                .perform()
            try:
                waiter = WebDriverWait(driver, timeout=10, poll_frequency=1)
                waiter.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='ab_button CL9Uqc']")))
                websiteElem = driver.find_element(By.XPATH, "//a[@class='ab_button CL9Uqc']")
                websiteUrl = websiteElem.get_dom_attribute("href")
                phoneElem = driver.find_elements(By.XPATH, "//div[@class='zloOqf PZPZlf']")
                phoneElemLen = len(phoneElem)
                bizName = mapElements[(x-1)].text
                phoneNum = phoneElem[(phoneElemLen - 1)].text.strip("Phone :")
                mapData.append((bizName, websiteUrl, phoneNum))
                mapDataLength = len(mapData)
                newVar = mapData[mapDataLength-1]
                updateRange = f'A{mapDataLength + 1}:C{mapDataLength + 1}'
                sheet.update(updateRange, [[newVar[0], newVar[1], newVar[2]]])
            except NoSuchElementException:
                print("couldn't find the element")
            except StaleElementReferenceException:
                print("bruh fml")
            except TimeoutException:
                print("timeout exception")
        # Lowkey masking the real bug with this try:except, program tries to paginate 1 page above index
        # e.g. FINAL PAGE: 10, Tries to find PAGE 11, but crashes
        try:
            pagination = driver.find_element(By.LINK_TEXT, str(n + 2))
            ActionChains(driver)\
                .click(pagination)\
                .perform()
        except NoSuchElementException:
            driver.quit()

def clearFakePhoneNumbers():
    values_list = sheet.col_values(3)
    values_list_length = len(values_list)
    for x in range(0, values_list_length):
        if len(values_list[x]) > 15 or values_list[x] == "Address":
            sheet.update_cell((x + 1), 3, "(801) 000-0000")
