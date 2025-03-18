import os
import csv
#import pandas as pd #Im leaving this line here in case I better learn to use pandas.
from variables import *
export_dir = os.path.join(export_path, "Damage CSVs")


def parse_bad_logs(option): #This function looks through a number of logs and adds a players log to a dict with their name as the key.
    #Option is probably a bad var to use with how common I want to do both anyway. But if I need to seperate for any reason this will let me
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

def process_player_entry(player, option): #Here I take a given entry in the player dict and average the information I need and set a default for what I dont need. Then I reconstruct a entry using the new data and return that.
    if option == "Damage":
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
        new_entry['Parse %'] = f"{temp_parse_percent}"
        new_entry['Name'] = f"{player[0]['Name']}"
        new_entry['Amount'] = f"{player[0]['Amount']}"
        new_entry['Ilvl'] = f"{player[len(player)-1]['Ilvl']}"
        new_entry['Ilvl %'] = f"{temp_ilvl_percent}"
        new_entry["Active"] = "90"
        new_entry['DPS'] = f"{temp_dps}"
        new_entry[''] = ''

    elif option == "Healing":
        new_entry = {}
        temp_ilvl_percent = 0
        temp_parse_percent = 0
        temp_hps = 0
        #temp_overheal = 0
        if len(player) < 2:
            print(f"{player[0]['Name']} doesnt have enough parses.")
            return None
        if player[0]['Name'] == "Rolling Rubbish":
            return None
        for log in player:
            temp_parse_percent += int(log['Parse %'])
            temp_ilvl_percent += int(log['Ilvl %'])
            temp_hps += int((log['HPS'][:len(log['HPS'])-2]).replace(',',''))
            #temp_overheal += int((log['Overheal'][:len(log['Overheal'])-2]).replace('.',''))

        temp_parse_percent = str(int(temp_parse_percent/len(player)))
        temp_ilvl_percent = str(int(temp_ilvl_percent/len(player)))
        #temp_overheal = str(int(temp_overheal/len(player)))
        temp_hps = str(int(temp_hps/len(player)))
        new_entry['Parse %'] = f"{temp_parse_percent}"
        new_entry['Name'] = f"{player[0]['Name']}"
        new_entry['Amount'] = f"{player[0]['Amount']}"
        new_entry['Overheal'] = f"0"
        new_entry['Ilvl'] = f"{player[len(player)-1]['Ilvl']}"
        new_entry['Ilvl %'] = f"{temp_ilvl_percent}"
        new_entry["Active"] = "90"
        new_entry['HPS'] = f"{temp_hps}"
        new_entry[''] = ''

    #print(new_entry)
    return new_entry
    
def create_new_Log(player_dict, option): #The goal of this function is to write a new csv file with our new averaged data and export it to a location where it can be used in the other programs.
    if option == "Damage":
        local_path = os.path.join(damage_csv_path) 
        csv_name = input("Please enter the week of this log: ")
        new_csv = os.path.join(local_path, f'{csv_name}.csv')
        with open(new_csv, 'w', newline='', encoding='utf-8') as file:
            write = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer = csv.DictWriter(file, fieldnames=damage_field_names, quoting=csv.QUOTE_ALL)
            write.writerow(damage_field_names)
            for item in player_dict:
                #print(player_dict[item])
                if player_dict[item] != None:
                    writer.writerow(player_dict[item])
        print(f"CSV file: {new_csv} created.")
    elif option == "Healing":
        local_path = os.path.join(healing_csv_path) 
        csv_name = input("Please enter the week of this log: ")
        new_csv = os.path.join(local_path, f'{csv_name}.csv')
        with open(new_csv, 'w', newline='', encoding='utf-8') as file:
            write = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer = csv.DictWriter(file, fieldnames=healing_field_names, quoting=csv.QUOTE_ALL)
            write.writerow(healing_field_names)
            for item in player_dict:
                #print(player_dict[item])
                if player_dict[item] != None:
                    writer.writerow(player_dict[item])
    else:
        raise Exception ("Invaild option was given.")

def average_player_dict(option):
    if option == "Damage":
        player_dict = parse_bad_logs(option)
        for player in player_dict:
            player_dict[player] = process_player_entry(player_dict[player], option)
            #print(player_dict[player])
        create_new_Log(player_dict, option)
    elif option == "Healing":
        player_dict = parse_bad_logs(option)
        for player in player_dict:
            player_dict[player] = process_player_entry(player_dict[player], option)
            #print(player_dict[player])
        create_new_Log(player_dict, option)

def main():
    option = input("What log type would you like to parse? Healing/Damage \n")
    print(option)
    if option != "Healing" and option != "Damage":
        raise Exception ("That is not a valid option bailing out.")
    if option == "Damage":
        average_player_dict("Damage")
    elif option == "Healing":
        average_player_dict("Healing")
    else:
        print("Something went wrong!")

if __name__ == '__main__':
    main()