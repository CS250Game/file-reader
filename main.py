import json
import os
import psycopg2


#connect to database to retrieve & send data
#https://www.postgresqltutorial.com/postgresql-python/connect/

#set up db connection, needs actual db info 
#Connection should ideally be made in a config file
dbConnection = psycopg2.connect(
    host="localhost",
    database="suppliers",
    user="postgres",
    password="Abcd1234")



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