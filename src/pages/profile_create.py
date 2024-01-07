## dash file for profile of the loaded data

import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output,State


dash.register_page(__name__, path='/profiler', name="Dataset Profiler")

layout = html.Div(children=[
    html.Br(),
    dcc.Input(id='file_path', type='text', placeholder='Enter the file path'),
    html.Button('Load File', id='execute-btn', n_clicks=0),
    html.P("Select Column:"),
    dcc.Dropdown(id="dist_column", value="Age", clearable=False),
    dcc.Graph(id="histogram")
])

# Empty DataFrame for global variable
load_db = pd.DataFrame()

@callback(
    Output('dist_column', 'options'),
    Output('dist_column', 'value'),
    [Input('execute-btn', 'n_clicks')],
    [State('file_path', 'value')]
)
def update_dropdown_options(n_clicks, file_path):
    global load_db
    if n_clicks > 0 and file_path:
        try:
            # Load data from the specified file path
            load_db = pd.read_csv(file_path)
            columns = [{'label': col, 'value': col} for col in load_db.columns]
            return columns, load_db.columns[0]
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # Return empty options and default value if no file path is provided or button not clicked
    return [], None

@callback(
    Output("histogram", "figure"),
    [Input("dist_column", "value")]
)
def update_histogram(dist_column):
    return px.histogram(data_frame=load_db, x=dist_column, height=600)
