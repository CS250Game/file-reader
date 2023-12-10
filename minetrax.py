import json
import os
import requests
import pystray
import tkinter as tk
from PIL import Image
import asyncio
from windows_toasts import Toast, WindowsToaster, ToastDisplayImage

#pip install...
class StatsFileNotFound(Exception):
    """Base error for a statistic file that was not found."""
    pass

class StatNotFound(Exception):
    """Base error for a statistic that was not found within a stat file."""
    pass

global UUID
global username
username = ""
#a5d5ab98-326c-4d57-8be3-dc4e7a81bd0e
UUID = ""

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
    def __init__(self, api_url: str) -> None:
        self.api_url = api_url
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

        r= requests.post(f"{self.api_url}/api/addworld", json={'uuid':UUID, 'worldname':stat_file.world_name, 'data':to_push}, headers={'content-type': 'application/json'})
        print("adding world")
        print(r)

    #insert into user table
    def Push_Username(self, UUID: str, username: str):
        r = requests.post(f"{self.api_url}/api/adduser", json={'uuid':UUID, 'username':username}, headers={'content-type': 'application/json'})
        print("username")
        print(r)

minetraxDatabase = Database('http://127.0.0.1:5000')
#minetraxDatabase.testPush()

def notification(message: str, title: str = 'MineTrax', image_path: str = "img/Minetraxbackground.png"):
    toaster = WindowsToaster("MineTrax")
    new_toast = Toast()
    new_toast.text_fields = [message]
    if image_path is not None:
        new_toast.AddImage(ToastDisplayImage.fromPath(str(os.path.realpath(open(image_path).name))))
    toaster.show_toast(new_toast)

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

def prompt_info():
    UUID_text, user_text = "", ""
    def on_button_click():
        nonlocal UUID_text, user_text
        UUID_text = UUID_entry.get()
        user_text = user_entry.get()
        window.destroy()

    window = tk.Tk()
    window.title("Minetrax Setup")
    window.geometry("200x150")

    UUID_label = tk.Label(window, text="UUID")
    UUID_label.pack()

    UUID_entry = tk.Entry(window)
    UUID_entry.pack()

    user_label = tk.Label(window, text="Username")
    user_label.pack()

    user_entry = tk.Entry(window)
    user_entry.pack()

    button = tk.Button(window, text="Okay", command=on_button_click)
    button.pack()

    window.mainloop()

    return [UUID_text, user_text]

#System tray icon stuff
image = Image.open("img/Minetraxbackground.png")
queries = [
    'Setup',
    'Track World',
    'Track most recent world',
    'Exit'
]

def after_click(icon, query):
    global UUID

    if str(query) == queries[0]:
        given_uuid, given_user = prompt_info()
        if None in [given_uuid, given_user]:
            #Left fields empty
            pass
        print(given_user)
        UUID = given_uuid
        username = given_user
        try: minetraxDatabase.Push_Username(given_uuid, given_user)
        except requests.exceptions.ConnectionError as e: notification(message=f"Failed to update remote server. {e}")
        notification(message=f"Success, now tracking stats for {given_user}")
    elif str(query) == queries[1]:
        if UUID == "":
            UUID = input("Enter UUID: ")
            username = input("Enter Username: ")
            minetraxDatabase.Push_Username(UUID, username)
        world = input("Enter World Name: ")
        trackWorld(world,UUID)
        notification(message=f"Now tracking world '{world}' for user {username}")
    elif str(query) == queries[2]:
        if UUID == "":
            UUID = input("Enter UUID: ")
            username = input("Enter Username: ")
            minetraxDatabase.Push_Username(UUID, username)
        trackMostRecent(UUID)
    elif str(query) == queries[3]:
        icon.stop()

async def main():
    notification(message='MineTrax is running in the background. For setup, click the icon in the taskbar.')
    icon = pystray.Icon("MT", image, "Minetrax", menu=pystray.Menu(
    pystray.MenuItem(queries[0], after_click),
    pystray.MenuItem(queries[1], after_click),
    pystray.MenuItem(queries[2], after_click),
    pystray.MenuItem(queries[3], after_click)))
    await asyncio.to_thread(icon.run)
    print("Closing")