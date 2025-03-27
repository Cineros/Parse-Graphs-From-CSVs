from plotly.subplots import make_subplots #Changing from plotly express to get better subplots.
import plotly.graph_objects as go
import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
from variables import color_palette

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Player Performance Dashboard", style={'textAlign': 'center', 'color': 'white'}),
    dcc.Dropdown(
        id='graph-selector',
        options=[
            {'label': 'Damage', 'value': 'Damage'},
            {'label': 'Healing', 'value': 'Healing'}
        ],
        value='Damage',  # default value
        clearable=False,
        style={'width': '200px', 'marginBottom': '20px'}
    ),
    dcc.Graph(id='graph-output')
    
], style={'minHeight': '100vh','backgroundColor': '#1c1f24','padding': '30px'})

@app.callback(
    Output('graph-output', 'figure'),
    Input('graph-selector', 'value')
)
def update_graph(selected_value):
    if selected_value == 'Damage':
        return make_plots(get_player_dataframes("Damage"), "Damage")
    else:
        return make_plots(get_player_dataframes("Healing"), "Healing")



def get_player_dataframes(option):
    print("Current working directory:", os.getcwd())
    print("Available files/folders:")
    print(os.listdir("Parse-Graphs-From-CSVs"))
    if option == "Damage":
        total_player_data_damage = {} #moved to make local.
        player_path = r"Parse-Graphs-From-CSVs/Player Damage CSVs"
        for file in os.listdir(player_path): #Essentially it iterates over all the player CSVs it created and makes a graph using the various data points in it.
            if file.endswith(".csv"):
                file_path = os.path.join(player_path, file)

                df = pd.read_csv(file_path)
                #print(df)
                if "Name" not in df.columns or "Parse %" not in df.columns or "DPS" not in df.columns:
                    #print(f"Skipping {file}: Missing required columns.")
                    continue

                df = df.dropna(subset=["Parse %", "DPS"])

                if len(df) < 2:
                    #print(f"Skipping {file}: Not enough data points.")
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
        total_player_data_healing = {}
        player_path = r"Parse-Graphs-From-CSVs/Player Healing CSVs"
        for file in os.listdir(player_path): #Essentially it iterates over all the player CSVs it created and makes a graph using the various data points in it.
            if file.endswith(".csv"):
                file_path = os.path.join(player_path, file)

                df = pd.read_csv(file_path)
                #print(df)
                if "Name" not in df.columns or "Parse %" not in df.columns or "HPS" not in df.columns:
                    #print(f"Skipping {file}: Missing required columns.")
                    continue

                df = df.dropna(subset=["Parse %", "HPS"])

                if len(df) < 2:
                    #print(f"Skipping {file}: Not enough data points.")
                    continue

                df["HPS"] = df["HPS"].astype(str).str.replace(",", "").astype(float)
                if df["HPS"].mean() < 700000:
                    #print(f"Skipping {file}: Player is not a healer.")
                    continue


                parse_percent = df["Parse %"]
                ilvl_values = df["Ilvl"]
                ilvl_percent = df["Ilvl %"]
                hps_values = df["HPS"]
                player_name = df["Name"].iloc[0]
                total_player_data_healing[player_name] = [parse_percent, hps_values, ilvl_percent, ilvl_values]
        return(total_player_data_healing)





def make_plots(player_df_dict, option):
    if option == "Damage":
        Parse_percent = 0 #These are a terrible version of an alias
        DPS = 1
        Ilvl_Percent = 2
        Ilvl = 3
        y_axis = list(range(0,100))
        color_ref = 0
        fig = make_subplots(rows=2, cols=2, start_cell="bottom-left", subplot_titles=("Parse %","Damage Per Second","Ilvl %", "Ilvl"))
        for entry in player_df_dict:
            df = player_df_dict[entry]
            #print(df[1])
            fig.add_trace(go.Scatter(name=entry, y=df[Parse_percent], x=(y_axis), legendgroup=entry, line=dict(color=color_palette[color_ref])), row=1, col=1)
            fig.add_trace(go.Scatter(name=entry, y=df[DPS], legendgroup=entry, showlegend=False, line=dict(color=color_palette[color_ref])), row=1, col=2)
            fig.add_trace(go.Scatter(name=entry, y=df[Ilvl_Percent], legendgroup=entry, showlegend=False, line=dict(color=color_palette[color_ref])), row=2, col=1)
            fig.add_trace(go.Scatter(name=entry, y=df[Ilvl], legendgroup=entry, showlegend=False, line=dict(color=color_palette[color_ref])), row=2, col=2)
            color_ref += 1

        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

        fig.update_layout(legend_title_text='Players',height=1150, width=2700, template="plotly_dark")
        return(fig)
    elif option == "Healing":
        Parse_percent = 0 #These are a terrible version of an alias
        HPS = 1
        Ilvl_Percent = 2
        Ilvl = 3
        y_axis = list(range(0,100))
        color_ref = 0
        fig = make_subplots(rows=2, cols=2, start_cell="bottom-left", subplot_titles=("Parse %","Healing Per Second","Ilvl %", "Ilvl"))
        for entry in player_df_dict:
            df = player_df_dict[entry]
            #print(df[1])
            fig.add_trace(go.Scatter(name=entry, y=df[Parse_percent], x=(y_axis), legendgroup=entry, line=dict(color=color_palette[color_ref])), row=1, col=1)
            fig.add_trace(go.Scatter(name=entry, y=df[HPS], legendgroup=entry, showlegend=False, line=dict(color=color_palette[color_ref])), row=1, col=2)
            fig.add_trace(go.Scatter(name=entry, y=df[Ilvl_Percent], legendgroup=entry, showlegend=False, line=dict(color=color_palette[color_ref])), row=2, col=1)
            fig.add_trace(go.Scatter(name=entry, y=df[Ilvl], legendgroup=entry, showlegend=False, line=dict(color=color_palette[color_ref])), row=2, col=2)
            color_ref += 1

        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))

        fig.update_layout(legend_title_text='Players',height=1150, width=2700, template="plotly_dark")
        return(fig)


#get_player_dataframes("Damage")

#make_plots(get_player_dataframes("Damage"))

#Todo: Implement Dash to turn plotly graphs into an application.

if __name__ == "__main__":
    app.run_server(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8050))  # use platform-assigned port
    )