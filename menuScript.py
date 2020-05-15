from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.font import Font
import qrMaker
import jsonOperation
import qrReader
import json
import os
import os.path
from os import path
import openWeb
import gspread
from oauth2client.service_account import ServiceAccountCredentials

settings = {}
jsonPath = path.join(qrMaker.getCurrentPath(), "config\\settings.json")
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"] #only used for testing
def openPreferences():

    def testSheet():
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(jsonOperation.readFromJson('credentialsJsonEntry', jsonPath),scope)
            try:
                client = gspread.authorize(creds)
                sheet = client.open("spoolData").sheet1
                try:
                    openWeb.openChrome(sheetEntry.get())
                    statusText['text'] = "All tests successful"
                except:
                    statusText['text'] = "Unable to open sheet"

            except:
                statusText['text'] = "Unable to authorize"

        except:
            statusText['text'] = 'Invalid credentials file'


    def updateJson():
        try:
            for k, l in zip(entryNames, entry):
                if k == 'qrModeValue':
                    mode = QRMode.get()
                    settings[k]=mode
                elif l:
                    value = str(l.get())
                    settings[k]=value
            jsonOperation.writeToJson(settings, jsonPath)
            statusText['text'] = 'Sucessfully updated status file'
        except:
            statusText['text'] = 'Unable to write to/create settings file'
    preferences = Tk()
    QRMode=IntVar(master=preferences)

    def getFilePath():
        filepath = filedialog.askopenfilename(initialdir =  qrMaker.getCurrentPath(), title = "Select Credentials File", filetypes=[("Json", '*.json'), ("All Fucken Files", "*.*")]) 
        return str(filepath)
    
    def loadSettings():
        try:
            if path.exists(jsonPath) != True:
                statusText['text'] = "Save some new settings first"
            else:
                for y, z in zip(entryNames, entry):
                    if y == "qrModeValue":
                        data = jsonOperation.readFromJson(y, jsonPath)
                        if data != None:
                            if data == 0:
                                qrModeEntry0.invoke()
                            elif data == 1:
                                qrModeEntry1.invoke()
                    elif z:
                        z.delete(0, "end")
                        data = jsonOperation.readFromJson(y, jsonPath)
                        if data:
                            z.insert(0, str(data))
                    statusText['text'] = "Successfully loaded settings file"
        except:
            statusText['text'] = 'Unable to load settings'

    def loadCreds():
        data = getFilePath()
        if data:
            credentialsJsonEntry.delete(0, "end")
            credentialsJsonEntry.insert(0, data)
    
    def changeQRMode():
        mode = QRMode.get()
        if mode == 0:
            qrHeightEntry['state']='disabled'
        elif mode == 1:
            qrHeightEntry['state']='enabled'




    preferences.title("Preferences")
    preferences.iconbitmap(qrMaker.getCurrentPath()+'icon.ico')
    preferences.geometry('500x600')

    topText = Label(preferences, width=20, text="Edit Preferences", font=("Enter Sansman Bold", 10))

    cameraText = Label(preferences, width=25, text="Select Camera Instance:")
    cameraEntry = Combobox(preferences, width=10, values=qrReader.getCameras())

    printerText = Label(preferences, width=25, text="Printer list(x, y, z...)")
    printerEntry = Entry(preferences, width=20)

    materialText = Label(preferences, width=25, text="Material list(x, y, z...)")
    materialEntry = Entry(preferences, width=20)

    qrWidthText = Label(preferences, width=25, text="QR Output Width (in.)")
    qrWidthEntry = Entry(preferences, width=10)

    qrHeightText = Label(preferences, width=25, text="QR Output Height (in.)")
    qrHeightEntry = Entry(preferences, width=10)

    qrModeText = Label(preferences, width=25, text="QR Output Mode")
    qrModeEntry0 = Radiobutton(preferences, text="Text beneath QR code", variable = QRMode, value = 0, command = changeQRMode)
    qrModeEntry1 = Radiobutton(preferences, text="Text right of QR code", variable = QRMode, value = 1, command = changeQRMode)

    settingsJsonText = Label(preferences, width=25, text="Load from settings")
    loadSettingsButton = Button(preferences, width=12, text="Load Settings", command=loadSettings)

    credentialsJsonText = Label(preferences, width=25, text="Path to Credentials file")
    credentialsJsonEntry = Entry(preferences, width=30)
    credentialsJsonButton = Button(preferences, width=7, text="Browse", command=loadCreds)

    sheetText = Label(preferences, width=25, text="Google Sheets Link")
    sheetEntry = Entry(preferences, width=30)
    sheetTest = Button(preferences, width=18, text="Test Auth and Link", command=testSheet)
    text = [cameraText, printerText, materialText, qrWidthText, qrHeightText, qrModeText, settingsJsonText, credentialsJsonText, sheetText]
    entry = [cameraEntry, printerEntry, materialEntry, qrWidthEntry, qrHeightEntry, False, False, credentialsJsonEntry, sheetEntry]
    entryNames = ['cameraEntry', 'printerEntry', 'materialEntry', 'qrWidthEntry', 'qrHeightEntry', 'qrModeValue', False, 'credentialsJsonEntry', 'sheetEntry']

    updateJsonButton = Button(preferences, text="Save Preferences", command=updateJson)

    statusText = Label(preferences, width=30)


    for i in range(1, 100, 2):
        preferences.grid_rowconfigure(i, minsize=10)

    topText.grid(column = 1, row = 0)
    row=2
    for i, j in zip(text, entry):
        if i:
            i.grid(sticky='w', column = 0, row = row)
        if j:
            j.grid(sticky='w', column = 1, row = row)
        row+=2
    updateJsonButton.grid(sticky='w',  column=1, row=row+4)
    credentialsJsonButton.grid(sticky='w',  column=2, row=row-4)
    loadSettingsButton.grid(sticky='w',  column=1, row=row-6)
    statusText.grid(sticky='w',  column=1, row=row+6)
    sheetTest.grid(sticky='w',  column=2, row=row-2)
    qrModeEntry0.grid(sticky='w',  column=1, row=row-8)
    qrModeEntry1.grid(sticky='w',  column=2, row=row-8)
    qrModeEntry1.invoke()

    if path.exists(jsonPath):
        loadSettings()

    preferences.mainloop()
    preferences.quit()
