import textwrap
from pandas import Series

def index_wrap(ser:Series, width:int):
    # Wraps the series indexes to width number of characters
    # Series passed as reference
    ser.index = [textwrap.fill(l, width=width) for l in ser.index.values]   #type: ignore
