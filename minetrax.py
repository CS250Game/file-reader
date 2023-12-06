import json
import os
#from sqlite3 import connect
import requests
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
        #dsn = f"postgres://{username}:{password}@{host}:{port}/{database}"
        #self.conn = psycopg2.connect(dsn=dsn)
        pass

    def push(self, stat_file: StatisticsFile):
        stats = stat_file.file_path
        
        #load the json file data into a dict
        with open(stats) as json_file:
            stats_data = json.load(json_file)

        #clean the data of stats we dont want and push the stats we want to the database
        stats = stats_data['stats']['minecraft:custom']
        if 'minecraft:killed' in stats_data['stats']:
            kill_data = stats_data['stats']['minecraft:killed']
            stats.update(kill_data)

        #Temporary for testing
        stats_to_exclude = {}#{"minecraft:interact_with_furnace",
        # "minecraft:mob_kills",
        # "minecraft:interact_with_crafting_table",
        # "minecraft:drop",
        # "minecraft:open_chest",
        # "minecraft:play_time",
        # "minecraft:sneak_time",
        # "minecraft:jump"
        # }

        world_id = stat_file.world_name

        for key in stats_to_exclude:
            if key in stats:
                del stats[key]

        to_push = {}
        for key, value in stats.items():
            to_push['key'] = value

        requests.post("http://127.0.0.1:5000/api/addworld", {UUID, stat_file.world_name, to_push}, headers={'content-type': 'application/json'})

    #insert into user table
    def Push_Username(self, UUID, username):
        cursor = self.conn.cursor()
        cursor.execute(f"select username from mcuser where(uuid='{UUID}');")
        results = cursor.fetchall()

        #if the world does not exist in the db create this 
        if len(results) == 0:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO mcuser(uuid,username) VALUES ('{UUID}','{username}');")
            self.conn.commit()

minetraxDatabase = Database('postgres', '1234', 'localhost',5432)
#minetraxDatabase.testPush()

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
           worldsPaths = root + "\\.minecraft\\saves\\"
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
        #create a statistics file object
        newStatFileToPush = StatisticsFile(UUID, world, filePath[0])
        minetraxDatabase.push(newStatFileToPush)
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


    for name in worlds:
        if name in mostRecentFile:
            mostRecentWorldName = name

    statFileToPush = StatisticsFile(UUID, mostRecentWorldName ,mostRecentFile)

    minetraxDatabase.push(statFileToPush)
    #create a statistics file object

    #next push to DB


global UUID
global username

username = ""
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
        username = input("Enter Username: ")
        minetraxDatabase.Push_Username(UUID, username)
        # icon.stop()
    elif str(query) == queries[1]:
        if UUID == "":
            UUID = input("Enter UUID: ")
            username = input("Enter Username: ")
            minetraxDatabase.Push_Username(UUID, username)
        world = input("Enter World Name: ")
        trackWorld(world,UUID)
    elif str(query) == queries[2]:
        if UUID == "":
            UUID = input("Enter UUID: ")
            username = input("Enter Username: ")
            minetraxDatabase.Push_Username(UUID, username)
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