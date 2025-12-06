import json
import os
import shutil
import zipfile
from typing import Literal, cast

import pandas as pd

from utils.TrackInfoClasses import (
    FilteredTrackInfo,
    SongAttributes,
    SongInfoArray,
)


def read_file(name: str) -> SongInfoArray:
    with open(name, "r", encoding="utf-8") as file:
        return json.load(file)


def extract_filtered(song_info_obj, filters: list[SongAttributes]) -> FilteredTrackInfo:
    filtered = {}
    for filter in filters:
        filtered[filter] = song_info_obj[filter]
    return cast(FilteredTrackInfo, filtered)


# Unzips the spotify data zip file and compiles all the Audio Listening History files into one singular json.
# Returns the path of the compiled json file
def process_zip(filepath: str, filters: list[SongAttributes], *, _as: Literal["json", "csv"]):
    filename = os.path.basename(filepath).split(".")[0]

    zip_extract_path = os.path.join(
        os.path.dirname(filepath),
        filename,  # directory name same as filename
    )

    # print(f"{zip_extract_path=}")
    out_path = os.path.join(os.path.dirname(filepath), filename + "." + _as)

    with zipfile.ZipFile(filepath) as __zipfile:
        __zipfile.extractall(path=zip_extract_path)

    if "Spotify Extended Streaming History" not in os.listdir(zip_extract_path):
        raise TypeError(
            "Zip file is not spotify data, it must contain a folder named 'Spotify Extended Streaming History'"
        )

    data_folder = os.path.join(zip_extract_path, "Spotify Extended Streaming History")

    if os.path.exists(data_folder) is False:
        raise RuntimeError(f"Cannot os.path for {data_folder=}")

    files = [
        os.path.join(data_folder, file)
        for file in os.listdir(data_folder)
        if file.startswith("Streaming_History_Audio")  # only including the Audio History files
    ]

    songs = [song for file in files for song in read_file(file)]
    filtered = [extract_filtered(song, filters) for song in songs]
    tracks = pd.DataFrame(filtered)

    match _as:
        case "csv":
            tracks.to_csv(out_path, index=False)
        case "json":
            tracks.to_json(out_path, date_format="iso", orient="records")
        case _:
            raise ValueError(f"Invalid value passed to _as {_as}. Permitted values are 'json', 'csv'.")

    # cleanup
    # os.remove(filepath)
    shutil.rmtree(zip_extract_path)
    return out_path
