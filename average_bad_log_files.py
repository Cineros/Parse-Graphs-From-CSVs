import os

bad_logs_path = r"C:\Parse-Graphs-From-CSVs\Bad_Logs"
export_path = r"C:\Parse-Graphs-From-CSVs"
player_list = []
from variables import *


def average_bad_logs():
    damage_dir = os.path.join(bad_logs_path, "Damage")
    export_dir = os.path.join(export_path, "Damage CSVs")
    for file in os.listdir(damage_dir):
        pass

