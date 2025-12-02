import pandas as pd

df_or_series = pd.DataFrame | pd.Series


# Filters to filter row data based on values
class Filters:
    @staticmethod
    def rows_gt(value: int | float, obj: df_or_series):
        if type(obj) is pd.Series:
            return obj[obj > value]
        elif type(obj) is pd.DataFrame:
            return obj[(obj > value).all(axis=1)]
        else:
            raise TypeError("Can filter only Series or DataFrame objects")

    @staticmethod
    def rows_lt(value: int | float, obj: df_or_series):
        if type(obj) is pd.Series:
            return obj[obj < value]
        elif type(obj) is pd.DataFrame:
            return obj[(obj < value).all(axis=1)]
        else:
            raise TypeError("Can filter only Series or DataFrame objects")

    @staticmethod
    def rows_lteq(value: int | float, obj: df_or_series):
        if type(obj) is pd.Series:
            return obj[obj <= value]
        elif type(obj) is pd.DataFrame:
            return obj[(obj <= value).all(axis=1)]
        else:
            raise TypeError("Can filter only Series or DataFrame objects")

    @staticmethod
    def rows_gteq(value: int | float, obj: df_or_series):
        if type(obj) is pd.Series:
            return obj[obj >= value]
        elif type(obj) is pd.DataFrame:
            return obj[(obj >= value).all(axis=1)]
        else:
            raise TypeError("Can filter only Series or DataFrame objects")

    @staticmethod
    def non_zero_rows(obj: df_or_series):
        if type(obj) is pd.Series:
            return obj[obj != 0]
        elif type(obj) is pd.DataFrame:
            return obj[(obj != 0).any(axis=1)]
        else:
            raise TypeError("Can filter only Series or DataFrame objects")
