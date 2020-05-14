import json
import os
import qrMaker

def readFromJson(key, jsonPath):
    """
    Reads from a json file given a key and path of the json
    """
    def trySettingsJson():
        if os.path.exists(jsonPath):
            return readJson()
        else:
            return -1

    def readJson():
        """
        asd
        """
        with open(jsonPath) as f:
            data = json.load(f)
            if data != False:
                return data[key]

    return trySettingsJson()

        

def writeToJson(dictionary, jsonPath):
    if os.path.exists(jsonPath) != True:
        with open(jsonPath, 'w') as fp:
            pass
    with open(jsonPath, 'w') as f:
        data = json.dump(dictionary, f)

    
