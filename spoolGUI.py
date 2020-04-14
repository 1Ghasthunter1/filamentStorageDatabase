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

#data from first pyscript
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/Hunter/Documents/Python Scripts/demo/spoolClient/credentials1.json",scope)
except:
    print("No service credentials json found!")
    exit()
client = gspread.authorize(creds)

sheet = client.open("spoolData").sheet1



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

def updateStatusText(string1):
    statusText['text']=string1

def makeNewSpool():
    #gather data about new spool
    ID           = IDEntry.get()
    date         = dateEntry.get()
    materialID   = materialEntry.get()
    color        = colorEntry.get()
    matWeight    = matEntry.get()
    costPerSpool = costPerSpoolEntry.get()
    spoolWeight  = spoolWeightEntry.get()
    manufacturer = manufacturerEntry.get()
    isArchived   = spoolActive.get()
    comment      = commentEntry.get()

    if checkIfCellExists(str(ID)) == True:
        print("A spool with that ID already exists!")
        updateStatusText("A spool with that ID already exists!")
    else:
        #create new spool object
        newSpool = Spool(ID, date, materialID, color, matWeight, costPerSpool, spoolWeight, manufacturer, isArchived ,comment)

        #upload new spool data to spreadsheet in new row
        sheet.insert_row([newSpool.spoolID, newSpool.dateAdded, newSpool.material, newSpool.color, newSpool.materialWeight, newSpool.costPerSpool, newSpool.spoolWeight, newSpool.manufacturer, newSpool.isArchived, newSpool.comment], getNextOpenRow())
        updateStatusText("Spool successfully created!")

def checkIfCellExists(spoolID):
    try:
        sheet.find(spoolID)
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
        for i, x in zip(entryList, foundSpoolData):
            setEntryText(i, x)
        changeToMode(2)
        updateStatusText("Data Received!")
    else:
        print("no spool has that ID!")
        updateStatusText("Couldn't find a spool with that ID!")

#define some variables
skippedRows = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
#create click functions, etc

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
            matEntry['state']='enabled'
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
            matEntry['state']='disabled'
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
            matEntry['state']='enabled'
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
            matEntry['state']='disabled'
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
            matEntry['state']='enabled'
            costPerSpoolEntry['state']='enabled'
            spoolWeightEntry['state']='enabled'
            manufacturerEntry['state']='enabled'
            spoolActive['state']='enabled'
            commentEntry['state']='enabled'

    else:
        raise ValueError("changeToMode function only accepts values 1-4!")
def updateMode():
    currentMode = mode.get()
    if currentMode == 1:
        changeToMode(1)

    if currentMode == 2:
        changeToMode(2)

    if currentMode == 3:
        changeToMode(3)

    if currentMode == 4:
        changeToMode(4)



def applyChanges():
    pass

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
    try:
        spoolCell = sheet.find(str(IDEntry.get()))
        sheet.delete_row(spoolCell.row)
        makeNewSpool()
        updateStatusText("Updated Spool "+str(IDEntry.get()) +" Data!")
    except:
        updateStatusText("Unable to update "+str(IDEntry.get()) +" Data!")

def getQRID():
    setEntryText(IDEntry, qrReader.getQR())
    updateStatusText("QR code has been scanned!")
    soundPlayer.playChime()
    
#create objects
window = Tk() #create the main window object
selectorText = Label(window, text="Select Mode: ")
placeholder = Label(window, text="")
statusText = Label(window, text="", anchor=CENTER)
mode = IntVar() #wether we are uploading, editing, or deleting


uploadNew = Button(window, text="Upload Spool", command=makeNewSpool)
getSpool = Button(window, text="Update Spool Info", command=getSpoolData)
applyChanges = Button(window, text="Apply Changes", command=editSpool)
deleteSpool = Button(window, text="Delete Spool", command=deleteRow)

newSpool = Radiobutton(window,text='New Spool', value=1, variable=mode, command=updateMode) #create mode selector button objects
viewSpool = Radiobutton(window,text='View Spool Data', value=2, variable=mode, command=updateMode)
editSpool = Radiobutton(window,text='Edit Spool', value=3, variable=mode, command=updateMode)
delSpool = Radiobutton(window,text='Delete Spool', value=4, variable=mode, command=updateMode)

scanQR = Button(window, text="Scan QR Code", command=getQRID)
IDText = Label(window, text="Spool ID:")
IDEntry = Entry(window, width=25)

dateText = Label(window, text="Date Opened:")
dateEntry = Entry(window, width=25)

materialText = Label(window, text="Material:")
materialEntry = Combobox(window, width=22, values=("PLA","ABS","PETG","Nylon","Conductive"))

colorText = Label(window, text="Color:")
colorEntry = Entry(window, width=25)

matText = Label(window, text="Filament Weight:")
matEntry = Entry(window, width=25)

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


entryList = [IDEntry, dateEntry, materialEntry, colorEntry, matEntry, costPerSpoolEntry, spoolWeightEntry, manufacturerEntry, spoolActive, commentEntry]
textList  = [IDText, dateText, materialText, colorText, matText, costPerSpoolText, spoolWeightText, manufacturerText, spoolActiveText, commentText]
radButtonList = [newSpool, viewSpool, editSpool, delSpool]
doButtonList = [uploadNew, getSpool, applyChanges, deleteSpool]

#object methods
window.title("Filament Storage Client V0.1.1")
window.iconbitmap('C:/Users/Hunter/Documents/Python Scripts/demo/SpoolClient/icon.ico')
window.geometry('500x600')

#locations of objects
selectorText.grid(column=0, row=0)
scanQR.grid(column=2, row=3)
colVar = 0
for button in radButtonList:
    button.grid(column=colVar, row=1)
    colVar += 1

rowVar = 3
for text, entry in zip(textList, entryList):
    text.grid(column=0, row = rowVar)
    entry.grid(column=1, row = rowVar)
    rowVar+=2

colVar = 0
for button in doButtonList:
    button.grid(column=colVar, row=23)
    colVar +=1

placeholder.grid(column=0, row=24)
statusText.grid(column=1, row=24)

newSpool.invoke()
for a in skippedRows:
    window.grid_rowconfigure(a, minsize=10)
    print(a)

#main loop
window.mainloop()

