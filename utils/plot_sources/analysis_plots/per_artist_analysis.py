import re
from typing import cast
from datetime import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

from utils.series_textwrap import index_wrap, list_wrap
from utils.series_textellipses import index_ellipses

from utils.plot_sources.plotters.simple_barplot import simple_barplot
from utils.plot_sources.plotters.plot_squarify import plot_squarify

from utils.plot_sources.analysis_plots.daily_tracks_graph import daily_tracks_graph
from utils.plot_sources.analysis_plots.track_playtime_kde_dist import (
    track_playtime_kde_dist,
)
from utils.plot_sources.analysis_plots.daily_listening_activity import (
    daily_listening_activity,
)
from utils.fuzzy_searchers import fuzzy_search


def __bar_plot(heights, labels, target: str, title: str, *, _ax=None):
    blue = "#5EABD6"
    red = "#EF5A6F"

    # All other bars blue, artist bar red
    colors = [blue if (value != target) else red for value in labels]

    if _ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    else:
        ax = _ax
    sns.barplot(x=list_wrap(labels, 12), y=heights, palette=colors, ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Artists")
    ax.set_ylabel("Playtime in hours")
    ax.set_ylim(top=max(heights) + 10)
    patches = [
        mpatch.Patch(label=f"{name} - {playtime}", facecolor=color)
        for (name, playtime, color) in zip(labels, heights, colors)
    ]
    ax.legend(loc="upper right", ncols=2, frameon=True, handles=patches)
    sns.despine()
    if _ax is None:
        plt.show()


def __relative_artist_analysis(
    artist_name: str, user_df: pd.DataFrame, artists_df: pd.DataFrame, ax1, ax2
):
    unique_artists_name = user_df["master_metadata_album_artist_name"].unique()
    # Extracting rows for only those artists which are in user's data
    unique_artists_df = artists_df.loc[
        artists_df["artist_name"].isin(unique_artists_name)
    ]

    # Number of artists from a particular country
    artist_countries_count_ser = unique_artists_df["country"].value_counts()

    if artist_name not in unique_artists_df["artist_name"].values:
        raise ValueError(f"No country found for artist {artist_name}")
    else:
        artist_country = unique_artists_df.loc[
            unique_artists_df["artist_name"] == artist_name, "country"
        ].iat[0]

        print(artist_country)
    # Common artists from the same country as our artist
    same_country_artists_names = unique_artists_df.loc[
        artists_df["country"] == artist_country, "artist_name"
    ]

    same_country_artists_playtime_ser = (
        user_df.loc[
            user_df["master_metadata_album_artist_name"].isin(
                same_country_artists_names  # type: ignore
            ),
            ["master_metadata_album_artist_name", "ms_played"],
        ]
        .groupby("master_metadata_album_artist_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
    )

    artist_rank = cast(
        int, same_country_artists_playtime_ser.index.get_loc(artist_name)
    )

    # How many artists to consider on either side
    delta = 3
    if artist_rank <= 0:
        raise ValueError(f"artist_rank cannot be lesser than 1. It is {artist_rank}")

    if artist_rank <= delta:
        # Whatever the rank is, we will always display data for (2*delta) + 1 artists
        # It is not nessasary that the provided artist_name would be at the center of this distribution
        lim_prev = 1
        lim_next = (2 * delta) + 1
    else:
        lim_prev = artist_rank - delta
        lim_next = artist_rank + delta

    surrounding_artists = same_country_artists_playtime_ser.iloc[
        lim_prev - 1 : lim_next
    ]
    __bar_plot(
        surrounding_artists.div(3.6e6).round(1).values,
        surrounding_artists.index,
        artist_name,
        f"Playtime of {artist_name} relative to nearby ranking artists from same country.",
        _ax=ax1,
    )
    top_artists = same_country_artists_playtime_ser.iloc[: (2 * delta)]

    # If the artist is a top artist, it is possible that these two plots are same
    top_artists[artist_name] = same_country_artists_playtime_ser[artist_name]
    __bar_plot(
        top_artists.div(3.6e6).round(1).values,
        top_artists.index,
        artist_name,
        f"Playtime of {artist_name} with relative to top artists from the same country.",
        _ax=ax2,
    )


def analysis_per_artist(
    frame: pd.DataFrame, artist: str, artists_info_frame: pd.DataFrame
):
    if artist not in frame["master_metadata_album_artist_name"].values:
        raise ValueError(f"Artist {artist} is not in data")

    artist_frame = frame[frame["master_metadata_album_artist_name"] == artist].copy(
        True
    )
    # grouped = artist_frame.groupby("master_metadata_album_artist_name")
    # changing ts to year
    artist_frame["year"] = artist_frame["ts"].apply(
        lambda ts: datetime.strftime(ts, "%Y")
    )

    # Setting up plot grid
    fig = plt.figure(figsize=(18, 26), constrained_layout=False)

    grid = fig.add_gridspec(
        5, 2, height_ratios=[2.5, 1, 1, 1.5, 1.5], hspace=0.4, wspace=0.3
    )

    # 1x2
    ax1 = fig.add_subplot(grid[0, :])

    # 1x1
    ax2 = fig.add_subplot(grid[1, 0])

    # 1x1
    # Currently empty
    ax3 = fig.add_subplot(grid[1, 1])

    # 1x1

    ax4 = fig.add_subplot(grid[2, 0])
    ax5 = fig.add_subplot(grid[2, 1])
    ax6 = fig.add_subplot(grid[3, :])

    ax7 = fig.add_subplot(grid[4, 0])
    ax8 = fig.add_subplot(grid[4, 1])

    # Top 50 played tracks
    played_track_count = (
        artist_frame.groupby("master_metadata_track_name")
        .size()
        .sort_values(ascending=False)
    )

    index_wrap(played_track_count, 12)
    index_ellipses(played_track_count, 22)

    plot_squarify(
        played_track_count[:25], f"Twenty Five most played tracks by {artist}", ax1
    )

    # Year wise play time
    yearwise_playtime = artist_frame.groupby("year").size()
    simple_barplot(
        yearwise_playtime,
        f"Tracks played in a particular year by {artist}",
        "Year",
        "Play count",
        ax2,
    )

    # fig, ax = plt.subplots(2, 2, figsize=(15,7.5))

    fig.suptitle("Track analysis for " + artist, fontsize=23)

    daily_tracks_graph(artist_frame, ax4)
    track_playtime_kde_dist(artist_frame, [ax5, ax3])  # type: ignore
    daily_listening_activity(artist_frame, ax6)
    __relative_artist_analysis(artist, frame, artists_info_frame, ax7, ax8)

    plt.tight_layout()
    fig.subplots_adjust(top=0.93, hspace=0.4, wspace=0.3)
    plt.show()


PROMPT = """What do you want to do ??
(1) Display top artist analysis for top artists
(2) Display analysis for custom artist
(*) Exit
"""


def __top_n_artist_analysis(frame: pd.DataFrame, artists_info_frame: pd.DataFrame):
    while True:
        try:
            n = int(input("Generate analysis for how many top artists ??: "))
            break
        except:
            print("Unable to parse that value!!")

    print(f"Generate analysis for how many top artists ??: {n}")

    top_artists = (
        frame.groupby("master_metadata_album_artist_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
    )

    top_artists.head()

    for artist_name, _ in top_artists.head(n).items():
        artist_name = cast(str, artist_name)
        analysis_per_artist(frame, artist_name, artists_info_frame)
        print(" ")


def __custom_artist_analysis(
    frame: pd.DataFrame,
    artists_info_frame: pd.DataFrame,
    *,
    __confidence: int = 80,
    __artist_name: str | None = None,
):
    artist_name = __artist_name or input("Input the name of the artist: ")
    if artist_name == "":
        print("Enter a valid name!!")
        return __custom_artist_analysis(frame, artists_info_frame)
    print(f"Input the name of the artist: {artist_name}")

    artists_found = fuzzy_search(
        artist_name,
        frame["master_metadata_album_artist_name"],
        "partial ratio",
        confidence=__confidence,
        top_n=50,
    )

    artists_found_count = len(artists_found)

    if artists_found_count == 0:
        # No artists found after fuzzy searching
        if __confidence - 20 < 0:
            # Could not find any artist with that name even after lowering confidence.
            print(f"Couldnt find any artist with name {artist_name}!!\n")
            return

        print(
            f"Could not fuzzy search any artist with name {artist_name}, retrying with a lower confidence"
        )
        return __custom_artist_analysis(
            frame,
            artists_info_frame,
            __confidence=__confidence - 20,
            __artist_name=artist_name,
        )

    elif artists_found_count > 1:
        # found more than 1 name match, ask user which one to consider
        print(
            f"Found {artists_found_count} matches, select the number for which one to choose"
        )

        for idx, name in enumerate(artists_found, start=1):
            print(f"({idx}) {name}")

        while True:
            try:
                option = int(input("Artist index: "))
            except:
                print("Unable to parse that value!!")

            if option > 0 and option <= artists_found_count:
                break

        print(f"Showing analysis for {artists_found[option - 1]}")
        artist = artists_found[option - 1]

    else:
        # only one artist found
        artist = artists_found[0]

    analysis_per_artist(frame, artist, artists_info_frame)
    return


def interactive_per_artist_analysis(
    frame: pd.DataFrame, artist_info_frame: pd.DataFrame
):
    while True:
        match int(input(PROMPT)):
            case 1:
                __top_n_artist_analysis(frame, artist_info_frame)

            case 2:
                __custom_artist_analysis(frame, artist_info_frame)
            case _:
                print("Exiting!!")
                break
