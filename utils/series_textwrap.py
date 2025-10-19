import textwrap
from pandas import Series


# Wraps the series indexes to width number of characters
def index_wrap(ser: Series, width: int):
    # Series passed as reference
    ser.index = [textwrap.fill(l, width=width) for l in ser.index.values]  # type: ignore
