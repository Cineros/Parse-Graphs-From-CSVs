import plotly.express as px
import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output


total_player_data_damage = {}

def update_graph_data(option):
    if option == "Damage":
        player_path = r"C:\Parse-Graphs-From-CSVs\Player Damage CSVs"
        graph_dir = r"C:\Parse-Graphs-From-CSVs\DPS_Graphs"



        os.makedirs(graph_dir, exist_ok=True)
        for file in os.listdir(player_path): #Essentially it iterates over all the player CSVs it created and makes a graph using the various data points in it.
            if file.endswith(".csv"):
                file_path = os.path.join(player_path, file)

                df = pd.read_csv(file_path)
                print(df)
                if "Name" not in df.columns or "Parse %" not in df.columns or "DPS" not in df.columns:
                    print(f"Skipping {file}: Missing required columns.")
                    continue

                df = df.dropna(subset=["Parse %", "DPS"])

                if len(df) < 2:
                    print(f"Skipping {file}: Not enough data points.")
                    continue

                df["DPS"] = df["DPS"].astype(str).str.replace(",", "").astype(float)
                parse_percent = df["Parse %"]
                ilvl_values = df["Ilvl"]
                ilvl_percent = df["Ilvl %"]
                dps_values = df["DPS"]
                player_name = df["Name"].iloc[0]
                total_player_data_damage[player_name] = [parse_percent, dps_values, ilvl_percent, ilvl_values]
        #print(total_player_data_damage)


    elif option == "Healing":
        player_path = r"C:\Parse-Graphs-From-CSVs\Player Healing CSVs"
        graph_dir = r"C:\Parse-Graphs-From-CSVs\HPS_Graphs"





update_graph_data("Damage")

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Life expentancy progression of countries per continents'),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options=["Asia", "Europe", "Africa","Americas","Oceania"],
        value=["Americas", "Oceania"],
        inline=True
    ),
])


@app.callback(
    Output("graph", "figure"),
    Input("checklist", "value"))
def update_line_chart(contents):
    df = px.data.gapminder() # replace with your own data source
    mask = df.contents.isin()
    fig = px.line(df[mask],
        x="year", y="lifeExp", color='country')
    return fig


app.run(debug=True)