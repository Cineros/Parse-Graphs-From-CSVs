import os
import csv
import pandas as pd
from variables import *
export_dir = os.path.join(export_path, "Damage CSVs")


def parse_bad_logs(option):
    player_names = {}
    if option == "Damage":
        damage_dir = os.path.join(bad_logs_path, "Damage")

        for file in os.listdir(damage_dir):
            if file.endswith(".csv"):
                file_path = os.path.join(damage_dir, file)
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    print(f"Processing file: {csvfile}")
                    if not reader.fieldnames:
                        print(f"Skipping {csvfile} - no header")
                        continue
                    for row in reader:
                        #This for loop is nearly identical in stucture as the other ones,
                        #but instead of using it to make a graph im using it to average a number of csv files into a new one.

                        #print(f"Row Data: {row}")
                        name = row["Name"]
                        if not name:
                            print(f"Skipping row, missing 'Name': {row}")
                            continue
                        if name not in player_names:
                            player_names[name] = []
                            #player_names[name].append(damage_field_names) #I might need the field names to traverse columns later.
                        if row != reader.fieldnames:
                            player_names[name].append(row)

    return player_names


def average_player_dict():
    player_dict = parse_bad_logs("Damage")
    for player in player_dict:
        new_entry = []
        for entry in player_dict[player]:
            pass
        player_dict[player] = new_entry
    print(player_dict)


average_player_dict()
