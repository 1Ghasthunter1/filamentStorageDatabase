from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from tkinter import messagebox
import qrcode
import os

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
def generateQR(qrData):
    if isinstance(qrData, str) == True:
        img = qrcode.make(qrData)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('entsans.ttf', 30)
        draw.text((40, 250), qrData, 0, font=font)
        img.save(desktop+'\\'+qrData+'.png')
    else:
        raise ValueError("generateQR Function requires string input!")

def getDesktopPath():
        return desktop



