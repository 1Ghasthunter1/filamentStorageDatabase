from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from tkinter import messagebox
import tkinter
import qrcode
import os
import ctypes
import math

ctypes.windll.shcore.SetProcessDpiAwareness(1)
dpiWindow = tkinter.Tk()
dpiWindow.withdraw()
folderName = "qrCodes"
qrHeight = 2 #inches


def makeFolder():
    desktopPath = getDesktopPath()
    if os.path.isdir(desktopPath+folderName) == False:
        os.system('mkdir '+desktopPath+folderName)
    else:
        pass

def getInchPixels(inches):
    dpi = int(ctypes.windll.user32.GetDpiForWindow(dpiWindow.winfo_id()))
    inchPixels = dpi * inches
    inchPixels = int(round(inchPixels))
    return inchPixels

def getDesktopPath():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\')
    return desktop

def getCurrentPath():
    return (os.path.dirname(__file__)+'\\')

def getFolderPath():
    return getDesktopPath()+folderName

def generateQR(qrData, inches):
    if isinstance(qrData, str) == True:
        
        #ratios for text to qr, used when scaling down the text to fit qrHeight no matter what:
        # text at 20,65 size 20 enter sansman where qr height is 2.

        #dependent variables on func getInchPixels

        textHScale = int(round(getInchPixels(inches)/9.6))               #20, 165, and 20 were all found by trial and error with a 
        textVScale = int(round(getInchPixels(inches)/1.16363636364))     #QR size of 2. all that is needed is to apply these constants
        textTextScale = int(round(getInchPixels(inches)/9.6))            #to the QR size being inputted

        rectScale1 = int(round(getInchPixels(inches)/64))
        rectScale2 = int(round(getInchPixels(inches)/1.02127659574))
        rectWidthScale = int(round(getInchPixels(inches)/48))
        #math to solve these values: pixelSize/foundValue(20, 65, etc) = ratio
        #use the ratio above which returns the scaled position of the text
        img = qrcode.make(qrData)
        img = img.resize((getInchPixels(inches),getInchPixels(inches)))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arialbd.ttf', textTextScale)
        draw.text((textHScale, textVScale), qrData, 0, font=font)
        draw.rectangle([(rectScale1, rectScale1), (rectScale2,rectScale2)],
            fill = None,
            outline = 0,
            width = rectWidthScale)
        makeFolder()
        img.save(getDesktopPath()+folderName+'/'+qrData+'.png')
    else:
        raise ValueError("generateQR Function requires string input!")
