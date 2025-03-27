from plotly.subplots import make_subplots #Changing from plotly express to get better subplots.
import plotly.graph_objects as go
import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output




def get_player_dataframes(option):
    if option == "Damage":
        total_player_data_damage = {} #moved to make local.
        player_path = r"C:\Parse-Graphs-From-CSVs\Player Damage CSVs"
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
        return(total_player_data_damage)


    elif option == "Healing":
        player_path = r"C:\Parse-Graphs-From-CSVs\Player Healing CSVs"



def make_plots():
    fig = make_subplots(rows=2, cols=2, start_cell="bottom-left")
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
              row=1, col=1)

    fig.add_trace(go.Scatter(x=[20, 30, 40], y=[50, 60, 70]),
                row=1, col=2)

    fig.add_trace(go.Scatter(x=[300, 400, 500], y=[600, 700, 800]),
                row=2, col=1)

    fig.add_trace(go.Scatter(x=[4000, 5000, 6000], y=[7000, 8000, 9000]),
                row=2, col=2)

    fig.show()


#get_player_dataframes("Damage")

make_plots()

#Todo: Implement Dash to turn plotly graphs into an application.
'''
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
'''

#app.run(debug=True)