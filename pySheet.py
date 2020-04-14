import gspread
from oauth2client.service_account import ServiceAccountCredentials
import inspect

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/Hunter/Documents/Python Scripts/demo/credentials1.json",scope)

client = gspread.authorize(creds)

sheet = client.open("spoolData").sheet1

materials = ['PLA', 'ABS', 'NYLON', 'PETG', 'CONDUCTIVE']

class Spool:
    """A class that stores 9 pieces of data relating to each spool,
    like weight, cost, etc"""
    def __init__(self, spoolID, dateAdded, materialID, color, materialWeight, costPerSpool, spoolWeight, manufacturer, isArchived, comment):
        self.spoolID = spoolID #6 digit spool ID
        self.dateAdded = dateAdded #mmddyyyy
        self.material = materials[materialID] #PLA, PETG, NYLON, ABS, etc.
        self.color = color #color, string
        self.materialWeight = materialWeight #weight of plastic in grams
        self.costPerSpool = costPerSpool #cost per spool 
        self.spoolWeight = spoolWeight # weight of the spool in grams
        self.manufacturer = manufacturer #spool manufacturer
        self.isArchived = False
        self.comment = comment #comments about spool

def getNextOpenRow(): #returns the row # as an integer of the next available row on the spreadsheet
    itemList = sheet.col_values(1)
    nextOpenRow = len(itemList)+1
    return nextOpenRow

def makeNewSpool():
    #gather data about new spool
    ID           = input("input spool ID: \n")
    date         = input("input date spool opened:\n")
    materialID   = input("input material ID: \n")
    color        = input("color of plastic: \n")
    matWeight    = input("plastic weight in grams: \n")
    costPerSpool = input("input cost per spool: \n")
    spoolWeight  = input("enter weight of the spool: \n")
    manufacturer = input("input manufacturer name: \n")
    comment      = input("any commments: \n")

    if checkIfCellExists(str(ID)) == True:
        print("A spool with that ID already exists!")
    else:
        #create new spool object
        newSpool = Spool(ID, date, materialID, color, matWeight, costPerSpool, spoolWeight, manufacturer, False ,comment)

        #upload new spool data to spreadsheet in new row
        sheet.insert_row([newSpool.spoolID, newSpool.dateAdded, newSpool.material, newSpool.color, newSpool.materialWeight, newSpool.costPerSpool, newSpool.spoolWeight, newSpool.manufacturer, newSpool.comment], getNextOpenRow())

def checkIfCellExists(spoolID):
    try:
        sheet.find(spoolID)
        return True
    except:
        return False
        
def getSpoolData(spoolID):
    if checkIfCellExists(spoolID) == True:
        spoolCell = sheet.find(spoolID)
        foundSpoolData = sheet.row_values(spoolCell.row)
        print(foundSpoolData)
    else:
        print("no spool has that ID!")


