## dash file for profile of the loaded data

import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output,State


dash.register_page(__name__, path='/profiler', name="Dataset Profiler")

#def create_distribution(col_name="Age"):
#    return px.histogram(data_frame=None, x=col_name, height=600)

columns = ["Age", "Fare", "SibSp", "Parch", "Survived", "Pclass", "Sex", "Embarked", "Cabin"]
dd = dcc.Dropdown(id="dist_column", options=columns, value="Age", clearable=False)

layout = html.Div(children=[
    html.Br(),
    html.P("Select Column:"),
    dd,
    dcc.Graph(id="histogram")
])

#@callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
#def update_histogram(dist_column):
#    return create_distribution(dist_column)


