from io import BytesIO
from matplotlib.figure import Figure
FORMAT = "png"

def get_uri(fig:Figure):
    if(not isinstance(fig, Figure)):
        raise TypeError("Passed object must be of type matplitlib.figure.Figure")
    
    buffer = BytesIO()
    fig.savefig(buffer, format=FORMAT)
    return buffer.getvalue().decode("utf-8")
    