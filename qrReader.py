import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from collections import Counter
import operator



def checkData(list):
    dataValues = Counter(list)
    cv2.destroyAllWindows()
    return max(dataValues, key=dataValues.get)

def getQR(cameraID):
    qrData=[]
    try:
        video = cv2.VideoCapture(cameraID, cv2.CAP_DSHOW)
    except:
        raise NameError("Could not access the camera, for some weird reason")
    while True:
        _, frame = video.read()

        decodedObjects = pyzbar.decode(frame)
        for obj in decodedObjects:
            qrData.append(obj.data)


        cv2.imshow("QR Code Scanner, press ESC to exit", frame)

        if len(qrData)>=10:
            video.release()
            return checkData(qrData)
            

        key=cv2.waitKey(1)
        if key == 27:
            video.release()
            cv2.destroyAllWindows()
            break

def getCameras():
    index = 0
    cameraArray = []
    while True:
        test = cv2.VideoCapture(index)
        if not test.read()[0]:
            break
        else:
            cameraArray.append(index)
        test.release()
        index +=1
    return cameraArray
