import os
import csv 
from create_graphs_from_csv import *


damage_path = r"C:\Parse-Graphs-From-CSVs\Damage CSVs"
heal_path = r"C:\Parse-Graphs-From-CSVs\Healing CSVs"
player_damage_path = r"C:\Parse-Graphs-From-CSVs\Player Damage CSVs"
player_healing_path = r"C:\Parse-Graphs-From-CSVs\Player Healing CSVs"
damage_field_names = ["Parse %","Name","Amount","Ilvl","Ilvl %","Active","DPS",""]
healing_field_names = ["Parse %","Name","Amount","Overheal","Ilvl","Ilvl %","Active","HPS",""] #These are the fields from the CSV files
player_names = {} #Player dictionary


def export_to_csv(player_name, data_list, option): #Creates new CSV files with the player name as the title.
    try:
        if option == "damage":
            local_path = os.path.join(player_damage_path) #Replaced "new_path" with "local_path" for clarity.
            if len(data_list) == 0:
                print("Data list empty!")
                return
            
            new_csv = os.path.join(local_path, f'{player_name}.csv')
            with open(new_csv, 'w', newline='', encoding='utf-8') as file:
                write = csv.writer(file)
                writer = csv.DictWriter(file, fieldnames=damage_field_names)
                write.writerow(damage_field_names)
                for item in data_list:
                    print(item)
                    writer.writerow(item)
            print(f"CSV file: {new_csv} created.")

        #if not os.path.exists(local_path): 
        #    os.mkdir(local_path)
        else:
            local_path = os.path.join(player_healing_path)
            if len(data_list) == 0:
                print("Data list empty!")
                return
            
            new_csv = os.path.join(local_path, f'{player_name}.csv')
            with open(new_csv, 'w', newline='', encoding='utf-8') as file:
                write = csv.writer(file)
                writer = csv.DictWriter(file, fieldnames=healing_field_names)
                write.writerow(healing_field_names)
                for item in data_list:
                    print(item)
                    writer.writerow(item)
            print(f"CSV file: {new_csv} created.")




        

    except Exception as e:
        print("Failed to create file", e)
    

def fill_damage_dict(): #Parses a directory of CSV files and seperates the entries into a dictionary with the player names as keys and their row in the CSV as its values.
    for filename in os.listdir(damage_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(damage_path, filename)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                print(f"Processing file: {csvfile}")
                if not reader.fieldnames:
                    print(f"Skipping {csvfile} - no header")
                    continue
                print(f"CSV Headers: {reader.fieldnames}")
                for row in reader:
                    print(f"Row Data: {row}")
                    name = row["Name"]
                    if not name:
                        print(f"Skipping row, missing 'Name': {row}")
                        continue
                    if name not in player_names: #Do I need a dict with the player names in it? Yes I need to make a name -> list relationship.
                        player_names[name] = []
                    if row != reader.fieldnames:
                        player_names[name].append(row)
                    #for item in player_names[name]:
                    #    print(item)
                
def fill_healing_dict(): #Parses a directory of CSV files and seperates the entries into a dictionary with the player names as keys and their row in the CSV as its values.
    for filename in os.listdir(heal_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(heal_path, filename)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                print(f"Processing file: {csvfile}")
                if not reader.fieldnames:
                    print(f"Skipping {csvfile} - no header")
                    continue
                print(f"CSV Headers: {reader.fieldnames}")
                for row in reader:
                    print(f"Row Data: {row}")
                    name = row["Name"]
                    if not name:
                        print(f"Skipping row, missing 'Name': {row}")
                        continue
                    if name not in player_names: 
                        player_names[name] = []
                    if row != reader.fieldnames:
                        player_names[name].append(row)
                    #for item in player_names[name]:
                    #    print(item)
                
def main():
    fill_damage_dict()
    for player in player_names:
        #print(player, player_names[player])
        export_to_csv(player, player_names[player], "damage")
    make_graphs("damage")
    player_names.clear() #Clear the player dictionary to prepare for making the healing graphs.
    fill_healing_dict()
    for player in player_names:
        #print(player, player_names[player])
        export_to_csv(player, player_names[player], "healing")
    make_graphs("healing")


main()