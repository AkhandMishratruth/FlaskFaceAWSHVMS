'''
    Helper functions

    @author Sanchit Mehta
    @copyright HyperVerge
'''

import os
import json

# GroupId decided based on the name of the folder
# which contains subfolders containing training faces
def getGroupId(path):
    """
    GroupId decided based on the name of the folder
    which contains subfolders containing training faces
    """
    return os.path.basename(os.path.normpath(path))

def getPeopleIds(path):
    peopleList = [o for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]
    return peopleList

def getJSONFromFile(path):
    if not os.path.isfile(path):
        print("Config file doesnot exist. Kindly \
               create a file with name 'configs.json'. \
               Refer 'configs_template.json' for an example of \
               configs.json file")
        return None

    with open(path) as data_file:
        data = json.load(data_file)
        return data
