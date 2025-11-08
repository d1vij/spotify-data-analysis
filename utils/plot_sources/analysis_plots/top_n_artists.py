from typing import cast

import matplotlib.pyplot as plt
import pandas as pd

from utils.filters import Filters
from utils.series_textwrap import index_wrap

from utils.plot_sources.plotters.plot_squarify import plot_squarify

def top_n_artists_by_playtime(df: pd.DataFrame, n: int):
    # Top artists by playtime
    copy = df.copy(True)
    grouped_by_artist_name = copy.groupby(copy["master_metadata_album_artist_name"])
    time_listend = grouped_by_artist_name["ms_played"].sum()
    time_listend = time_listend[time_listend != 0]
    time_listend.sort_values(ascending=False, inplace=True)
    time_listend_mins = time_listend.div(6e4)
    time_listend_mins = cast(pd.Series, Filters.rows_gt(1, time_listend_mins))
    index_wrap(time_listend_mins, 10)
    plot_squarify(
        time_listend_mins[:n], f"Top {n} played artists by listening minutes"
    )

def top_n_tracks_by_playcount(df: pd.DataFrame, n: int):
    most_played_tracks = df.groupby(df["master_metadata_track_name"])[
        "master_metadata_track_name"
    ].count()
    most_played_tracks.sort_values(ascending=False, inplace=True)
    index_wrap(most_played_tracks, 10)
    plot_squarify(most_played_tracks[:n], f"{n} Most played tracks")
