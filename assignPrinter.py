from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import qrReader
import qrMaker
import soundPlayer
import jsonOperation
import os
import qrMaker
import sheetOperation

skippedRows = [1, 3, 5, 7, 9, 11]
activePrinterColumn = 10 #according to google sheets

jsonPath = os.path.join(qrMaker.getCurrentPath(), "config\\settings.json")
activePrinter = StringVar()
def assignPrinterWindow():
    def saveChanges():
        pass
    def getPrinterList():
        data = jsonOperation.readFromJson("printerEntry", jsonPath)
        data = data.replace(" ", "")
        data = data.split(",")
        data.insert(0, "")
        data.insert(len(data), "None")
        return data
    printerList = getPrinterList()
    activePrinter.set(printerList[2])
    def getQRID():
        try:
            scanQREntry.delete(0, "end")
            scanQREntry.insert(0, qrReader.getQR(int(jsonOperation.readFromJson('cameraEntry', jsonPath))))
            statusText['text'] = "Successfully scanned QR Code"
        except:
            statusText['text'] = "Unable to scan QR Code"
    def changePrinter(cell, data):
        cell = sheetOperation.getCell(cell)
        if cell:
            sheetOperation.updateCell(cell.row, activePrinterColumn, data)
        else:
            print('couldnt fetch cell')
    assignPrinter = Tk()

    assignPrinter.title("Add Spool to Printer")
    assignPrinter.iconbitmap(qrMaker.getCurrentPath()+'icon.ico')
    assignPrinter.geometry('400x600')

    scanQRText = Label(assignPrinter, width=10, text="Spool ID: ")
    scanQRButton = Button(assignPrinter, text="Scan", command=getQRID)
    scanQREntry = Entry(assignPrinter, width=10)

    printerText = Label(assignPrinter, width=20, text="Select active printer:")
    printerEntry = OptionMenu(assignPrinter, activePrinter, *printerList)

    uploadText = Label(assignPrinter, width=15, text="Assign Printer")
    uploadButton = Button(assignPrinter, width=20, text="Save Changes", command=lambda:changePrinter(scanQREntry.get(), activePrinter.get()))

    statusText = Label(assignPrinter, width=25)

    text = [scanQRText, printerText, uploadText]
    entry = [scanQREntry, printerEntry, uploadButton]
        
    for i in skippedRows:
        assignPrinter.grid_rowconfigure(i, minsize=10)
    row=2
    for text, entry in zip(text, entry):
        text.grid(column = 0, row = row)
        entry.grid(column = 1, row = row)
        row+=2
    scanQRButton.grid(column=2, row=2)
    statusText.grid(column=0, row=row+2)
    assignPrinter.mainloop()
    assignPrinter.quit()
 