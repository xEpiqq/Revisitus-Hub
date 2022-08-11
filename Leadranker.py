from oauth2client.service_account import ServiceAccountCredentials
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import customtkinter
import threading
import gspread
import time

def leadRankerMainFunction():
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches",["enable-automation"])
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Leads").sheet1
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    
    def openSites():
        time.sleep(4)
        site_list = sheet.col_values(2)
        site_list_length = len(site_list)
        global x
        for x in range(0, site_list_length):
            try:
                if "http" in site_list[x]:
                    driver.get(site_list[x])
                    time.sleep(3)
            except WebDriverException:
                print("Web driver exception")

    def badButton():
        def logBadToSheets():
            sheet.format(f"B{(x + 1)}", {"backgroundColor": {"red": 0.9568, "green": 0.8, "blue": 0.8}})
        def logMidToSheets():
            sheet.format(f"B{(x + 1)}", {"backgroundColor": {"red": 1, "green": 0.9490, "blue": 0.8}})
        def logGudToSheets():
            sheet.format(f"B{(x + 1)}", {"backgroundColor": {"red": 0.8509, "green": 0.9176, "blue": 0.8274}})
        time.sleep(1)
        customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
        app = customtkinter.CTk()
        app.geometry("600x80")
        app.title("LEAD RANKER")
        frame_1 = customtkinter.CTkFrame(master=app)
        frame_1.pack(pady=20, padx=40, fill="both", expand=True)
        button_bad = customtkinter.CTkButton(master=frame_1, command=logBadToSheets, text="BAD", pady=14, padx=40)
        button_bad.grid(row=1, column=1)
        button_mid = customtkinter.CTkButton(master=frame_1, command=logMidToSheets, text="MID", pady=14, padx=40)
        button_mid.grid(row=1, column=2)
        button_good = customtkinter.CTkButton(master=frame_1, command=logGudToSheets, text="GUD", pady=14, padx=40)
        button_good.grid(row=1, column=3)
        app.mainloop()

    Thread1 = threading.Thread(target=openSites)
    Thread2 = threading.Thread(target=badButton)
    Thread1.start()
    Thread2.start()
    Thread1.join()
    Thread2.join()
