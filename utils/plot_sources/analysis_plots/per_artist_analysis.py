# Generates analysis for each artist

import warnings
from datetime import datetime
from typing import cast

import chalk
import matplotlib.patches as mpatch
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utils.fuzzy_searchers import fuzzy_search
from utils.plot_sources.analysis_plots.daily_listening_activity import (
    daily_listening_activity,
)
from utils.plot_sources.analysis_plots.daily_tracks_graph import daily_tracks_graph
from utils.plot_sources.analysis_plots.track_playtime_kde_dist import (
    track_playtime_kde_dist,
)
from utils.plot_sources.plotters.plot_squarify import plot_squarify
from utils.plot_sources.plotters.simple_barplot import simple_barplot
from utils.printers import Printer
from utils.series_textellipses import index_ellipses
from utils.series_textwrap import index_wrap, list_wrap


# Another generic bar plot plotter
def __bar_plot(heights, labels, target: str, title: str, x_label: str, y_labels: str, *, _ax=None):
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
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_labels)
    ax.set_ylim(top=max(heights) + 10)

    # Patches allow to for setting up custom legends
    patches = [
        mpatch.Patch(label=f"{name} - {playtime}", facecolor=color)
        for (name, playtime, color) in zip(labels, heights, colors)
    ]
    ax.legend(loc="upper right", ncols=2, frameon=True, handles=patches)
    sns.despine()
    if _ax is None:
        plt.show()


# Analyzing provided artist with artists from same country or with similar ranking
def __relative_artist_analysis(
    artist_name: str,
    frame: pd.DataFrame,  # User's history dataframe
    artists_df: pd.DataFrame,  # Artist metadata dataframe
    ax1,
    ax2,
):
    # All the unique artists from my listening history
    unique_artists_name = cast(pd.Series, frame["master_metadata_album_artist_name"].unique())

    # Extracting rows from the artist metadata dataframe,
    # for only those artists which are in user's listening history dataframe
    unique_artists_df = artists_df.loc[artists_df["artist_name"].isin(unique_artists_name)]

    # Identifying the country of my artist from the artist metadata dataframe
    if artist_name not in unique_artists_df["artist_name"].values:
        warnings.warn(f"No country found for artist {artist_name}, proceeding with no country based analysis")
        return
    else:
        artist_country = unique_artists_df.loc[unique_artists_df["artist_name"] == artist_name, "country"].iat[0]

    # Common artists from the same country as our artist
    same_country_artists_names = unique_artists_df.loc[artists_df["country"] == artist_country, "artist_name"]

    same_country_artists_playtime_ser = (
        frame.loc[
            frame["master_metadata_album_artist_name"].isin(
                same_country_artists_names
            ),
            ["master_metadata_album_artist_name", "ms_played"],
        ]
        .groupby("master_metadata_album_artist_name")["ms_played"]
        .sum()
        .sort_values(ascending=False)
    )

    # Getting the rank of my artist
    # Rank is just the index number of my artist in the playtime series
    artist_rank = cast(
        int,
        same_country_artists_playtime_ser.index.get_loc(artist_name),
    )

    # Since the indexes start at 0
    artist_rank += 1

    # Edge case senario
    if artist_rank <= 0:
        raise ValueError(f"artist_rank cannot be lesser than 1. It is {artist_rank}")

    # How many artists to consider on either side
    delta = 3

    # Determining the indexes of nearby artists wrt the ranking of my artist
    # for example, if my artist ranks 10th, then the slice range of nearby artists
    # would be from (10 - delta) to (10 + delta) (exclusive), ie from 7 to 13 (exclusive)
    if artist_rank <= delta:
        # Whatever the rank is, we will always display data for (2*delta) + 1 artists
        # It is not nessasary that the provided artist_name would be at the center of this distribution
        lim_prev = 1
        lim_next = (2 * delta) + 1
    else:
        lim_prev = artist_rank - delta
        lim_next = artist_rank + delta

    surrounding_artists = same_country_artists_playtime_ser.iloc[lim_prev - 1 : lim_next]
    __bar_plot(
        surrounding_artists.div(3.6e6).round(1).values,
        surrounding_artists.index,
        artist_name,
        f"Playtime of {artist_name} relative to nearby ranking artists from same country.",
        "Artists",
        "Playtime in hours",
        _ax=ax1,
    )

    # The top artists of the country are just the first (2*delta) artists
    top_artists = same_country_artists_playtime_ser.iloc[: (2 * delta)]

    # If the artist is a top artist, it is possible that these two plots are same
    top_artists[artist_name] = same_country_artists_playtime_ser[artist_name]
    __bar_plot(
        top_artists.div(3.6e6).round(1).values,
        top_artists.index,
        artist_name,
        f"Playtime of {artist_name} with relative to top artists from the same country.",
        "Artists",
        "Playtime in hours",
        _ax=ax2,
    )


# Analyzing the albums of my artist
def __artist_album_analysis(frame: pd.DataFrame, artist_name: str):
    # Wont filter here based on artist name cuz my dataframe already is filtered
    albums = frame.loc[
        :,
        "master_metadata_album_album_name",
    ].unique()

    Printer.plain()
    Printer.blue_underline(f"Album analysis for {chalk.yellow(artist_name)}")

    Printer.green_underline(f"All listened albums by {artist_name}")
    data = list(f"{chalk.green(f'{idx}.')} {album}" for (idx, album) in enumerate(sorted(albums), 1))
    Printer.two_columns(data)

    # Approximate count of tracks in each album by the artist
    # This would be inaccurate if the user hasnt listened to all tracks from the album
    album_track_count = (
        frame.loc[frame["master_metadata_album_album_name"].isin(albums)]
        .groupby("master_metadata_album_album_name")
        .nunique()
        .loc[:, "master_metadata_track_name"]
    )

    # Times a track from a particular album was played
    album_track_play_count = (
        frame.loc[frame["master_metadata_album_album_name"].isin(albums)]
        .groupby("master_metadata_album_album_name")
        .size()
    )

    # Number of time an album has been played
    # playcount = total times track from a album has been played / number of tracks from that album
    album_playcount = (
        album_track_play_count.div(album_track_count)
        .fillna(1)
        .sort_values(ascending=False)
        .head(50)  # Only get top 50
        .round(0)
        .astype(int)
    )

    Printer.plain()
    Printer.green_underline("Top albums by approximate playcount")
    Printer.two_columns(
        list(
            f"{chalk.green(f'{idx}.')} {album} - {playcount}"
            for (idx, (album, playcount)) in enumerate(album_playcount.items(), 1)
        )
    )


def analysis_per_artist(frame: pd.DataFrame, artist: str, artists_info_frame: pd.DataFrame):
    if artist not in frame["master_metadata_album_artist_name"].values:
        raise ValueError(f"Artist {artist} is not in data")

    # Dataframe having data only for the provided artist
    artist_frame = cast(pd.DataFrame, frame[frame["master_metadata_album_artist_name"] == artist].copy(True))
    # grouped = artist_frame.groupby("master_metadata_album_artist_name")
    # changing ts to year
    artist_frame["year"] = artist_frame.loc[:, "ts"].apply(lambda ts: datetime.strftime(ts, "%Y"))

    # Setting up plot grid
    fig = plt.figure(figsize=(18, 24), constrained_layout=False)

    grid = fig.add_gridspec(5, 2, height_ratios=[2.5, 1, 1, 1, 1.5], hspace=0.4, wspace=0.3)

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
        artist_frame.groupby("master_metadata_track_name").size().sort_values(ascending=False)
    )
    Printer.blue_underline(f"Twenty most played tracks by {chalk.yellow(artist)}")

    data = list(
        f"{chalk.green(f'{idx + 1}.')} {trackname} - {chalk.yellow(playcount)} plays"
        for idx, (trackname, playcount) in enumerate(played_track_count.head(25).items())
    )
    Printer.two_columns(data)
    index_wrap(played_track_count, 12)
    index_ellipses(played_track_count, 22)

    plot_squarify(played_track_count.head(25), f"Twenty Five most played tracks by {artist}", ax1)

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

    # artist_frame = cast(pd.DataFrame, artist_frame)
    daily_tracks_graph(artist_frame, ax4, print_analysis=True, artist_name=artist)
    track_playtime_kde_dist(artist_frame, [ax5, ax3], True, artist_name=artist)
    __artist_album_analysis(artist_frame, artist)
    daily_listening_activity(artist_frame, ax6)
    __relative_artist_analysis(artist, frame, artists_info_frame, ax7, ax8)

    plt.tight_layout()
    fig.subplots_adjust(top=0.93, hspace=0.4, wspace=0.3)
    plt.show()


PROMPT = """
What do you want to do ??
(1) Display top artist analysis for top artists
(2) Display analysis for custom artist
(*) Exit
"""


# Asks the user which top n artists to generate the analysis for
# Top artists are determined on the basis of total playtime
def __top_n_artist_analysis(frame: pd.DataFrame, artists_info_frame: pd.DataFrame):
    while True:
        try:
            n = int(input("Generate analysis for how many top artists ??: "))
            break
        except ValueError:
            print("Unable to parse that value!!")

    Printer.red_bold(f"Generate analysis for how many top artists ??: {n}")

    top_artists = (
        frame.groupby("master_metadata_album_artist_name")["ms_played"].sum().sort_values(ascending=False) #type: ignore
    )

    for artist_name, _ in top_artists.head(n).items():
        artist_name = cast(str, artist_name)
        analysis_per_artist(frame, artist_name, artists_info_frame)
        Printer.plain()


# Asks the user name of the artist to generate the analysis for,
# then the exact artist name is fuzzy finded.
# Incase no match is found, the fuzzy finding is done again (recursively) with a lower confidence,
# until either a match is found, or the confidence becomes lower than a threshold,
# most often implying that no such artist exists as provided by the user.
# Incase of multiple matches, the user is provided an option menu,
# asking for the exact artist name.
def __custom_artist_analysis(
    frame: pd.DataFrame,
    artists_info_frame: pd.DataFrame,
    *,
    __confidence: int = 80,
    __artist_name: str | None = None,
):
    # Either reuse the artist name provided by the lower confidence search, or ask the user for one
    artist_name = __artist_name or input("Input the name of the artist: ")

    if artist_name == "":
        print("Enter a valid name!!")
        return __custom_artist_analysis(frame, artists_info_frame)

    Printer.red_bold(f"Input the name of the artist: {artist_name}")

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
            Printer.plain(f"Couldnt find any artist with name {artist_name}!!\n")
            return

        Printer.plain(f"Could not fuzzy search any artist with name {artist_name}, retrying with a lower confidence")
        return __custom_artist_analysis(
            frame,
            artists_info_frame,
            __confidence=__confidence - 20,
            __artist_name=artist_name,
        )

    elif artists_found_count > 1:
        # found more than 1 name match, ask user which one to consider
        Printer.red_bold(f"Found {artists_found_count} matches, select the number for which one to choose")

        Printer.two_columns(
            list(f"{chalk.green(str(idx) + '.')} {artist}" for (idx, artist) in enumerate(artists_found, 1))
        )

        while True:
            try:
                option = int(input("Artist index: "))
                if option == 0:
                    Printer.plain("Selecting no artist!!")
                elif option > 0 and option <= artists_found_count:
                    break
            except ValueError:
                print("Unable to parse that value!!")

        artist = artists_found[option - 1]
    else:
        # only one artist found
        artist = artists_found[0]

    Printer.green(f"Showing analysis for {artist}")
    analysis_per_artist(frame, artist, artists_info_frame)
    return


# Interactively ask the user for which to generate the analysis for
def interactive_per_artist_analysis(frame: pd.DataFrame, artist_info_frame: pd.DataFrame):
    while True:
        try:
            match int(input(PROMPT)):
                case 1:
                    __top_n_artist_analysis(frame, artist_info_frame)
                case 2:
                    __custom_artist_analysis(frame, artist_info_frame)
                case _:
                    print("Exiting!!")
                    break
        except ValueError:
            # User inputting goofy stuff
            pass
