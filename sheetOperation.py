from tkinter import messagebox
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import qrMaker
import jsonOperation
import os
jsonPath = os.path.join(qrMaker.getCurrentPath(), "config\\settings.json")
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(jsonOperation.readFromJson('credentialsJsonEntry', jsonPath),scope)
except:
    print("No service credentials json found!")
    exit()

client = gspread.authorize(creds)
sheet = client.open("spoolData").sheet1

def insertRow(rowData, rowNumber):
    sheet.insert_row(rowData, rowNumber)

def checkIfCellExists(cellData):
    try:
        sheet.find(str(cellData))
        return True
    except:
        return False

def getSpoolData(spoolID):
    if checkIfCellExists(spoolID) == True:
        spoolCell = sheet.find(spoolID)
        foundSpoolData = sheet.row_values(spoolCell.row)
        return foundSpoolData
    else:
        return False

def getNextOpenRow(): #returns the row # as an integer of the next available row on the spreadsheet
    itemList = sheet.col_values(1)
    nextOpenRow = len(itemList)+1
    return nextOpenRow

def deleteRow(spoolID, msgBox):
    def delete():
        try:
            spoolCell = sheet.find(str(spoolID))
            sheet.delete_row(spoolCell.row)
            return True
        except:
            return False
    if msgBox:
        confirmDel = messagebox.askyesno('Confirm Delete?', f'Are you sure you want to delete {spoolID}?')
        if confirmDel == True:
            return delete()
    else:
        return delete()

def getCell(cellData):
    '''
    Simple function that returns where a cell is given data
    '''
    try:
        return sheet.find(str(cellData))
    except:
        return False

def updateCell(row, column, data):
    try:
        sheet.update_cell(row, column, data)
        return True
    except:
        return False