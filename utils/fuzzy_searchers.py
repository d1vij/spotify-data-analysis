# Fuzzy searching artists / track name
from typing import Literal

import pandas as pd
from rapidfuzz import fuzz


# Fuzzy searcher searches for given word in a series, dataframe, or list of strings
# and return the closest matches sorted in descending order of confidence
# For searching within single worded sequences prefer partial ratio (example for artist names)
# and for multi word sequences prefer token set ratio (example Track names)
def fuzzy_search(
    phrase: str,
    sequence: pd.DataFrame | pd.Series | list[str],
    _search_type: Literal["partial ratio", "token set ratio"],
    *,
    confidence: int = 80,
    col_name: str | None = None,
    top_n=5,  # If negative, returns matched words
):
    search_type = 0 if (_search_type == "partial ratio") else 1

    if type(sequence) is pd.DataFrame:
        if col_name is None:
            raise ValueError("Must provide a columnn name to fuzzy search when sequence is a DataFrame")
        data = sequence[col_name].values

    elif type(sequence) is pd.Series:
        if col_name is not None:
            raise ValueError("Cannot provide a col_name if sequence is of type Series")
        data = sequence.values

    elif isinstance(sequence, list):
        data = sequence

    else:
        raise (TypeError(f"Type of sequence must be pd.Series, pd.Dataframe or list[str] and not {type(sequence)}"))

    if not isinstance(sequence[0], str):
        raise (TypeError("Values of sequence can only be of type string"))

    matched = []
    ratios = []
    print(data)
    for value in data:
        if value is not None:
            value = str(value)
            if search_type == 0:
                ratio = fuzz.partial_ratio(phrase.lower(), value.lower())
            else:
                ratio = fuzz.token_set_ratio(phrase.lower(), value.lower())

            if (ratio >= confidence) and (value not in matched):
                matched.append(value)
                ratios.append(ratio)

    artists = [
        value
        for value, _ in sorted(
            [(value, ratio) for value, ratio in zip(matched, ratios)],
            key=lambda p: p[1],
            reverse=True,
        )
    ]
    if top_n < 0:
        return artists
    else:
        return artists[:top_n]
