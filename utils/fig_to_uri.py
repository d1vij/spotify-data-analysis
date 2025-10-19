from io import BytesIO
from matplotlib.figure import Figure

FORMAT = "png"


# Matplotlib figure to dataUri
def get_uri(fig: Figure):
    if not isinstance(fig, Figure):
        raise TypeError("Passed object must be of type matplotlib.figure.Figure")
    buffer = BytesIO()
    fig.savefig(buffer, format=FORMAT)
    return buffer.getvalue().decode("utf-8")
