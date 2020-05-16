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

def inchToPixels(var):
    dpi = int(ctypes.windll.user32.GetDpiForWindow(dpiWindow.winfo_id()))
    dpi=dpi*var
    dpi=int(round(dpi))
    return dpi

def getDesktopPath():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\')
    return desktop

def getCurrentPath():
    return (os.path.dirname(__file__)+'\\')

def getFolderPath():
    return getDesktopPath()+folderName

def generateQR(qrData, width, height, mode):
    '''
    Takes 3 inputs:
    -qrData: Raw QR Data
    -inches: height in inches
    -mode: mode=0 -> text beneath, mode=1 -> text to the right of
    '''

    if isinstance(qrData, str) == True:
        if mode == 0:
            #ratios for text to qr, used when scaling down the text to fit qrHeight no matter what:
            # text at 20,65 size 20 enter sansman where qr height is 2.

            #dependent variables on func inchToPixels

            textHScale = int(round(inchToPixels(width)/9.6))               #20, 165, and 20 were all found by trial and error with a 
            textVScale = int(round(inchToPixels(width)/1.16363636364))     #QR size of 2. all that is needed is to apply these constants
            textTextScale = int(round(inchToPixels(width)/12))            #to the QR size being inputted

            rectScale1 = int(round(inchToPixels(width)/64))
            rectScale2 = int(round(inchToPixels(width)/1.02127659574))
            rectWidthScale = int(round(inchToPixels(width)/48))
            #math to solve these values: pixelSize/foundValue(20, 65, etc) = ratio
            #use the ratio above which returns the scaled position of the text
            img = qrcode.make(qrData)
            img = img.resize((inchToPixels(width),inchToPixels(width)))
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype(r'C:\Users\Hunter\Documents\Filament Client\fonts', textTextScale)
            except:
                font=None
            draw.text((textHScale, textVScale), f"ID: {qrData} ", 0, font=font)
            draw.rectangle([(rectScale1, rectScale1), (rectScale2,rectScale2)],
                fill = None,
                outline = 0,
                width = rectWidthScale)
        elif mode == 1:
        
            #ratios for text to qr, used when scaling down the text to fit qrHeight no matter what:
            # text at 20,65 size 20 enter sansman where qr height is 2.

            x1 = int(round((inchToPixels(height)/19.2)))
            y1 = x1
            x2 = int(round((inchToPixels(width) - x1)))
            y2 = int(round((inchToPixels(height) - x1)))
            rectWidthScale = int(round((inchToPixels(height)/48)))

            hScaleMath=inchToPixels(height)+(3*inchToPixels(height)/19.2)
            textHScale = int(round(hScaleMath))

            textTextScale = int(round((inchToPixels(width)/12))) 

            vScaleMath=inchToPixels(height)/2-textTextScale
            textVScale = int(round(vScaleMath))
            
            img = Image.new("L", (inchToPixels(width), inchToPixels(height)), color=255)
            qrOutput = qrcode.make(qrData)
            qrOutput = qrOutput.resize((inchToPixels(height), inchToPixels(height)))
            img.paste(qrOutput)
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype('fonts\entsans.ttf', textTextScale)
            except:
                font = None
            draw.text((textHScale, textVScale), f"Spool ID:\n{qrData}", 0, font=font)
            draw.rectangle([(x1, y1), (x2, y2)],
                fill = None,
                outline = 0,
                width = rectWidthScale)
        makeFolder()
        img.save(getDesktopPath()+folderName+'/'+qrData+'.png')
    else:
        raise ValueError("generateQR Function requires string input!")

def getFont():
    font = ImageFont.truetype('fonts\entsans.ttf', 20)
    return font

generateQR("TESTDATA", 2, 1, 1)
