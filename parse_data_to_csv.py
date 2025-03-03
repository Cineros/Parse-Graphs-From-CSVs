import os
import csv 
from create_graphs_from_csv import *


damage_path = r"C:\Parse-Graphs-From-CSVs\Damage CSVs"
heal_path = r"C:\Parse-Graphs-From-CSVs\Healing CSVs"
player_path = r"C:\Parse-Graphs-From-CSVs\Player CSVs"
field_names = ["Parse %","Name","Amount","Ilvl","Ilvl %","Active","DPS",""]
player_names = {} #Player dict


def export_to_csv(player_name, data_list): #Creates new CSV files with the player name as the title.
    try:
        new_path = os.path.join(player_path)
        #if not os.path.exists(new_path):
        #    os.mkdir(new_path)

        if len(data_list) == 0:
            print("Data list empty!")
            return

        new_csv = os.path.join(new_path, f'{player_name}.csv')

        with open(new_csv, 'w', newline='', encoding='utf-8') as file:
            write = csv.writer(file)
            writer = csv.DictWriter(file, fieldnames=field_names)
            write.writerow(field_names)
            for item in data_list:
                print(item)
                writer.writerow(item)

        print(f"CSV file: {new_csv} created.")

    except Exception as e:
        print("Failed to create file", e)
    

def fill_damage_dict():
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
                
def main():
    fill_damage_dict()
    for player in player_names:
        #print(player, player_names[player])
        export_to_csv(player, player_names[player])
    make_graphs()


main()