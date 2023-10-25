from configparser import ConfigParser
import json
import os
import psycopg2
import typing
import pystray
from PIL import Image

class StatsFileNotFound(Exception):
    """Base error for a statistic file that was not found."""
    pass

class StatNotFound(Exception):
    """Base error for a statistic that was not found within a stat file."""
    pass

class StatisticsFile:
    def __init__(self, uuid: str, world_name: str) -> None:
        self.uuid = uuid
        self.file_name = f"{self.uuid}.json".strip()
        self.file_path = None
        self.world_name = world_name

        #File searching logic goes here
        
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
        pass



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


def trackWorld(world):
    worldsPaths = findWorlds()
    UID = "a5d5ab98-326c-4d57-8be3-dc4e7a81bd0e"
    fileName = UID + ".json"
    if world not in os.listdir(worldsPaths):
        print("World Not Found")
    else:
        path = worldsPaths + world
        filePath = findFiles(fileName,path)
        print(filePath[0])

def trackMostRecent():
    worldsPaths = findWorlds()
    worlds = os.listdir(worldsPaths)
    #search for different worlds and save the path to the directory
    #that the worlds are held
    #get the name of the worlds
    print(worldsPaths)
    print(worlds)

    #start at users file for file search
    UID = "a5d5ab98-326c-4d57-8be3-dc4e7a81bd0e"

    fileName = UID + ".json"
    # get the full path to the file
    fullFilePaths = findFiles(fileName, worldsPaths)
    mostRecentFile = fullFilePaths[0]


    for files in fullFilePaths:
        if os.path.getmtime(files) > os.path.getmtime(mostRecentFile):
            mostRecentFile = files

    print(mostRecentFile)



#System tray icon stuff
image = Image.open("img/Minetraxbackground.png")

queries = [
    'Settings',
    'Track World',
    'Track most recent world',
    'Exit'
]
def after_click(icon, query):
    if str(query) == queries[0]:
        print("s")
        # icon.stop()
    elif str(query) == queries[1]:
        world = input("Enter World Name: ")
        trackWorld(world)
    elif str(query) == queries[2]:
        trackMostRecent()
    elif str(query) == queries[3]:
        icon.stop()

def setup(): # Put object definitions and other code in here
    icon = pystray.Icon("MT", image, "Minetrax", menu=pystray.Menu(
    pystray.MenuItem(queries[0], after_click),
    pystray.MenuItem(queries[1], after_click),
    pystray.MenuItem(queries[2], after_click),
    pystray.MenuItem(queries[3], after_click)))
    icon.run()

setup()

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


           





