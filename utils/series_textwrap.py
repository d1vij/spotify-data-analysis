import textwrap
from pandas import Series

def index_wrap(ser:Series, width:int):
    ser.index = [textwrap.fill(l, width=width) for l in ser.index.values]   #type: ignore