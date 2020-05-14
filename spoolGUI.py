#necessary impoorts
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import inspect
import qrReader
import time
import soundPlayer
import qrMaker
import random
import openWeb
import menuScript
import jsonOperation
import os
import assignPrinter

#data from first pyscript
jsonPath = os.path.join(qrMaker.getCurrentPath(), "config\\settings.json")
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(jsonOperation.readFromJson('credentialsJsonEntry', jsonPath),scope)
except:
    print("No service credentials json found!")
    exit()
client = gspread.authorize(creds)

sheet = client.open("spoolData").sheet1
#someVars
spreadsheetURL = jsonOperation.readFromJson("sheetEntry", jsonPath)
qrInches = 4 #height of generated QR code in inches

class Spool:
    """A class that stores 9 pieces of data relating to each spool,
    like weight, cost, etc"""
    def __init__(self, spoolID, dateAdded, material, color, materialWeight, costPerSpool, spoolWeight, manufacturer, isArchived, comment):
        self.spoolID = spoolID #6 digit spool ID
        self.dateAdded = dateAdded #mmddyyyy
        self.material = material #PLA, PETG, NYLON, ABS, etc.
        self.color = color #color, string
        self.materialWeight = materialWeight #weight of plastic in grams
        self.costPerSpool = costPerSpool #cost per spool 
        self.spoolWeight = spoolWeight # weight of the spool in grams
        self.manufacturer = manufacturer #spool manufacturer
        self.isArchived = isArchived
        self.comment = comment #comments about spool

def getNextOpenRow(): #returns the row # as an integer of the next available row on the spreadsheet
    itemList = sheet.col_values(1)
    nextOpenRow = len(itemList)+1
    return nextOpenRow

def updateStatusText(text):
    statusText['text']=text

def makeNewSpool():
    #gather data about new spool
    ID           = IDEntry.get()
    date         = dateEntry.get()
    materialID   = materialEntry.get()
    color        = colorEntry.get()
    matWeight    = weightEntry.get()
    costPerSpool = costPerSpoolEntry.get()
    spoolWeight  = spoolWeightEntry.get()
    manufacturer = manufacturerEntry.get()
    isArchived   = spoolActive.get()
    comment      = commentEntry.get()

    if checkIfCellExists(str(ID)) == True:
        updateStatusText("A spool with that ID already exists!")
    elif ID == "":
        updateStatusText("Please enter a spool ID")
    else:
        #create new spool object
        newSpool = Spool(ID, date, materialID, color, matWeight, costPerSpool, spoolWeight, manufacturer, isArchived ,comment)

        #upload new spool data to spreadsheet in new row
        sheet.insert_row([newSpool.spoolID, newSpool.dateAdded, newSpool.material, newSpool.color, newSpool.materialWeight, newSpool.costPerSpool, newSpool.spoolWeight, newSpool.manufacturer, newSpool.isArchived, newSpool.comment], getNextOpenRow())
        updateStatusText("Spool successfully created!")

def generateSpoolID():
    tempSpoolID = random.randint(100000, 999999)
    if checkIfCellExists(tempSpoolID) == False:
        setEntryText(IDEntry, tempSpoolID)
    elif checkIfCellExists(tempSpoolID) == True:
        generateSpoolID()

def checkIfCellExists(cellData):
    try:
        sheet.find(str(cellData))
        return True
    except:
        return False

def setEntryText(entryName, text):
    entryName.delete(0,"end")
    entryName.insert(0, text)


def getSpoolData():
    changeToMode(5)
    spoolID = IDEntry.get()
    if checkIfCellExists(spoolID) == True:
        spoolCell = sheet.find(spoolID)
        foundSpoolData = sheet.row_values(spoolCell.row)
        for i, x in zip(entryList[1:], foundSpoolData):
            setEntryText(i, x)
        changeToMode(2)
        updateStatusText("Data Received!")
    else:
        changeToMode(2)
        updateStatusText("Couldn't find a spool with that ID!")

#define some variables
skippedRows = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
#create click functions, etc

currentMode = 0
def changeToMode(mode):
    if mode >= 1 or mode <= 4:
        if mode == 1:
            uploadNew['state']='enabled'
            getSpool['state']='disabled'
            applyChanges['state']='disabled'
            deleteSpool['state']='disabled'
            IDEntry['state']='enabled'
            dateEntry['state']='enabled'
            materialEntry['state']='enabled'
            colorEntry['state']='enabled'
            weightEntry['state']='enabled'
            costPerSpoolEntry['state']='enabled'
            spoolWeightEntry['state']='enabled'
            manufacturerEntry['state']='enabled'
            spoolActive['state']='enabled'
            commentEntry['state']='enabled'
        elif mode == 2:
            uploadNew['state']='disabled'
            getSpool['state']='enabled'
            applyChanges['state']='disabled'
            deleteSpool['state']='disabled'
            IDEntry['state']='enabled'
            dateEntry['state']='disabled'
            materialEntry['state']='disabled'
            colorEntry['state']='disabled'
            weightEntry['state']='disabled'
            costPerSpoolEntry['state']='disabled'
            spoolWeightEntry['state']='disabled'
            manufacturerEntry['state']='disabled'
            spoolActive['state']='disabled'
            commentEntry['state']='disabled'
        elif mode == 3:
            uploadNew['state']='disabled'
            getSpool['state']='disabled'
            applyChanges['state']='enabled'
            deleteSpool['state']='disabled'
            IDEntry['state']='enabled'
            dateEntry['state']='enabled'
            materialEntry['state']='enabled'
            colorEntry['state']='enabled'
            weightEntry['state']='enabled'
            costPerSpoolEntry['state']='enabled'
            spoolWeightEntry['state']='enabled'
            manufacturerEntry['state']='enabled'
            spoolActive['state']='enabled'
            commentEntry['state']='enabled'
        elif mode == 4:
            uploadNew['state']='disabled'
            getSpool['state']='disabled'
            applyChanges['state']='disabled'
            deleteSpool['state']='enabled'
            IDEntry['state']='enabled'
            dateEntry['state']='disabled'
            materialEntry['state']='disabled'
            colorEntry['state']='disabled'
            weightEntry['state']='disabled'
            costPerSpoolEntry['state']='disabled'
            spoolWeightEntry['state']='disabled'
            manufacturerEntry['state']='disabled'
            spoolActive['state']='disabled'
            commentEntry['state']='disabled'
        elif mode == 5:
            uploadNew['state']='disabled'
            getSpool['state']='enabled'
            applyChanges['state']='disabled'
            deleteSpool['state']='disabled'
            IDEntry['state']='enabled'
            dateEntry['state']='enabled'
            materialEntry['state']='enabled'
            colorEntry['state']='enabled'
            weightEntry['state']='enabled'
            costPerSpoolEntry['state']='enabled'
            spoolWeightEntry['state']='enabled'
            manufacturerEntry['state']='enabled'
            spoolActive['state']='enabled'
            commentEntry['state']='enabled'
        currentMode = mode

    else:
        raise ValueError("changeToMode function only accepts values 1-4!")
    


def deleteRow():
    confirmDel = messagebox.askyesno('Confirm Delete?', 'Are you sure you want to delete '+str(IDEntry.get()+'?'))
    if confirmDel == True:
        try:
            spoolCell = sheet.find(str(IDEntry.get()))
            sheet.delete_row(spoolCell.row)
            updateStatusText("Filament Profile Deleted!")
        except:
            updateStatusText("Couldnt find a spool with that ID!")
    else:
        pass


def editSpool():
    confirmEdit = messagebox.askyesno('Confirm Edit?', 'Are you sure you want to edit '+str(IDEntry.get()+'?'))
    if  confirmEdit == True:
        try:
            spoolCell = sheet.find(str(IDEntry.get()))
            sheet.delete_row(spoolCell.row)
            makeNewSpool()
            updateStatusText("Updated Spool "+str(IDEntry.get()) +" Data!")
        except:
            updateStatusText("Unable to update "+str(IDEntry.get()) +" Data!")
    else:
        pass
    
def getQRID():
    try:
        print("step1")
        setEntryText(IDEntry, qrReader.getQR(int(jsonOperation.readFromJson("cameraEntry", jsonPath))))
        if currentMode == 2:
            getSpoolData()
        updateStatusText("QR code has been scanned!")
        soundPlayer.playChime()
    except:
        updateStatusText("Unable to scan QR code")

def generateQR():
    if str(IDEntry.get()) == "":
        updateStatusText("Please enter a spool ID")

    else:
        qrMaker.generateQR(str(IDEntry.get()), qrInches)
        updateStatusText(str(IDEntry.get())+" QR code has been saved to: \n" + qrMaker.getFolderPath())

def openChrome():
    if openWeb.openChrome(spreadsheetURL) == False:
        updateStatusText("Unable to open spreadsheet.")

def preferences():
    menuScript.openPreferences()



#create objects
window = Toplevel() #create the main window object
placeholder = Label(window, text="")
statusText = Label(window, text="", anchor=CENTER)


uploadNew = Button(window, text="Upload Spool", command=makeNewSpool)
getSpool = Button(window, text="Update Spool Info", command=getSpoolData)
applyChanges = Button(window, text="Apply Changes", command=editSpool)
deleteSpool = Button(window, text="Delete Spool", command=deleteRow)

scanQR = Button(window, text="Scan QR Code", command=getQRID)
generateQRButton = Button(window, text="Generate QR Code", command=generateQR)

IDText = Label(window, text="Spool ID:")
IDEntry = Entry(window, width=25)
generateIDButton = Button(window, text="Generate ID", command=generateSpoolID)
openBrowserButton = Button(window, text="Open Sheet", command=openChrome)

dateText = Label(window, text="Date Opened:")
dateEntry = Entry(window, width=25)

materialText = Label(window, text="Material:")
materialEntry = Combobox(window, width=22, values=("PLA","ABS","PETG","Nylon","Conductive"))

colorText = Label(window, text="Color:")
colorEntry = Entry(window, width=25)

weightText = Label(window, text="Filament Weight:")
weightEntry = Entry(window, width=25)

costPerSpoolText = Label(window, text="Cost per Spool:")
costPerSpoolEntry = Entry(window, width=25)

spoolWeightText = Label(window, text="Empty Spool Weight:")
spoolWeightEntry = Entry(window, width=25)

manufacturerText = Label(window, text="Manufacturer: ")
manufacturerEntry = Entry(window, width=25)

spoolActiveText = Label(window, text="Spool active: ")
spoolActive = Combobox(window, width=22, values=("Deactive", "Active"))

commentText = Label(window, text="Comments:")
commentEntry = Entry(window, width=25)


entryList = [IDEntry, dateEntry, materialEntry, colorEntry, weightEntry, costPerSpoolEntry, spoolWeightEntry, manufacturerEntry, spoolActive, commentEntry]
textList  = [IDText, dateText, materialText, colorText, weightText, costPerSpoolText, spoolWeightText, manufacturerText, spoolActiveText, commentText]
doButtonList = [uploadNew, getSpool, applyChanges, deleteSpool]


#menu functions
def addNewSpoolMode():
    changeToMode(1)

def viewSpoolMode():
    changeToMode(2)

def editSpoolMode():
    changeToMode(3)

def deleteSpoolMode():
    changeToMode(4)

def assignPrinterMode():
    assignPrinter.assignPrinterWindow()

#Configure Menus
menuBar = Menu(window)
filemenu = Menu(menuBar, tearoff=0)
filemenu.add_command(label = "Preferences", command = preferences)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)

actionmenu = Menu(menuBar, tearoff=0)
actionmenu.add_command(label = "Add Spool", command=addNewSpoolMode)
actionmenu.add_command(label = "View Spool", command=viewSpoolMode)
actionmenu.add_command(label = "Assign Printer", command=assignPrinterMode)
actionmenu.add_command(label = "Edit Spool", command=editSpoolMode)
actionmenu.add_command(label = "Delete Spool", command=deleteSpoolMode)
menuBar.add_cascade(label="File", menu=filemenu)
menuBar.add_cascade(label="Actions", menu=actionmenu)

#object methods
window.title("Filament Storage Client V0.2.1")
window.iconbitmap(qrMaker.getCurrentPath()+'icon.ico')
window.geometry('550x600')

window.config(menu=menuBar)

#locations of objects
scanQR.grid(column=2, row=3)
generateQRButton.grid(column=3, row=3)
generateIDButton.grid(column=2, row=5)
openBrowserButton.grid(column=3, row=5)

rowVar = 3
for text, entry in zip(textList, entryList):
    text.grid(column=0, row = rowVar)
    entry.grid(column=1, row = rowVar)
    rowVar+=2

colVar = 0
for button in doButtonList:
    button.grid(column=colVar, row=25)
    colVar +=1

placeholder.grid(column=0, row=26)
statusText.grid(column=1, row=26)

for a in skippedRows:
    window.grid_rowconfigure(a, minsize=10)

#main loop
changeToMode(1)
window.mainloop()
qrMaker.dpiWindow.quit()
window.quit()