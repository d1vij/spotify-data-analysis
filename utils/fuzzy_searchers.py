# Fuzzy searching artists / track name
from rapidfuzz import fuzz
import pandas as pd


def search_artists(
    name: str,
    _in: pd.DataFrame | pd.Series | list[str],
    confidence: int,
    top_n=5,
    artist_colname="master_metadata_album_artist_name",
):

    if type(_in) == pd.DataFrame:
        artists = _in[artist_colname].values
    elif type(_in) == pd.Series:
        artists = _in.values
    elif type(_in) == list[str]:
        artists = _in
    else:
        raise (TypeError(f"Type of {type(_in)} not allowed"))

    if confidence <= 0 or confidence > 100:
        raise ValueError("Confidence must be within 1 to 100")

    matched = []
    ratios = []
    for artist in artists:
        if artist is not None:
            ratio = fuzz.partial_ratio(name.lower(), artist.lower())
            if (ratio >= confidence) and (artist not in matched):
                matched.append(artist)
                ratios.append(ratio)

    return [
        artist
        for artist, _ in sorted(
            [(artist, ratio) for artist, ratio in zip(matched, ratios)],
            key=lambda p: p[1],
            reverse=True,
        )[:top_n]
    ]


def search_tracks(
    name: str,
    _in: pd.DataFrame | pd.Series | list[str],
    confidence: int,
    top_n: int = 5,
    artist_colname="master_metadata_track_name",
):

    if type(_in) == pd.DataFrame:
        tracks = _in[artist_colname].values
    elif type(_in) == pd.Series:
        tracks = _in.values
    elif type(_in) == list[str]:
        tracks = _in
    else:
        raise (TypeError(f"Type of {type(_in)} not allowed"))

    if confidence <= 0 or confidence > 100:
        raise ValueError("Confidence must be within 1 to 100")

    matched = []
    ratios = []
    for track in tracks:
        if track is not None:
            ratio = fuzz.token_set_ratio(name.lower(), track.lower())
            if (ratio >= confidence) and (track not in matched):
                matched.append(track)
                ratios.append(ratio)

    return [
        track
        for track, _ in sorted(
            [(track, ratio) for track, ratio in zip(matched, ratios)],
            key=lambda p: p[1],
            reverse=True,
        )[:top_n]
    ]
