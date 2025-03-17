import pandas as pd
import os
import matplotlib.pyplot as plt

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
                ax1.set_xlabel("Fight Number (Ordered)")
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
                plt.xlabel("Fight Number (Ordered)")
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

                if df["HPS"].mean() < 600000:
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
                ax1.set_xlabel("Fight Number (Ordered)")
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
                plt.xlabel("Fight Number (Ordered)")
                plt.ylabel("HPS")
                plt.title(f"HPS Performance of {player_name}")
                plt.legend()
                dps_graph_path = os.path.join(player_graph_dir, f"{player_name}_dps.png")
                plt.savefig(dps_graph_path, dpi=300)
                plt.close()
                print(f"HPS graph saved: {dps_graph_path}")


