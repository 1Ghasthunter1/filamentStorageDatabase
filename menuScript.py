from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
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
                    openWeb.openChrome(jsonOperation.readFromJson('sheetEntry', jsonPath))
                    statusText['text'] = "All tests successful"
                except:
                    statusText['text'] = "Unable to open sheet"

            except:
                statusText['text'] = "Unable to authorize"

        except:
            statusText['text'] = 'Invalid credentials file'


    def updateJson():
        #try:
        for k, l in zip(entryNames, entry):
            if l:
                value = str(l.get())
                settings[k]=value
        jsonOperation.writeToJson(settings, jsonPath)
        statusText['text'] = 'Sucessfully updated status file'
        #except:
            #statusText['text'] = 'Unable to write to/create settings file'
    preferences = Tk()

    def getFilePath():
        filepath = filedialog.askopenfilename(initialdir =  qrMaker.getCurrentPath(), title = "Select A File", filetypes=[("Json", '*.json'), ("All Fucken Files", "*.*")]) 
        return str(filepath)
    
    def loadSettings():
        try:
            if path.exists(jsonPath) != True:
                statusText['text'] = "Save some new settings first"
            else:
                for y, z in zip(entryNames, entry):
                    if z:
                        z.delete(0, "end")
                        data = jsonOperation.readFromJson(y, jsonPath)
                        if data:
                            z.insert(0, str(data))
                        statusText['text'] = "Successfully loaded settings file"
        except:
            statusText['text'] = 'Unable to load settings'

    def loadCreds():
        credentialsJsonEntry.delete(0, "end")
        credentialsJsonEntry.insert(0, getFilePath())



    preferences.title("Preferences")
    preferences.iconbitmap(qrMaker.getCurrentPath()+'icon.ico')
    preferences.geometry('500x600')

    topText = Label(preferences, width=30, text="Filament Spool Client Preferences")

    cameraText = Label(preferences, width=30, text="Select Camera Instance:")
    cameraEntry = Combobox(preferences, width=10, values=qrReader.getCameras())

    printerText = Label(preferences, width=30, text="Printer list(x, y, z...)")
    printerEntry = Entry(preferences, width=20)

    qrWidthText = Label(preferences, width=30, text="QR Output Width (in.)")
    qrWidthEntry = Entry(preferences, width=10)

    qrHeightText = Label(preferences, width=30, text="QR Output Height (in.)")
    qrHeightEntry = Entry(preferences, width=10)

    settingsJsonText = Label(preferences, width=30, text="Load from settings")
    loadSettingsButton = Button(preferences, width=12, text="Load Settings", command=loadSettings)

    credentialsJsonText = Label(preferences, width=30, text="Path to Credentials file")
    credentialsJsonEntry = Entry(preferences, width=30)
    credentialsJsonButton = Button(preferences, width=7, text="Browse", command=loadCreds)

    sheetText = Label(preferences, width=30, text="Google Sheets Link")
    sheetEntry = Entry(preferences, width=30)
    sheetTest = Button(preferences, width=18, text="Test Auth and Link", command=testSheet)

    text = [cameraText, printerText, qrWidthText, qrHeightText, settingsJsonText, credentialsJsonText, sheetText]
    entry = [cameraEntry, printerEntry, qrWidthEntry, qrHeightEntry, False, credentialsJsonEntry, sheetEntry]
    buttons = [False, False, False, False, False, credentialsJsonButton, sheetTest]
    entryNames = ['cameraEntry', 'printerEntry', 'qrWidthEntry', 'qrHeightEntry', False, 'credentialsJsonEntry', 'sheetEntry']

    updateJsonButton = Button(preferences, text="Save Preferences", command=updateJson)

    statusText = Label(preferences, width=30)


    for i in range(1, 100, 2):
        preferences.grid_rowconfigure(i, minsize=10)

    topText.grid(column = 1, row = 0)
    row=2
    for i, j, a in zip(text, entry, buttons):
        if i:
            i.grid(column = 0, row = row)
        if j:
            j.grid(column = 1, row = row)
        if a:
            a.grid(column = 2, row=row)
        row+=2
    updateJsonButton.grid(column=1, row=row+4)
    loadSettingsButton.grid(column=1, row=row-6)
    statusText.grid(column=1, row=row+6)

    if path.exists(jsonPath):
        loadSettings()

    preferences.mainloop()
    preferences.quit()