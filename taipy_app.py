import numpy as np
import plotly.graph_objs as go
from taipy.gui import Gui

# Create the Plotly figure (graph)
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Sin Curve"))

# Create the Taipy page
page = """
# My Graph

This is a dynamic graph rendered by Taipy.

<|{fig}|chart|>
"""

# Initialize and run the Taipy GUI
gui = Gui(page=page)
gui.run(title="Taipy App", host="0.0.0.0", port=5001, dark_mode=False)
