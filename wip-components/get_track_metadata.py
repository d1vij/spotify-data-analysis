import asyncio
import aiohttp
import pandas as pd
import numpy as np
from urllib.parse import quote
import time


API_BASE = "http://ws.audioscrobbler.com/2.0/"
API_KEY = "931513964b1e073e2951fd3aebd03dd3"


async def fetch_track(
    session, track_name: str, artist_name: str, api_key: str = API_KEY, retries: int = 3
) -> dict | None:
    """Fetch metadata for a single track asynchronously with retries and logging."""
    url = (
        f"{API_BASE}?method=track.getInfo&api_key={api_key}&format=json"
        f"&track={quote(track_name)}&artist={quote(artist_name)}"
    )

    for attempt in range(1, retries + 1):
        try:
            async with session.get(url, timeout=10) as resp:
                response_json = await resp.json()

                if response_json.get("error") == 6:
                    print(f"[NOT FOUND] {track_name} - {artist_name}")
                    return None

                track = response_json.get("track", {})
                tags = track.get("toptags", {}).get("tag", [])

                if isinstance(tags, dict):  # if only one tag, API returns dict
                    tags = [tags]

                found_tags = [tag.get("name", np.nan) for tag in tags]
                mbid = track.get("mbid", np.nan)

                print(f"[OK] {track_name} - {artist_name} (tags={len(found_tags)})")

                return {
                    "master_metadata_track_name": track_name,
                    "master_metadata_album_artist_name": artist_name,
                    "mbid": mbid,
                    "tags": found_tags if found_tags else [np.nan],
                }

        except Exception as e:
            print(
                f"[ERROR] {track_name} - {artist_name} (attempt {attempt}/{retries}): {e}"
            )
            await asyncio.sleep(2**attempt)  # exponential backoff

    return None


async def get_track_metadata_async(
    df: pd.DataFrame, api_key: str = API_KEY, concurrency: int = 10
) -> pd.DataFrame:
    """Fetch metadata for unique (track, artist) pairs asynchronously, with logging and concurrency control."""
    assert "master_metadata_track_name" in df.columns
    assert "master_metadata_album_artist_name" in df.columns

    seen_tracks = set()
    tasks = []

    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(concurrency)  # limit simultaneous requests

        async def bound_fetch(track_name, artist_name):
            async with sem:
                return await fetch_track(session, track_name, artist_name, api_key)

        for row in df[
            ["master_metadata_track_name", "master_metadata_album_artist_name"]
        ].itertuples(index=False):
            track_name, artist_name = row

            if not track_name or not artist_name:
                continue

            key = (track_name.lower().strip(), artist_name.lower().strip())
            if key in seen_tracks:
                continue
            seen_tracks.add(key)

            tasks.append(bound_fetch(track_name, artist_name))

        print(
            f"[START] Fetching {len(tasks)} unique tracks with concurrency={concurrency}..."
        )

        results = await asyncio.gather(*tasks)

    elapsed = time.time() - start_time
    print(
        f"[DONE] Retrieved {len([r for r in results if r])} tracks in {elapsed:.2f} seconds"
    )

    # Filter out None
    results = [res for res in results if res]
    return pd.DataFrame(results)
