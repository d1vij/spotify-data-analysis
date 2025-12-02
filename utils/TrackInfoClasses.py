from typing import Literal, Optional, TypedDict


class TrackInfo(TypedDict, total=True):
    """
    Class describing each data object in spotify's listening history json file
    Only there for type hinting and data reference
    """

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
            "playbtn",
            "fwdbtn",
            "backbtn",
            "trackdone",
            "clickrow",
            "appload",
            "remote",
            "trackerror",
            "unknown",
        ]
    ]
    reason_end: Optional[
        Literal[
            "fwdbtn",
            "backbtn",
            "logout",
            "endplay",
            "trackdone",
            "unknown",
            "remote",
            "unexpected-exit-while-paused",
            "unexpected-exit",
            "trackerror",
        ]
    ]
    shuffle: bool
    skipped: bool
    offline: bool
    offline_timestamp: int
    incognito_mode: bool


class FilteredTrackInfo(TypedDict):
    """Class describing the each object of post-processed and filtered data"""

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
            "playbtn",
            "fwdbtn",
            "backbtn",
            "trackdone",
            "clickrow",
            "appload",
            "remote",
            "trackerror",
            "unknown",
        ]
    ]
    reason_end: Optional[
        Literal[
            "fwdbtn",
            "backbtn",
            "logout",
            "endplay",
            "trackdone",
            "unknown",
            "remote",
            "unexpected-exit-while-paused",
            "unexpected-exit",
            "trackerror",
        ]
    ]
    shuffle: Optional[bool]
    skipped: Optional[bool]
    offline: Optional[bool]
    offline_timestamp: Optional[int]
    incognito_mode: Optional[bool]


# Json provided by spotify is in this format
SongInfoArray = list[TrackInfo]

# Once data is filtered by utils.process_zip.process_zip,
# the compiled json is in this format
FilteredSongInfoArray = list[FilteredTrackInfo]

# Again for the sake of intellisense
SongAttributes = Literal[
    "ts",
    "platform",
    "ms_played",
    "conn_country",
    "ip_addr",
    "master_metadata_track_name",
    "master_metadata_album_artist_name",
    "master_metadata_album_album_name",
    "spotify_track_uri",
    "episode_name",
    "episode_show_name",
    "spotify_episode_uri",
    "audiobook_title",
    "audiobook_uri",
    "audiobook_chapter_uri",
    "audiobook_chapter_title",
    "reason_start",
    "reason_end",
    "shuffle",
    "skipped",
    "offline",
    "offline_timestamp",
    "incognito_mode",
]
