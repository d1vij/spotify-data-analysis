from os import path
from typing import cast


import pandas as pd
import matplotlib.pyplot as plt

from utils.filters import Filters
from utils.series_textwrap import index_wrap

from utils.plot_sources.plotters.plot_squarify import plot_squarify
from utils.plot_sources.plotters.simple_barplot import simple_barplot

from utils.printers import Printer


def top_n_artists_by_playtime(df: pd.DataFrame, n: int):
    # Top artists by playtime
    copy = df.copy(True)
    grouped_by_artist_name = copy.groupby(copy["master_metadata_album_artist_name"])
    time_listend = grouped_by_artist_name["ms_played"].sum()
    time_listend = time_listend[time_listend != 0]
    time_listend.sort_values(ascending=False, inplace=True)
    time_listend_mins = time_listend.div(6e4)
    time_listend_mins = cast(pd.Series, Filters.rows_gt(1, time_listend_mins))

    Printer.cyan_underline(
        f"Out of {len(time_listend_mins)} artists, the top {n} artists based on track playtimes are"
    )
    for artist, playtime in time_listend_mins[:n].items():
        print(f"{artist} - {playtime / 60:.1f} hours")

    # Plotting
    index_wrap(time_listend_mins, 10)
    plot_squarify(time_listend_mins[:n], f"Top {n} played artists by playtime")
    plt.show()


def top_n_tracks_by_playcount(df: pd.DataFrame, n: int):
    most_played_tracks = df.groupby(df["master_metadata_track_name"])[
        "master_metadata_track_name"
    ].count()
    most_played_tracks.sort_values(ascending=False, inplace=True)

    Printer.cyan_underline(
        f"Out of {len(most_played_tracks)} unique tracks, the top {n} played tracks are"
    )
    for trackname, playcount in most_played_tracks[:n].items():
        print(f"{trackname} - {playcount} plays")

    index_wrap(most_played_tracks, 10)
    plot_squarify(most_played_tracks[:n], f"{n} Most played tracks")
    plt.show()


def top_n_albums_by_playcount(df: pd.DataFrame, n: int):
    most_played_albums = df.groupby(df["master_metadata_album_album_name"])[
        "master_metadata_album_album_name"
    ].count()
    most_played_albums.sort_values(ascending=False, inplace=True)

    # Number of tracks in each album
    track_count = df.groupby(df["master_metadata_album_album_name"])[
        "master_metadata_track_name"
    ].nunique()
    # NOTE: This ^ might be wrong

    # Normalizing the album playcounts
    # Normalized counts = total playcount / number of tracks in album
    most_played_albums = most_played_albums.div(track_count).round(0)

    most_played_albums.sort_values(inplace=True, ascending=False)

    Printer.cyan_underline(
        f"Out of {len(most_played_albums)} unique albums, the top {n} played albums based on approximate playcounts are"
    )
    for albumname, playcount in most_played_albums[:n].items():
        print(f"{albumname} - {playcount} plays")

    index_wrap(most_played_albums, 10)
    plot_squarify(most_played_albums[:n], f"{n} Most played albums")


def top_n_genres(df: pd.DataFrame, n: int):
    artists_df = pd.read_csv(path.abspath("./ext_data/global_music_artists.csv"))

    unique_artists_names = df["master_metadata_album_artist_name"].unique()
    unique_artists_df = artists_df.loc[
        artists_df["artist_name"].isin(unique_artists_names)
    ]

    artist_countries_ser = unique_artists_df["country"].value_counts()

    # Genres stuff
    unique_genres = {}
    for genre_list in unique_artists_df["artist_genre"]:
        for genre in genre_list.split(","):
            genre = genre.strip()
            unique_genres[genre] = unique_genres.get(genre, 0) + 1

    # Genre of artist
    unique_genres_ser = pd.Series(unique_genres)
    print(unique_genres_ser.sort_values(ascending=False))


def top_analysis(df: pd.DataFrame):
    top_n_artists_by_playtime(df, 50)
    top_n_tracks_by_playcount(df, 50)
    top_n_albums_by_playcount(df, 50)
