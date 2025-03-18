import pandas as pd
import os
import matplotlib.pyplot as plt
from variables import *

def make_graphs(option): #This function performs matplotlib magic to create graphs from various data sets.
    if option == "damage":

        player_path = r"C:\Parse-Graphs-From-CSVs\Player Damage CSVs"
        graph_dir = r"C:\Parse-Graphs-From-CSVs\DPS_Graphs"
        os.makedirs(graph_dir, exist_ok=True)
        for file in os.listdir(player_path): #Essentially it iterates over all the player CSVs it created and makes a graph using the various data points in it.
            if file.endswith(".csv"):
                file_path = os.path.join(player_path, file)

                df = pd.read_csv(file_path)
                if "Name" not in df.columns or "Parse %" not in df.columns or "DPS" not in df.columns:
                    print(f"Skipping {file}: Missing required columns.")
                    continue

                df = df.dropna(subset=["Parse %", "DPS"])

                if len(df) < 2:
                    print(f"Skipping {file}: Not enough data points.")
                    continue
                #I *might* want to add an if statement here to filter out low data points.

                df["DPS"] = df["DPS"].astype(str).str.replace(",", "").astype(float)

                x_axis = range(1, len(df) + 1)
                parse_percent = df["Parse %"]
                ilvl_values = df["Ilvl"]
                ilvl_percent = df["Ilvl %"]
                dps_values = df["DPS"]
                player_name = df["Name"].iloc[0]

                player_graph_dir = os.path.join(graph_dir, player_name)
                os.makedirs(player_graph_dir, exist_ok=True)


                fig, ax1 = plt.subplots(figsize=(8, 5))
                ax1.set_xlabel("Week Number (Ordered)")
                ax1.set_ylabel("Parse % / Ilvl % (0-100)", color="blue")
                ax1.plot(x_axis, parse_percent, marker='o', linestyle="-", color="blue", label="Parse %")
                ax1.plot(x_axis, ilvl_percent, marker='x', linestyle="--", color="green", label="Ilvl %")
                ax1.set_ylim(0, 100)
                ax1.legend(loc="upper left")

                ax2 = ax1.twinx()
                ax2.set_ylabel("Ilvl", color="red")
                ax2.plot(x_axis, ilvl_values, marker="s", linestyle="-", color="red", label="Ilvl")
                ax2.legend(loc="upper right")

                plt.title(f"Parse % / Ilvl Performance of {player_name}")
                parse_graph_path = os.path.join(player_graph_dir, f"{player_name}_parse_ilvl.png")
                plt.savefig(parse_graph_path, dpi=300)
                plt.close()
                print(f"Parse % and Ilvl graph saved: {parse_graph_path}")



                plt.figure(figsize=(8, 5))
                plt.plot(x_axis, dps_values, marker='s', linestyle='--', color='red', label="DPS")
                plt.xlabel("Week Number (Ordered)")
                plt.ylabel("DPS")
                plt.title(f"DPS Performance of {player_name}")
                plt.legend()
                dps_graph_path = os.path.join(player_graph_dir, f"{player_name}_dps.png")
                plt.savefig(dps_graph_path, dpi=300)
                plt.close()
                print(f"DPS graph saved: {dps_graph_path}")
    else:

        player_path = r"C:\Parse-Graphs-From-CSVs\Player Healing CSVs"
        graph_dir = r"C:\Parse-Graphs-From-CSVs\HPS_Graphs"
        os.makedirs(graph_dir, exist_ok=True)
        for file in os.listdir(player_path):
            if file.endswith(".csv"):
                file_path = os.path.join(player_path, file)

                df = pd.read_csv(file_path)

                if "Name" not in df.columns or "Parse %" not in df.columns or "HPS" not in df.columns:
                    print(f"Skipping {file}: Missing required columns.")
                    continue

                df = df.dropna(subset=["Parse %", "HPS"])

                if len(df) < 2:
                    print(f"Skipping {file}: Not enough data points.")
                    continue



                df["HPS"] = df["HPS"].astype(str).str.replace(",", "").astype(float)

                if df["HPS"].mean() < 700000:
                    print(f"Skipping {file}: Player is not a healer.")
                    continue

                x_axis = range(1, len(df) + 1)
                parse_percent = df["Parse %"]
                ilvl_values = df["Ilvl"]
                ilvl_percent = df["Ilvl %"]
                hps_values = df["HPS"]
                player_name = df["Name"].iloc[0]

                player_graph_dir = os.path.join(graph_dir, player_name)
                os.makedirs(player_graph_dir, exist_ok=True)

                fig, ax1 = plt.subplots(figsize=(8, 5))
                ax1.set_xlabel("Week Number (Ordered)")
                ax1.set_ylabel("Parse % / Ilvl % (0-100)", color="blue")
                ax1.plot(x_axis, parse_percent, marker='o', linestyle="-", color="blue", label="Parse %")
                ax1.plot(x_axis, ilvl_percent, marker='x', linestyle="--", color="green", label="Ilvl %")
                ax1.set_ylim(0, 100)
                ax1.legend(loc="upper left")

                ax2 = ax1.twinx()
                ax2.set_ylabel("Ilvl", color="red")
                ax2.plot(x_axis, ilvl_values, marker="s", linestyle="-", color="red", label="Ilvl")
                ax2.legend(loc="upper right")

                plt.title(f"Parse % / Ilvl Performance of {player_name}")
                parse_graph_path = os.path.join(player_graph_dir, f"{player_name}_parse_ilvl.png")
                plt.savefig(parse_graph_path, dpi=300)
                plt.close()
                print(f"Parse % and Ilvl graph saved: {parse_graph_path}")

                plt.figure(figsize=(8, 5))
                plt.plot(x_axis, hps_values, marker='s', linestyle='--', color='red', label="HPS")
                plt.xlabel("Week Number (Ordered)")
                plt.ylabel("HPS")
                plt.title(f"HPS Performance of {player_name}")
                plt.legend()
                dps_graph_path = os.path.join(player_graph_dir, f"{player_name}_hps.png")
                plt.savefig(dps_graph_path, dpi=300)
                plt.close()
                print(f"HPS graph saved: {dps_graph_path}")


def plot_guild_graph(option): #This was more of if I could and not if it would be useful to know. Most of this I found online, I only changed it to fit this purpose. 
    if option == "Damage":
        data_total = []
        graph_col = ["Parse %", "Name", "DPS", "Ilvl"]
        week_num = 0
        for file in os.listdir(damage_path):
            file_path = os.path.join(damage_path, file)
            if os.path.isdir(file_path) or not file.endswith(".csv"):
                continue

            week_num += 1
            df = pd.read_csv(file_path)

            if not all(col in df.columns for col in graph_col):
                print(f"Skipping {file}: Missing required columns.")
                continue
            df["Week"] = week_num
            data_total.append(df)

        if not data_total:
            print("No valid data found.")
            return
        
        combined_df = pd.concat(data_total, ignore_index=True)
        combined_df["DPS"] = combined_df["DPS"].astype(str).str.replace(",", "").astype(float)
        combined_df["Ilvl"] = pd.to_numeric(combined_df["Ilvl"], errors="coerce")

        player_counts = combined_df["Name"].value_counts()
        valid_players = player_counts[player_counts > 1].index
        combined_df = combined_df[combined_df["Name"].isin(valid_players)]



        players = combined_df["Name"].unique()
        colors = plt.cm.get_cmap("rainbow", len(players)) 


        plt.figure(figsize=(18, len(df)))
        for i, player in enumerate(players):
            player_data = combined_df[combined_df["Name"] == player]
            plt.plot(
                player_data["Week"], 
                player_data["DPS"], 
                label=player, 
                color=colors(i),  
                marker="o", linestyle="-", linewidth=2.5, alpha=0.9
        )
        plt.xlabel("Week Number")
        plt.ylabel("DPS")
        plt.title("DPS Progression Over Weeks")
        plt.legend(title="Players", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        graph_path = r"C:\Parse-Graphs-From-CSVs\Guild Graphs"
        os.makedirs(graph_path, exist_ok=True)
        dps_graph_path = os.path.join(graph_path, "week_vs_dps.png")
        plt.savefig(dps_graph_path, dpi=300, bbox_inches="tight")
        plt.show()

    elif option == "Healing":
        data_total = []
        graph_col = ["Parse %", "Name", "HPS", "Ilvl"]
        week_num = 0
        for file in os.listdir(heal_path):
            file_path = os.path.join(heal_path, file)
            if os.path.isdir(file_path) or not file.endswith(".csv"):
                continue

            week_num += 1
            df = pd.read_csv(file_path)

            if not all(col in df.columns for col in graph_col):
                print(f"Skipping {file}: Missing required columns.")
                continue
            df["Week"] = week_num
            data_total.append(df)

        if not data_total:
            print("No valid data found.")
            return
        
        combined_df = pd.concat(data_total, ignore_index=True)
        combined_df["HPS"] = combined_df["HPS"].astype(str).str.replace(",", "").astype(float)
        combined_df["Ilvl"] = pd.to_numeric(combined_df["Ilvl"], errors="coerce")
        combined_df = combined_df[(combined_df["HPS"] >= 300000)]

        player_counts = combined_df["Name"].value_counts()
        valid_players = player_counts[player_counts > 1].index
        combined_df = combined_df[combined_df["Name"].isin(valid_players)]



        players = combined_df["Name"].unique()
        colors = plt.cm.get_cmap("rainbow", len(players)) 


        plt.figure(figsize=(18, len(df)))
        for i, player in enumerate(players):
            player_data = combined_df[combined_df["Name"] == player]
            plt.plot(
                player_data["Week"], 
                player_data["HPS"], 
                label=player, 
                color=colors(i),  
                marker="o", linestyle="-", linewidth=2.5, alpha=0.9
        )
        plt.xlabel("Week Number")
        plt.ylabel("HPS")
        plt.title("HPS Progression Over Weeks")
        plt.legend(title="Players", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        graph_path = r"C:\Parse-Graphs-From-CSVs\Guild Graphs"
        os.makedirs(graph_path, exist_ok=True)
        dps_graph_path = os.path.join(graph_path, "week_vs_dps.png")
        plt.savefig(dps_graph_path, dpi=300, bbox_inches="tight")
        plt.show()
    else:
        raise Exception ("Option is invaild bailing out. ")

