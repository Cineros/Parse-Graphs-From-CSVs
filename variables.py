#Common Variables

damage_field_names = ["Parse %","Name","Amount","Ilvl","Ilvl %","Active","DPS",""]
healing_field_names = ["Parse %","Name","Amount","Overheal","Ilvl","Ilvl %","Active","HPS",""] #These are the fields from the CSV files


damage_path = r"C:\Parse-Graphs-From-CSVs\Damage CSVs"
heal_path = r"C:\Parse-Graphs-From-CSVs\Healing CSVs" #These are the locations of the complete CSV files for a given stat.


player_damage_path = r"C:\Parse-Graphs-From-CSVs\Player Damage CSVs"
player_healing_path = r"C:\Parse-Graphs-From-CSVs\Player Healing CSVs" #Updated paths after the export to CSV function runs.

damage_csv_path = r"C:\Parse-Graphs-From-CSVs\Damage CSVs"
healing_csv_path = r"C:\Parse-Graphs-From-CSVs\Healing CSVs"

bad_logs_path = r"C:\Parse-Graphs-From-CSVs\Bad_Logs"
export_path = r"C:\Parse-Graphs-From-CSVs"

#A palette of colors used across multiple graphs in this program.
color_palette = [
    "#00FF00", "#FF4500", "#1E90FF", "#FFFF00", "#FF00FF", "#00FFFF",
    "#FFA500",  "#ADFF2F", "#00CED1", "#FF6347", "#7CFC00", "#8A2BE2",
    "#00BFFF", "#32CD32", "#FFD700", "#DC143C", "#40E0D0", "#8B0000",
    "#6495ED", "#20B2AA", "#FF8C00", "#9ACD32", "#B22222", "#48D1CC",
    "#7FFF00", "#4169E1", "#00FA9A", "#E6E600", "#6A5ACD", "#00FF7F"
]