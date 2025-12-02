import pandas as pd
from plotters.simple_barplot import simple_barplot


def yearwise_listening_minutes(df: pd.DataFrame):
    copy = df.copy(True)
    copy["ts"] = copy["ts"].dt.year
    yearwise_playtime = copy.groupby("ts")["ms_played"].sum() / 60000
    simple_barplot(yearwise_playtime, "Yearwise playtime in minutes", "Year", "Minutes Played")
