
import json
import os

import psycopg2
import pystray
from PIL import Image


#pip install...
class StatsFileNotFound(Exception):
    """Base error for a statistic file that was not found."""
    pass

class StatNotFound(Exception):
    """Base error for a statistic that was not found within a stat file."""
    pass

class StatisticsFile:
    def __init__(self, uuid: str, world_name: str, file_path) -> None:
        self.uuid = uuid
        self.file_name = f"{self.uuid}.json".strip()
        self.file_path = file_path
        self.world_name = world_name
        
    def get_stat(self, name: str) -> dict:
        """Gets a statistic from value name."""
        pass




class Database:
    def __init__(self, username:str, password:str, host:str, port:int, database:str = 'mttesting') -> None:
        dsn = f"postgres://{username}:{password}@{host}:{port}/{database}"
        self.conn = psycopg2.connect(dsn=dsn)

    def push(self, stat_file: StatisticsFile):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO
        """)
        self.conn.commit()
        
    def testPush(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO stats("UUID", "world_id", "stat_name", "stat_val") VALUES('1234', (SELECT "world_ID" FROM world WHERE world.mcuser_id = '1234' AND world.world_name = 'New_World'), 'time_swimming', '31');
        """)
        self.conn.commit()

minetraxDatabase = Database('postgres', '1234', 'localhost', 5432)
minetraxDatabase.testPush()

#search for file and return full path
def findFiles(name,path):
    fullFilePaths = []
    exclude = set(["advancements"])
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude]
        if name in files:
            fullFilePaths.append(os.path.join(root, name))
            
    return fullFilePaths

def findWorlds():
    for root, dirs, files in os.walk("C:\\Users\\"):
        if ".minecraft" in dirs: 
           worldsPaths = root + "\\.minecraft\\saves\\saves\\"
           return worldsPaths


def trackWorld(world, UUID):
    worldsPaths = findWorlds()
    fileName = UUID + ".json"

    if world not in os.listdir(worldsPaths):
        print("World Not Found")
    else:
        path = worldsPaths + world
        #search for the file
        filePath = findFiles(fileName,path)
        print(filePath[0])
        #create a statistics file object
        newStatFileToPush = StatisticsFile(UUID, world, filePath[0])
        #minetraxDatabase.push(newStatFileToPush)
        #next push to DB

def trackMostRecent(UUID):
    
    worldsPaths = findWorlds()
    worlds = os.listdir(worldsPaths)
    fileName = UUID + ".json"
    # get the full path to the file
    fullFilePaths = findFiles(fileName, worldsPaths)
    mostRecentFile = fullFilePaths[0]
    mostRecentWorldName = ""

    for files in fullFilePaths:
        if os.path.getmtime(files) > os.path.getmtime(mostRecentFile):
            mostRecentFile = files

    print(mostRecentFile)

    for name in worlds:
        if name in mostRecentFile:
            mostRecentWorldName = name

    print(mostRecentWorldName)
    statFileToPush = StatisticsFile(UUID, mostRecentWorldName ,mostRecentFile)
    #minetraxDatabase.push(newStatFileToPush)
    #create a statistics file object

    #next push to DB


global UUID
#a5d5ab98-326c-4d57-8be3-dc4e7a81bd0e
UUID = ""

#System tray icon stuff
image = Image.open("img/Minetraxbackground.png")

queries = [
    'Enter UUID',
    'Track World',
    'Track most recent world',
    'Exit'
]


def after_click(icon, query):
    global UUID

    if str(query) == queries[0]:
        UUID = input("Enter UUID: ")
        # icon.stop()
    elif str(query) == queries[1]:
        if UUID == "":
            UUID = input("Enter UUID: ")
        world = input("Enter World Name: ")
        trackWorld(world,UUID)
    elif str(query) == queries[2]:
        if UUID == "":
            UUID = input("Enter UUID: ")
        trackMostRecent(UUID)
    elif str(query) == queries[3]:
        icon.stop()

def setup(): # Put object definitions and other code in here
    icon = pystray.Icon("MT", image, "Minetrax", menu=pystray.Menu(
    pystray.MenuItem(queries[0], after_click),
    pystray.MenuItem(queries[1], after_click),
    pystray.MenuItem(queries[2], after_click),
    pystray.MenuItem(queries[3], after_click)))
    icon.run()

    """
        INSERT INTO mcuser("UUID", username) VALUES ('4006', 'testing');
        """
