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
                #print(df)
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



def make_plots(player_df_dict):
    Parse_percent = 0 #These are a terrible version of an alias
    DPS = 1
    Ilvl_Percent = 2
    Ilvl = 3
    y_axis = list(range(0,100))
    fig = make_subplots(rows=2, cols=2, start_cell="bottom-left", subplot_titles=("Parse %","Damage Per Second","Ilvl %", "Ilvl"))
    for entry in player_df_dict:
        df = player_df_dict[entry]
        #print(df[1])
        fig.add_trace(go.Scatter(name=entry, y=df[Parse_percent], x=(y_axis), legendgroup=entry), row=1, col=1)
        fig.add_trace(go.Scatter(y=df[DPS], legendgroup=entry, showlegend=False), row=1, col=2)
        fig.add_trace(go.Scatter(y=df[Ilvl_Percent], legendgroup=entry, showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(y=df[Ilvl], legendgroup=entry, showlegend=False), row=2, col=2)
    
    fig.update_layout(legend_title_text='Players')
    fig.show()


#get_player_dataframes("Damage")

make_plots(get_player_dataframes("Damage"))

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