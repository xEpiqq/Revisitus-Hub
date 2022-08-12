import tkinter
import customtkinter
import Leadgen
import Openup
import Emailfinder
import Leadranker
import Emailgen

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x520")
app.title("REVISITUS HUB")

def launchDefault():
    Openup.openVoice()
    Openup.openSheets()

def launchLeadgen():
    Leadgen.sheetsApi()
    Leadgen.navigateToListings(entry_1.get())
    Leadgen.pageCounter()
    Leadgen.clearFakePhoneNumbers()

def launchFindEmails():
    Emailfinder.main()
    
def launchLeadRanker():
    Leadranker.leadRankerMainFunction()

def launchScreenshotter():
    Emailgen.variablesAndSheetsConnect()
    Emailgen.createEmailList()
    Emailgen.screenShotters()

def launchGenEmails():
    Emailgen.signinToGmail()
    Emailgen.sendEmails()

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT, text="REVISITUS HUB")
label_1.pack(pady=12, padx=10)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="      BIZ + LOCATION")
entry_1.pack(pady=12, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=launchLeadgen, text="FIND LEADS")
button_1.pack(pady=12, padx=10)

button_5 = customtkinter.CTkButton(master=frame_1, command=launchLeadRanker, text="RANK LEADS")
button_5.pack(pady=12, padx=10)

button_2 = customtkinter.CTkButton(master=frame_1, command=launchFindEmails, text="FIND EMAILS")
button_2.pack(pady=12, padx=10)

button_4 = customtkinter.CTkButton(master=frame_1, command=launchScreenshotter, text="SCREENSHOT")
button_4.pack(pady=12, padx=10)

button_3 = customtkinter.CTkButton(master=frame_1, command=launchGenEmails, text="GEN EMAILS")
button_3.pack(pady=12, padx=10)

button_0 = customtkinter.CTkButton(master=frame_1, command=launchDefault, text="START GRIND")
button_0.pack(pady=12, padx=10)

switch_1 = customtkinter.CTkSwitch(master=frame_1, text="Theme: Dark")
switch_1.pack(pady=12, padx=10)

app.mainloop()
