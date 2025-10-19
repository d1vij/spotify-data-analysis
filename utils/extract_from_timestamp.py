import re
from typing import Literal

timestamp_regex = r"^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z$"
pattern = re.compile(timestamp_regex)


# 2020-11-27T07:19:29Z
def extract_from_timestamp(
    what: Literal[
        "year", "month", "day", "date", "hour", "minute", "seconds", "time-24"
    ],
    timestamp: str,
):
    m = re.match(pattern, timestamp)
    if m is None:
        raise ValueError("Cannot find match in timestamp " + timestamp)
    match what:
        case "year":
            return m.group(1)
        case "month":
            return m.group(2)
        case "day":
            return m.group(3)
        case "date":
            return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        case "hour":
            return m.group(4)

        case "minute":
            return m.group(5)
        case "seconds":
            return m.group(6)
        case "time-24":
            return f"{m.group(4)}:{m.group(5)}:{m.group(6)}"
