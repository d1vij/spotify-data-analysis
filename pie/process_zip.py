import os
from os import path
import zipfile

from typing import TypedDict, Literal, Optional, cast
import json
import pandas as pd

from pathlib import Path

class TrackInfo(TypedDict, total=True):
    ts: str
    platform: str
    ms_played: int
    conn_country: str
    ip_addr: str
    master_metadata_track_name: str
    master_metadata_album_artist_name: str
    master_metadata_album_album_name: str
    spotify_track_uri: str
    episode_name: Optional[str]
    episode_show_name: Optional[str]
    spotify_episode_uri: Optional[str]
    audiobook_title: Optional[str]
    audiobook_uri: Optional[str]
    audiobook_chapter_uri: Optional[str]
    audiobook_chapter_title: Optional[str]
    reason_start: Optional[
        Literal[
            "playbtn", "fwdbtn", "backbtn", "trackdone",
            "clickrow", "appload", "remote", "trackerror", "unknown"
        ]
    ]
    reason_end: Optional[
        Literal[
            "fwdbtn", "backbtn", "logout", "endplay",
            "trackdone", "unknown", "remote",
            "unexpected-exit-while-paused", "unexpected-exit", "trackerror"
        ]
    ]
    shuffle: bool
    skipped: bool
    offline: bool
    offline_timestamp: int
    incognito_mode: bool

    
class FilteredTrackInfo(TypedDict):
    ts: Optional[str]
    platform: Optional[str]
    ms_played: Optional[int]
    conn_country: Optional[str]
    ip_addr: Optional[str]
    master_metadata_track_name: Optional[str]
    master_metadata_album_artist_name: Optional[str]
    master_metadata_album_album_name: Optional[str]
    spotify_track_uri: Optional[str]
    episode_name: Optional[str]
    episode_show_name: Optional[str]
    spotify_episode_uri: Optional[str]
    audiobook_title: Optional[str]
    audiobook_uri: Optional[str]
    audiobook_chapter_uri: Optional[str]
    audiobook_chapter_title: Optional[str]
    reason_start: Optional[
        Literal[
            "playbtn", "fwdbtn", "backbtn", "trackdone", 
            "clickrow", "appload", "remote", "trackerror", "unknown"
        ]
    ]
    reason_end: Optional[
        Literal[
            "fwdbtn", "backbtn", "logout", "endplay", "trackdone", 
            "unknown", "remote", "unexpected-exit-while-paused", 
            "unexpected-exit", "trackerror"
        ]
    ]
    shuffle: Optional[bool]
    skipped: Optional[bool]
    offline: Optional[bool]
    offline_timestamp: Optional[int]
    incognito_mode: Optional[bool]

SongInfoArray = list[TrackInfo]
FilteredSongInfoArray = list[FilteredTrackInfo]
SongAttributes = Literal["ts","platform","ms_played","conn_country","ip_addr","master_metadata_track_name","master_metadata_album_artist_name","master_metadata_album_album_name","spotify_track_uri","episode_name","episode_show_name","spotify_episode_uri","audiobook_title","audiobook_uri","audiobook_chapter_uri","audiobook_chapter_title","reason_start","reason_end","shuffle","skipped","offline","offline_timestamp","incognito_mode"]

def read_file(name:str) -> SongInfoArray:
    with open(name, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_filtered(song_info_obj,filters:list[SongAttributes]) -> FilteredTrackInfo:
    filtered = {}
    for filter in filters : filtered[filter] = song_info_obj[filter]
    return cast(FilteredTrackInfo, filtered)

filters: list[SongAttributes] = ["ts", "ms_played", "master_metadata_track_name", "master_metadata_album_artist_name", "master_metadata_album_album_name", "spotify_track_uri"]



def process(filepath: str):
    filename = path.basename(filepath).split(".")[0]
    print(f"Filename {filename}")
    
    zip_extract_path = path.join(
        path.dirname(filepath), filename #directory name same as filename
    )
    
    print(f"{zip_extract_path=}")
    out_json_path = path.join(
        path.dirname(filepath), filename + ".json"
    )

    try:
        with zipfile.ZipFile(filepath) as __zipfile:
            __zipfile.extractall(path=zip_extract_path)
    except Exception as e:
        raise Exception(
            "Error in extracting zipfile"
        ) from e  # reraising the same exception so that py-bridge's core module handles it accordingly

    print(f"Contents at {zip_extract_path} are ", os.listdir(zip_extract_path))
    if('Spotify Extended Streaming History' not in os.listdir(zip_extract_path)):
            raise TypeError("zip file is not spotify data, it must contain a folder named 'Spotify Extended Streaming History'")
            
    data_folder = path.join(zip_extract_path, "Spotify Extended Streaming History")
    if(path.exists(data_folder) == False):
        raise RuntimeError(f"Cannot path for {data_folder=}")
    
    files = [
        os.path.join(data_folder, file)
        for file in os.listdir(data_folder)
        if file.startswith("Streaming_History_Audio") # only including the Audio History files
    ]
    print(f"{files=}")
    
    songs = [song for file in files for song in read_file(file)]
    filtered = [extract_filtered(song, filters) for song in songs]
    tracks = pd.DataFrame(filtered)
    # tracks["ts"] = pd.to_datetime(tracks['ts']) 
    tracks.to_json(out_json_path)

    print(tracks.head())
    # cleanup
    # os.remove(filepath)
    # os.remove(extract_path)

    return out_json_path


if __name__ == "__main__":
    process("/home/divij/coding/projects/spotify-data-analysis-app/pie/sample/my_spotify_data.zip")