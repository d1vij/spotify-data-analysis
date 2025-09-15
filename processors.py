# all the functions to process the df accordingly and plot them
from typing import cast
from datetime import datetime

import pandas as pd
from pandas import DataFrame

from utils.plots import Plots
from utils.filters import Filters
from utils.series_textwrap import index_wrap
from utils.fig_to_uri import get_uri


def top_artists_by_playtime(df: DataFrame):
    copy = df.copy(True)
    grouped_by_artist_name = copy.groupby(copy["master_metadata_album_artist_name"])
    time_listend = grouped_by_artist_name["ms_played"].sum()
    time_listend = time_listend[time_listend != 0]
    time_listend.sort_values(ascending=False, inplace=True)
    time_listend_mins = time_listend.div(6e4)
    time_listend_mins = cast(pd.Series, Filters.rows_gt(1, time_listend_mins))
    index_wrap(time_listend_mins, 10)
    Plots.plot_squarify(time_listend_mins[:50], "Top 50 played artists by listening minutes")

def most_played_tracks(df: DataFrame):
    # Most played tracks
    most_played_tracks = df.groupby(df["master_metadata_track_name"])["master_metadata_track_name"].count()
    most_played_tracks.sort_values(ascending=False, inplace=True)
    index_wrap(most_played_tracks, 10)
    Plots.plot_squarify(most_played_tracks[:100], "100 Most played tracks")

def yearwise_playtime(df: DataFrame):
    # yearwise listening minutes
    with_dates = df.copy(True)
    with_dates["ts"] = with_dates["ts"].apply(lambda ts: datetime.strftime(ts, "%Y"))
    grouped_by_ts = with_dates.groupby("ts")
    total_playtime = grouped_by_ts["ms_played"].sum()
    total_playtime = total_playtime.div(6e4)
    Plots.simple_barplot(total_playtime, "Yearwise playtime in minutes", "Year", "Minutes Played")



# TODO: Look into this
def analysis_per_artist(frame: pd.DataFrame, artist:str):
    if(artist not in frame["master_metadata_album_artist_name"].values):
        raise ValueError(f"Artist {artist} is not in data")

    artist_frame = frame[frame["master_metadata_album_artist_name"] == artist].copy(True)
    # grouped = artist_frame.groupby("master_metadata_album_artist_name")
    # changing ts to year
    artist_frame["year"] = artist_frame["ts"].apply(lambda ts: datetime.strftime(ts, "%Y"))

    # Top 50 played tracks
    played_track_count = (artist_frame
                          .groupby("master_metadata_track_name")
                          .size()
                          .sort_values(ascending=False))
    index_wrap(played_track_count, 12)
    Plots.plot_squarify(played_track_count[:50],f"Fifty most played tracks by {artist}")
    
    # Year wise play time
    yearwise_playtime = (artist_frame
                         .groupby("year")
                         .size())
    Plots.simple_barplot(yearwise_playtime, f"Tracks played in a particular year by {artist}", "Year", "Play count")
    
    
    daily_tracks_uri = get_uri(Plots.daily_tracks_graph(artist_frame))
    track_playtime_kde_uri = get_uri(Plots.track_playtime_kde_dist(artist_frame))
    daily_listening_activity_uri = get_uri(Plots.daily_listening_activity(artist_frame))