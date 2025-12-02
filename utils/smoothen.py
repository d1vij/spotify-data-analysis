import warnings

import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline


# Smoothens the data of series by applying spline function over it
# More the "amount", more smoother the curve would be
# and more time it would take to generate the interpolation
def smoothen(ser: pd.Series, amount: int):
    if amount > 1e5:
        warnings.warn("Reconsider the amount since it might cause large runtimes")  # lmao

    spline = make_interp_spline(ser.index, ser.values)
    x_points = np.linspace(ser.index.min(), ser.index.max(), amount, endpoint=True)
    y_points = spline(x_points)
    return pd.Series(y_points, index=x_points)
