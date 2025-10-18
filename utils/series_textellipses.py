from pandas import Series


def index_ellipses(ser:Series, characters: int):
    indexes = list(ser.index.copy(deep= True))

    for idx in range(len(indexes)):
        if(len(indexes[idx]) > characters):
            indexes[idx] = indexes[idx][:characters] + "..."
    
    ser.index = indexes
