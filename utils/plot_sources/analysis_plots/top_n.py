from typing import cast

import chalk
import matplotlib.pyplot as plt
import pandas as pd

from utils.filters import Filters
from utils.plot_sources.plotters.plot_squarify import plot_squarify
from utils.printers import Printer
from utils.series_textwrap import index_wrap


def top_n_artists_by_playtime(df: pd.DataFrame, n: int):
    # Top artists by playtime
    copy = df.copy(True)
    grouped_by_artist_name = copy.groupby(copy["master_metadata_album_artist_name"])
    time_listened = grouped_by_artist_name["ms_played"].sum()
    time_listened = time_listened[time_listened != 0]
    time_listened = cast(pd.Series, time_listened)
    time_listened.sort_values(ascending=False, inplace=True)
    time_listend_mins = time_listened.div(6e4)
    time_listend_mins = cast(pd.Series, Filters.rows_gt(1, time_listend_mins))

    Printer.blue_underline(
        f"Out of {len(time_listend_mins)} artists, the top {n} artists based on track playtimes (in hours) are"
    )

    data = list(
        f"{chalk.green(f'{idx + 1}.')} {artist_name} - {playtime_hours:,.1f}"
        for idx, (artist_name, playtime_hours) in enumerate(time_listend_mins[:n].div(60).items())  # type: ignore
    )
    Printer.two_columns(data)

    # Plotting
    index_wrap(time_listend_mins, 10)
    plot_squarify(time_listend_mins[:n], f"Top {n} played artists by playtime")  # type: ignore
    plt.show()


def top_n_tracks_by_playcount(df: pd.DataFrame, n: int):
    most_played_tracks = cast(
        pd.Series, df.groupby(df["master_metadata_track_name"])["master_metadata_track_name"].count()
    )
    most_played_tracks.sort_values(ascending=False, inplace=True)

    Printer.blue_underline(f"Out of {len(most_played_tracks)} unique tracks, the top {n} played tracks are")

    data = list(
        f"{chalk.green(f'{idx + 1}.')} {trackname} - {playcount:,.0f}"
        for idx, (trackname, playcount) in enumerate(most_played_tracks[:n].items())  # type: ignore
    )
    Printer.two_columns(data)

    index_wrap(most_played_tracks, 10)
    plot_squarify(most_played_tracks[:n], f"{n} Most played tracks")  # type: ignore
    plt.show()


def top_n_albums_by_playcount(df: pd.DataFrame, n: int):
    most_played_albums = cast(
        pd.Series, df.groupby(df["master_metadata_album_album_name"])["master_metadata_album_album_name"].count()
    )
    most_played_albums.sort_values(ascending=False, inplace=True)

    # Number of tracks in each album
    track_count = df.groupby(df["master_metadata_album_album_name"])["master_metadata_track_name"].nunique()
    # NOTE: This ^ might be wrong

    # Normalizing the album playcounts
    # Normalized counts = total playcount / number of tracks in album
    most_played_albums = cast(pd.Series, most_played_albums.div(track_count).round(0))

    most_played_albums.sort_values(inplace=True, ascending=False)

    Printer.blue_underline(
        f"Out of {len(most_played_albums)} unique albums, the top {n} played albums based on approximate playcounts are"
    )
    data = list(
        f"{chalk.green(f'{idx + 1}.')} {album_name} - {playcount:,.0f}"
        for idx, (album_name, playcount) in enumerate(most_played_albums[:n].items())  # type: ignore
    )
    Printer.two_columns(data)

    index_wrap(most_played_albums, 10)
    plot_squarify(most_played_albums[:n], f"{n} Most played albums")  # type: ignore


def top_n_genres_and_countries(df: pd.DataFrame, artists_df: pd.DataFrame):
    unique_artists_names = cast(pd.Series, df["master_metadata_album_artist_name"].unique())
    unique_artists_df = artists_df.loc[artists_df["artist_name"].isin(unique_artists_names)]

    artists_countries_ser = unique_artists_df["country"].value_counts()

    # Vars
    countries_count = len(artists_countries_ser)
    most_listened_country_name = artists_countries_ser.index[0]
    most_listened_country_artists_count = artists_countries_ser[most_listened_country_name]

    Printer.blue_underline("Where the artists you listened to come from")

    print(
        f"Out of {chalk.yellow(countries_count)} countries, "
        f"most of the artists you listen to are from {chalk.yellow(most_listened_country_name)} "
        f"with a total of {chalk.yellow(most_listened_country_artists_count)} artists!!"
    )

    n_countries = 10
    Printer.green_underline(f"\nTop {n_countries} countries by artist count are:")

    data = list(
        f"{chalk.green(f'{idx + 1}.')} {country_name} - {artist_count}"
        for idx, (country_name, artist_count) in enumerate(artists_countries_ser[:n_countries].items())
    )
    Printer.two_columns(data)

    fig, ax = plt.subplots(2, 1, figsize=(16, 16))

    index_wrap(artists_countries_ser, 10)

    plot_squarify(
        artists_countries_ser[artists_countries_ser > 1],
        "Countries' artist count",
        _ax=ax[0],
    )

    # Genres stuff
    unique_genres = {}
    for genre_list in unique_artists_df["artist_genre"]:
        for genre in genre_list.split(","):
            genre = genre.strip()
            unique_genres[genre] = unique_genres.get(genre, 0) + 1

    # Genre of artist
    unique_genres_ser = pd.Series(unique_genres).sort_values(ascending=False)

    genre_count = len(unique_genres_ser)
    most_listened_genre_name = unique_genres_ser.index[0]
    most_listened_genre_count = unique_genres_ser.iat[0]
    Printer.blue_underline("\nWhat genres do you listen to")

    print(
        f"Out of {chalk.yellow(genre_count)} genres, "
        f"you listen to {chalk.yellow(most_listened_genre_name)} the most "
        f"with a total of {chalk.yellow(most_listened_genre_count)} artists under that genre!!"
    )

    n_genres = 20
    Printer.green_underline(f"\nTop {n_genres} genres by artist count are:")

    if n_genres % 2 != 0:
        raise ValueError(f"Count of genres to include must be an even number!!")

    data = list(
        f"{chalk.green(f'{idx + 1}.')} {genre} - {artist_count}"
        for idx, (genre, artist_count) in enumerate(unique_genres_ser[:n_genres].items())  # type: ignore
    )
    Printer.two_columns(data)

    index_wrap(unique_genres_ser, 10)
    plot_squarify(
        unique_genres_ser[unique_genres_ser.astype(int) > 1][:100],  # type: ignore
        "Genres' artist count",
        _ax=ax[1],
    )  # type: ignore

    plt.tight_layout()
    plt.show()


def top_analysis(df: pd.DataFrame, artists_df: pd.DataFrame):
    top_n_artists_by_playtime(df, 50)
    top_n_tracks_by_playcount(df, 50)
    top_n_albums_by_playcount(df, 50)
    top_n_genres_and_countries(df, artists_df)
