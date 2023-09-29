import json
import os
import psycopg2
from configparser import ConfigParser



#downloading postgres to test connection
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

#connect to database to retrieve & send data
#https://www.postgresqltutorial.com/postgresql-python/connect/

#set up db connection, needs actual db info 
#Connection should ideally be made in a config file
dbConnection = config()



#search for file and return full path
def findFile(name,path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

#start at users file for file search
UID = "dbf84c87-9967-3dcc-857c-cb206907df92"

path = "C:\\Users\\"
fileName = UID + ".json"

# get the full path to the file
fullFilePath = findFile(fileName, path)

#open the file and load data to dictionary
file = open(fullFilePath)
minecraftData = json.load(file)


#print all data
for i in minecraftData:
   print(i)



#get file with most recent save
#os.path.getctime(path)


#Find out what stats we want to display and pull those into variables
#Push those stats to DB

#stat.walkOneCm
#stat.killEntity.Chicken
#stat.swimOneCm
#stat.climbOneCm
#stat.flyOneCm
#stat.timeSinceDeath
#stat.sprintOneCm
#stat.playOneMinute
#stat.killEntity.Pig
#stat.killEntity.Cow
#stat.damageDealt
#stat.killEntity.Sheep
#stat.killEntity.Donkey