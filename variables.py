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
    "#025718", "#02e840", "#688038", "#d9f0aa", "#FFD700", "#000000", "#f7db05", "#665a03",
    "#aba46f", "#d6610d", "#522403", "#2e1e13", "#b06b5b", "#fcc3b6", "#ff0000", "#690303",
    "#e00d50", "#993655", "#610049", "#9f11f7", "#3d1754", "#c56dfc", "#4f00fa", "#cbb3ff",
    "#0d15ff", "#020557", "#22244d", "#282829", "#40E0D0", "#DAA520"
]