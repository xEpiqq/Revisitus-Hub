from argparse import Action
from asyncore import write
from doctest import master
from oauth2client.service_account import ServiceAccountCredentials
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import threading
import keyboard
import gspread
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
import win32clipboard
from PIL import Image


def variablesAndSheetsConnect():
    global sheet, chrome_options_dekstop, chrome_options_mobile
    
    #chrome_location = "C:\Program Files\Google\Chrome Beta\Application\chrome.exe"

    chrome_options_dekstop = Options()
    chrome_options_dekstop.add_argument('start-maximized')
    chrome_options_dekstop.add_experimental_option("useAutomationExtension", False)
    chrome_options_dekstop.add_experimental_option("excludeSwitches",["enable-automation"])
    #chrome_options_dekstop.binary_location(chrome_location)

    mobile_emulation = {"deviceName": "iPhone X"}
    chrome_options_mobile = Options()
    chrome_options_mobile.add_argument('start-maximized')
    chrome_options_mobile.add_experimental_option("useAutomationExtension", False)
    chrome_options_mobile.add_experimental_option("excludeSwitches",["enable-automation"])
    chrome_options_mobile.add_experimental_option("mobileEmulation", mobile_emulation)
    #chrome_options_mobile.binary_location(chrome_location)

    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Leads").sheet1

def createEmailList():
    global master_list, master_list_length
    master_list = []
    all_sheet_data = sheet.get_all_records()
    sheet_data_length = len(all_sheet_data)

    for x in range(0, sheet_data_length):
        temp_var = all_sheet_data[x]
        if temp_var["EMAIL"] != "":
            master_list.append([temp_var["SITE"], temp_var["EMAIL"], "", ""])

    master_list_length = len(master_list)

def screenShotters():
    def desktopScreenshotter():
        global desktopDriver
        desktopDriver = webdriver.Chrome(options=chrome_options_dekstop)
        for x in range(0, master_list_length):
            current_biz_site = ((master_list[x])[0])
            current_biz_email = ((master_list[x])[1])
            desktopDriver.get(current_biz_site)
            time.sleep(3)
            desktopDriver.save_screenshot(f'./screenshots/{current_biz_email}_desktop.png')
            (master_list[x])[2] = f"{current_biz_email}_desktop.png"
        desktopDriver.quit()
            
    def mobileScreenshotter():
        mobileDriver = webdriver.Chrome(options=chrome_options_mobile)
        for x in range(0, master_list_length):
            current_biz_site = ((master_list[x])[0])
            current_biz_email = ((master_list[x])[1])
            mobileDriver.get(current_biz_site)
            time.sleep(3)
            mobileDriver.save_screenshot(f'./screenshots/{current_biz_email}_mobile.png')
            (master_list[x])[3] = f"{current_biz_email}_mobile.png"
        mobileDriver.quit()

    Thread1 = threading.Thread(target=desktopScreenshotter)
    Thread2 = threading.Thread(target=mobileScreenshotter)
    Thread1.start()
    Thread2.start()
    Thread1.join()
    Thread2.join()

    json_object = json.dumps(master_list, indent=4)
    with open("./screenshots/screenshotData.json", "w") as outfile:
        outfile.write(json_object)

def signinToGmail():
    global driver
    # Credentials removed for github
    email = ""
    password = ""
    chrome_options_two = Options()
    chrome_options_two.add_argument('start-maximized')
    chrome_options_two.add_experimental_option("useAutomationExtension", False)
    chrome_options_two.add_experimental_option("excludeSwitches",["enable-automation"])
    driver = webdriver.Chrome(options=chrome_options_two)
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
    gmailWebsite = f"https://accounts.google.com/signin/v2/identifier?hl=en&continue=https%3A%2F%2Fmail.google.com&service=mail&ec=GAlAFw&flowName=GlifWebSignIn&flowEntry=AddSession"
    driver.get(gmailWebsite)
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
    wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='T-I T-I-KE L3']")))

def sendEmails():
    align_center_button = "//div[@class='eP aaA aaB']"
    align_left_button = "//div[@class='e4 aaA aaB']"
    email_line_one = "I'll keep it real with you, I own revisitus.com and I am 100% trying to sell you a new website. Gotta be respectful of your time! With THAT said, can I tell you why I think it is legitimately one of the best decisions you can make? I'll keep it brief—50 seconds max—here we go!"
    email_line_two = "You want a landing page that doesn't lose anyone, so we need to optimize this. Your site needs to guarantee action—acting as a personal salesman of sorts. It does well informationally, but time on site is everything in 2022, and people are falling through the cracks (google tracks it, google ranks it). Areas to target: speed, flow, graphic design, blank-space, navigation bar, animation, clear funnel."
    email_line_three = "This is your website on an iphone—or pretty much any phone for that matter. For every 100 people that visit your site roughly 61 will be on their phone. Same changes here but because we design and code from scratch we actually have the capability to change this. We're really a help-you-get-more-customers company, but our method is web design. Thanks for your time. 50 seconds up. Hopefully this didn't sound too sales-man-y, just want to help out,"
    email_line_four = "-- Jayden"
    f = open('./screenshots/screenshotData.json', "r")
    json_data = json.loads(f.read())
    json_data_length = len(json_data)

    for x in range(0, json_data_length):
        recipients = (json_data[x])[1]
        desktop_screenshot = (json_data[x])[2]
        mobile_screenshot = (json_data[x])[3]
        split_string = (json_data[x])[0].split("/")
        remove_www = split_string[2].split("www.")
        for y in range(0, len(remove_www)):
            if len(remove_www[y]) > 3:
                site_name_gutted = remove_www[y]

        def clipboarder(z):
            filepath = f'./screenshots/{z}'
            image = Image.open(filepath)
            output = BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
        
        def alignImage(direction):
            time.sleep(0.1)
            try:
                align_button = driver.find_element(By.XPATH, "//div[@class='aaA aaB e4']")
            except:
                align_button = driver.find_element(By.XPATH, "//div[@class='aaA aaB eP']")
            ActionChains(driver)\
                .click(align_button)\
                .perform()
            time.sleep(0.1)
            align_button_direction = driver.find_element(By.XPATH, direction)
            ActionChains(driver)\
                .click(align_button_direction)\
                .perform()
            time.sleep(0.1)

        def clickComposeButton():
            compose_button = driver.find_element(By.XPATH, "//div[@class='T-I T-I-KE L3']")
            ActionChains(driver)\
                .click(compose_button)\
                .perform()
            wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
            time.sleep(2)

        def recipientsAdder():
            ActionChains(driver)\
                .send_keys(recipients)\
                .key_down(Keys.TAB)\
                .key_down(Keys.TAB)\
                .perform()

        def subjectLine():
            ActionChains(driver)\
                .send_keys(f"hey, I just finished looking over {site_name_gutted}")\
                .key_down(Keys.TAB)\
                .perform()

        def writeEmailBody():
            ActionChains(driver)\
                .send_keys(email_line_one)\
                .key_down(Keys.ENTER)\
                .key_down(Keys.ENTER)\
                .perform()

            alignImage(align_center_button)
            
            clipboarder(desktop_screenshot)
            ActionChains(driver)\
                .key_down(Keys.CONTROL)\
                .send_keys("v")\
                .key_up(Keys.CONTROL)\
                .perform()

            alignImage(align_left_button)

            ActionChains(driver)\
                .key_down(Keys.ENTER)\
                .key_down(Keys.ENTER)\
                .send_keys(email_line_two)\
                .key_down(Keys.ENTER)\
                .key_down(Keys.ENTER)\
                .perform()
            
            alignImage(align_center_button)

            clipboarder(mobile_screenshot)
            ActionChains(driver)\
                .key_down(Keys.CONTROL)\
                .send_keys("v")\
                .key_up(Keys.CONTROL)\
                .perform()

            alignImage(align_left_button)

            ActionChains(driver)\
                .key_down(Keys.ENTER)\
                .send_keys(email_line_three)\
                .key_down(Keys.ENTER)\
                .key_down(Keys.ENTER)\
                .send_keys(email_line_four)\
                .perform()
        
        def sendOnKeypress():
            while True:
                if keyboard.is_pressed('space'):
                    print('You Pressed A Key!')
                    break

        def sendEmail():
            send_button = driver.find_element(By.XPATH, "//div[@class='T-I J-J5-Ji aoO v7 T-I-atl L3']")
            ActionChains(driver)\
                .click(send_button)\
                .perform()
            time.sleep(2)

        clickComposeButton()
        recipientsAdder()
        subjectLine()
        writeEmailBody()
        sendOnKeypress()
        sendEmail()

# variablesAndSheetsConnect()
# createEmailList()
# screenShotters()
# signinToGmail()
# sendEmails()
