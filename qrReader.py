import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from collections import Counter
import operator



def checkData(list):
    dataValues = Counter(list)
    cv2.destroyAllWindows()
    return max(dataValues, key=dataValues.get)

def getQR():
    qrData=[]
    try:
        video = cv2.VideoCapture(0)
    except:
        raise ValueError("Unable to open camera!")
    while True:
        _, frame = video.read()

        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            qrData.append(obj.data)


        cv2.imshow("QR Code Scanner", frame)

        if len(qrData)>=10:
            return checkData(qrData)
            

        key=cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            break

