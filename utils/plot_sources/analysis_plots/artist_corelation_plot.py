from typing import Literal
from itertools import combinations
import pandas as pd
from utils.TrackInfoClasses import SongAttributes


def generate_correlation_matrix(
    df: pd.DataFrame,
    feild_1: SongAttributes,  # Eg artist name
    metric: SongAttributes,  # Eg ms played
    time_period: Literal["hour", "day", "month"] = "day",
):
    if feild_1 not in df.columns:
        raise ValueError(f"Column f{feild_1} does not exists in the dataframe!!")

    top_n = 25

    grouped = df.groupby(feild_1)
    metric_series = grouped[metric].sum().sort_values(ascending=False)

    # selecting top n artists based on playtime
    top_n_entries = df[df[feild_1].isin(metric_series.index[:top_n])].copy()
    match time_period:
        case "hour":
            top_n_entries["period"] = top_n_entries["ts"].dt.hour
        case "day":
            top_n_entries["period"] = top_n_entries["ts"].dt.date
        case "month":
            top_n_entries["period"] = top_n_entries["ts"].dt.month
        case _:
            raise ValueError(f"time_period cannot be {time_period}")

    unqiue_entries = top_n_entries[feild_1].unique()
    unqiue_period = top_n_entries["period"].unique()

    co_occurance_matrix = pd.DataFrame(
        0, index=unqiue_entries, columns=unqiue_entries, dtype=int
    )

    for period in unqiue_period:
        # Selecting the artists played in that day
        entries = top_n_entries.loc[top_n_entries["period"] == period, feild_1].unique()  # type: ignore
        for name_A, name_B in combinations(entries, 2):
            co_occurance_matrix.at[name_A, name_B] += 1  # type: ignore
            co_occurance_matrix.at[name_B, name_A] += 1  # type: ignore

    return co_occurance_matrix


# plot_corelation_matrix(get_probability_matrix(df), "a", "c", "d")


def generate_probability_matrix(correlation_matrix):
    # creating conditional probability matrix
    # conditional probabilty matrix is created by normalizing columns of co-occurance matrix
    # normalizing means dividing each row of co-occurance matrix by the sum of all values in that row
    # read as "probability of Y axis metric happening when X axis metric happened"
    return (correlation_matrix.div(correlation_matrix.sum(axis=1), axis=0) * 100).round(
        1
    )

from utils.plot_sources.plotters.plot_heatmap import plot_heatmap

def artist_correlation_plot(df: pd.DataFrame):
    mat = generate_correlation_matrix(
        df, "master_metadata_album_artist_name", "ms_played", "day"
    )
    mat = generate_probability_matrix(mat)
    plot_heatmap(
        mat,
        "Probability that tracks by two artists were listened on the same day",
        "Artist A",
        "Artist B",
        _fmt=".1f",
    )