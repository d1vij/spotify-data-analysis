import pandas as pd

from utils.process_zip import SongAttributes
from utils.process_zip import process_zip


# Reads the data zip path and returns a dataframe for the compile data, ready to be analyzed
def generate_frame(zip_path: str) -> pd.DataFrame:
    # Only extract the following rows from the whole json
    filters: list[SongAttributes] = [
        "ts",
        "ms_played",
        "master_metadata_track_name",
        "master_metadata_album_artist_name",
        "master_metadata_album_album_name",
    ]

    compiled_data_path = process_zip(zip_path, filters, _as="csv")
    # df = pd.read_json(compiled_json_path)
    df = pd.read_csv(compiled_data_path)

    # Converting the ts column to datetime object
    df["ts"] = pd.to_datetime(df["ts"])
    return df
