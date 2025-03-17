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
                        print(f"Row Data: {row}")
                        name = row["Name"]
                        if not name:
                            print(f"Skipping row, missing 'Name': {row}")
                            continue
                        if name not in player_names:
                            player_names[name] = []
                            #player_names[name].append(damage_field_names) #I might need the field names to traverse columns later.
                        if row != reader.fieldnames:
                            player_names[name].append(row)
        print("Finished averaging bad logs to dict.")
        #print(player_names) #From this I know it generates a list of dicts that all have fields Ill need to wade through to average the data.
    else:
        if option == "Healing":
            damage_dir = os.path.join(bad_logs_path, "Healing")
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
                            name = row["Name"]
                            if not name:
                                print(f"Skipping row, missing 'Name': {row}")
                                continue
                            if name not in player_names:
                                player_names[name] = []
                                #player_names[name].append(damage_field_names) #I might need the field names to traverse columns later.
                            if row != reader.fieldnames:
                                player_names[name].append(row)
            print("Finished averaging bad logs to dict.")
    return player_names

def process_player_entry(player):
    new_entry = {}
    temp_ilvl_percent = 0
    temp_dps = 0
    temp_parse_percent = 0
    #print(player)
    if len(player) < 2:
        print(f"{player[0]['Name']} doesnt have enough parses.")
        return None
    if player[0]['Name'] == "Rolling Rubbish":
        return None
    
    for log in player:
        temp_parse_percent += int(log['Parse %'])
        temp_ilvl_percent += int(log['Ilvl %'])
        temp_dps += int((log['DPS'][:len(log['DPS'])-2]).replace(',',''))
        
    temp_parse_percent = str(int(temp_parse_percent/len(player)))
    temp_ilvl_percent = str(int(temp_ilvl_percent/len(player)))
    temp_dps = str(int(temp_dps/len(player)))
    new_entry['Parse %'] = temp_parse_percent
    new_entry['Name'] = player[0]['Name']
    new_entry['Amount'] = player[0]['Amount']
    new_entry['Ilvl'] = player[len(player)-1]['Ilvl']
    new_entry['Ilvl %'] = temp_ilvl_percent
    new_entry["Acitve"] = '90'
    new_entry['DPS'] = temp_dps
    new_entry[''] = ''

    return new_entry
    

def average_player_dict():
    player_dict = parse_bad_logs("Damage")
    for player in player_dict:
        player_dict[player] = process_player_entry(player_dict[player])
        print(player_dict[player])


average_player_dict()
