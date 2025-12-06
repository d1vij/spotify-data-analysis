from pandas import Series


# Clips and appends ellipses (...) for string values in series greater than characters
def index_ellipses(ser: Series, characters: int):
    # if ser.dtype != "O":
    #     raise ValueError("Can only pass series with strings")

    indexes: list[str] = list(ser.index.copy(deep=True))
    for idx in range(len(indexes)):
        if len(indexes[idx]) > characters:
            indexes[idx] = indexes[idx][:characters] + "..."

    ser.index = indexes
