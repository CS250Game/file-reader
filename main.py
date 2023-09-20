import json
import os

#search for file and return full path
def findFile(name,path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

#start at users file for file search
path = "C:\\Users\\"
fileName = "dbf84c87-9967-3dcc-857c-cb206907df92.json"

# get the full path to the file
fullFilePath = findFile(fileName, path)

#open the file and load data to dictionary
file = open(fullFilePath)
minecraftData = json.load(file)

#print all data
for i in minecraftData:
   print(i)



#Find out what stats we want to display and pull those into variables
#Push those stats to DB