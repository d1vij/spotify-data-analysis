import re
from typing import cast
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

from utils.series_textwrap import index_wrap
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


def analysis_per_artist(frame: pd.DataFrame, artist: str):
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
    fig = plt.figure(figsize=(18, 20), constrained_layout=True)

    grid = fig.add_gridspec(
        4, 2, height_ratios=[2.5, 1, 1, 1.5], hspace=0.4, wspace=0.3
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

    # Top 50 played tracks
    played_track_count = (
        artist_frame.groupby("master_metadata_track_name")
        .size()
        .sort_values(ascending=False)
    )

    index_wrap(played_track_count, 12)
    index_ellipses(played_track_count, 22)

    plot_squarify(played_track_count[:50], f"Fifty most played tracks by {artist}", ax1)

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

    plt.tight_layout()
    plt.show()


PROMPT = """What do you want to do ??
(1) Display top artist analysis for top artists
(2) Display analysis for custom artist
(*) Exit
"""


def __top_n_artist_analysis(frame: pd.DataFrame):
    while True:
        try:
            n = int(input("Generate analysis for how many top artists ??: "))
            break
        except:
            print("Unable to parse that value!!")

    top_artists = (
        frame.groupby("master_metadata_album_artist_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
    )

    top_artists.head()

    for artist_name, _ in top_artists.head(n).items():
        artist_name = cast(str, artist_name)
        analysis_per_artist(frame, artist_name)
        print(" ")


def __custom_artist_analysis(
    frame: pd.DataFrame, *, __confidence: int = 80, __artist_name: str | None = None
):

    artist_name = __artist_name or input("Input the name of the artist: ")
    if(artist_name == ""):
        print("Enter a valid name!!")
        return __custom_artist_analysis(frame)

    artists_found = fuzzy_search(
        artist_name,
        frame["master_metadata_album_artist_name"],
        "partial ratio",
        confidence=__confidence,
        top_n=50
    )

    artists_found_count = len(artists_found)

    if(artists_found_count == 0):
        # No artists found after fuzzy searching
        if (__confidence - 20 < 0):
            # Could not find any artist with that name even after lowering confidence.
            print(f"Couldnt find any artist with name {artist_name}!!\n")
            return

        print(
            f"Could not fuzzy search any artist with name {artist_name}, retrying with a lower confidence"
        )
        return __custom_artist_analysis(frame, __confidence=__confidence - 20, __artist_name = artist_name)

    elif(artists_found_count > 1):
        # found more than 1 name match, ask user which one to consider
        print(f"Found {artists_found_count} matches, select the number for which one to choose")

        for (idx, name) in enumerate(artists_found, start=1):
            print(f"({idx}) {name}")
        
        while True:
            try:
                option = int(input("Artist index: "))
            except:
                print("Unable to parse that value!!")

            if(option > 0 and option <= artists_found_count): 
                break

        print(f"Showing analysis for {artists_found[option - 1]}")
        artist = artists_found[option - 1]
    
    else:
        # only one artist found
        artist = artists_found[0]

    analysis_per_artist(frame, artist)
    return


def interactive_per_artist_analysis(frame: pd.DataFrame):
    while True:
        match int(input(PROMPT)):
            case 1:
                __top_n_artist_analysis(
                    frame,
                )

            case 2:
                __custom_artist_analysis(frame)
            case _:
                print("Exiting!!")
                break
