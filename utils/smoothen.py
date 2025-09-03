from scipy.interpolate import make_interp_spline
import pandas as pd
import numpy as np

def smoothen(ser: pd.Series, amount: int):
    # Smoothen a to-be-plotted series with indexes as x values and values as y values

    if(amount > 1e5):
        raise RuntimeError("Reconsider the amount since it might cause large runtimes")
    spline = make_interp_spline(ser.index, ser.values)
    x_points = np.linspace(ser.index.min(), ser.index.max(), amount, endpoint=True)
    y_points = spline(x_points)
    return pd.Series(y_points, index=x_points)
