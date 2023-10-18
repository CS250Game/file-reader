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


#System tray icon stuff
image = Image.open("img/Minetraxbackground.png")
queries = [
    'Settings',
    'Account',
    'Tracking world:',
    'Exit'
]
def after_click(icon, query):
    if str(query) == queries[0]:
        print("s")
        # icon.stop()
    elif str(query) == queries[1]:
        print("a")
        # icon.stop()
    elif str(query) == queries[2]:
        print("t")
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