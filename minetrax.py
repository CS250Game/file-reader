import typing
import json
import os
from sqlite3 import connect
import psycopg2
import pystray
from PIL import Image

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

    def search_stat(self, value: typing.Union[int, tuple])-> dict:
        """Searches the stats file for stats with values matching the specified
        number or multiple within the range.
        `value` can either be a int or tuple."""
        pass

    @staticmethod
    def find_uuid() -> str:
        """Finds a UUID from a worldname."""
        pass

    @staticmethod
    def wait_for_new_world() -> tuple:
        """Waits for the creation of a new world. Once found, this will
        return the world name and UUID of the stats file in a tuple."""
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


#minetraxDatabase = Database()

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

def after_click(icon, query):
    global UUID
    queries = [
    'Enter UUID',
    'Track World',
    'Track most recent world',
    'Exit'
]

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

def setup(image, queries): # Put object definitions and other code in here
    icon = pystray.Icon("MT", image, "Minetrax", menu=pystray.Menu(
    pystray.MenuItem(queries[0], after_click),
    pystray.MenuItem(queries[1], after_click),
    pystray.MenuItem(queries[2], after_click),
    pystray.MenuItem(queries[3], after_click)))
    icon.run()


