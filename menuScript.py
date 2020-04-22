from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
import qrMaker

#define vars
preferencesSkippedRows = [1, 3, 5, 7, 9, 11]
preferences = Tk()
preferences.withdraw()

def openPreferences():

    preferences.title("Preferences")
    preferences.iconbitmap(qrMaker.getCurrentPath()+'icon.ico')
    preferences.geometry('400x600')

    topText = Label(preferences, width=30, text="Filament Spool Client Preferences")

    jsonPathText = Label(preferences, width=30, text="Json Path")
    jsonPathEntry = Entry(preferences, width=30)
    jsonPathButton = Button(preferences, text="Browse", command=getJsonDirectory)
    text = [jsonPathText]
    entry = [jsonPathEntry]
        
    for i in preferencesSkippedRows:
        preferences.grid_rowconfigure(i, minsize=10)

    topText.grid(column = 0, row = 0)
    jsonPathButton.grid(column = 2, row = 2)
    row=2
    for text, entry in zip(text, entry):
        text.grid(column = 0, row = row)
        entry.grid(column = 1, row = row)
        row+=2

    preferences.mainloop()

def getJsonDirectory():
    jsonPath = filedialog.askdirectory(parent=preferences, initialdir=qrMaker.getCurrentPath(), title='Please select a directory', filetypes = [("all files",".*")])
    print(jsonPath)

