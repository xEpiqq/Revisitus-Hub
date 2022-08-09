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

def leadGenerator(entryBox):
    # GOOGLE SHEETS API SETUP
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Leads").sheet1
    # OPEN DRIVER AND NAVIGATE TO MAPS PAGE
    clear = lambda: os.system('cls')
    clear()
    print("*****************************************************************")
    print("----------------THE ULTIMATE LEAD FINDING MACHINE----------------")
    print("*****************************************************************")
    print("\n")
    whatToSearch = entryBox

    driver = webdriver.Chrome()
    driver.get("https://google.com")
    driver.maximize_window()
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
    #REMOVED BECAUSE SOMETIMES THE MAIN MAP PORTION DOESN'T LOAD AND THE PROGRAM DIES
    ########################################################################################## 
    #wait_again = WebDriverWait(driver, timeout=10, poll_frequency=1)
    #wait_again.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='VIG2qd ApHyTb']")))
    ###########################################################################################
    pages = driver.find_elements(By.XPATH, "//a[@class='fl']")
    pagesNumber = len(pages) + 1
    mapData = []
    #NESTED FOR LOOP THAT GOES THROUGH THE 10 PAGES AND ITERATING OVER THE 20 MAP ELEMENTS
    for n in range(0, pagesNumber):
        time.sleep(4) #Make sure all elements load before mapElements runs again
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
                #update sheets based on info
                mapDataLength = len(mapData)
                newVar = mapData[mapDataLength-1]
                #sheet.update_cell(mapDataLength + 1, 1, newVar[0]) #mapDataLength + 1 so it starts 1 row down
                #sheet.update_cell(mapDataLength + 1, 2, newVar[1]) #to have titles NAME, SITE, NUMBER
                #sheet.update_cell(mapDataLength + 1, 3, newVar[2])
                updateRange = f'A{mapDataLength + 1}:C{mapDataLength + 1}'
                sheet.update(updateRange, [[newVar[0], newVar[1], newVar[2]]])
                #time.sleep(0) # AS TO NOT EXCEED 60 SHEETS REQUESTS PER MINUTE, ALSO 2 AVOID STALEELEMENT EXCEPTION
            except NoSuchElementException:
                print("couldn't find the element")
            except StaleElementReferenceException:
                print("bruh fml")
            except TimeoutException:
                print("timeout exception") # Is this in the right place?
        
        pagination = driver.find_element(By.LINK_TEXT, str(n + 2))
        ActionChains(driver)\
            .click(pagination)\
            .perform()
