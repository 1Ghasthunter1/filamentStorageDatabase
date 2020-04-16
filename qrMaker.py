from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from tkinter import messagebox
import qrcode
import os

folderName = "qrCodes"

def generateQR(qrData):
    if isinstance(qrData, str) == True:
        img = qrcode.make(qrData)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('entsans.ttf', 30)
        draw.text((40, 250), qrData, 0, font=font)
        makeFolder()
        img.save(getDesktopPath()+folderName+'/'+qrData+'.png')
    else:
        raise ValueError("generateQR Function requires string input!")

def makeFolder():
    desktopPath = getDesktopPath()
    if os.path.isdir(desktopPath+folderName) == False:
        os.system('mkdir '+desktopPath+folderName)
    else:
        pass

def getDesktopPath():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\')
    return desktop

def getCurrentPath():
    return (os.path.dirname(__file__)+'/')

def getFolderPath():
    return getDesktopPath()+folderName
generateQR("123456")