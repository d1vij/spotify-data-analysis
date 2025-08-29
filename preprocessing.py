import json
from typing import TypedDict, Literal, Optional, cast


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
    
    