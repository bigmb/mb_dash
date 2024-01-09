## dash file for profile of the loaded data

import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output,State

dash.register_page(__name__, path='/profiler', name="Dataset Profiler")

layout = html.Div(children=[
    html.Br(),
    #dcc.Input(id='file_path_profiler', type='text', placeholder='Enter the file path'),
    #html.Button('Load File', id='execute_profie', n_clicks=0),
    html.P("Select Column:"),
    #dcc.Dropdown(id="dist_column_profiler", value="Column", clearable=False),
    dcc.Dropdown(id="data_table_profile", value="Column", clearable=False),
    dcc.Graph(id="histogram")
])

# Empty DataFrame for global variable
# load_db_profiler = pd.DataFrame(columns=['test_A', 'test_B', 'test_C'])

# @callback(
#     #Output('dist_column_profiler', 'options'),
#     #Output('dist_column_profiler', 'value'),
#     [Output("data_table_profile", "options"),
#     Output("data_table_profile", "value"),],
#     [Input('execute_profie', 'n_clicks')],
#     [State('file_path_profiler', 'value')]
# )
# def update_dropdown_options(n_clicks, file_path_profiler):
#     global load_db_profiler
#     if n_clicks > 0 and file_path_profiler:
#         try:
#             # Load data from the specified file path
#             load_db_profiler = pd.read_csv(file_path_profiler)
#             columns = [{'label': col, 'value': col} for col in load_db_profiler.columns]
#             return columns, load_db_profiler.columns[0]  if columns else None
#         except Exception as e:
#             print(f"Error loading data: {e}")
    
#     # Return empty options and default value if no file path is provided or button not clicked
#     return [], None

@callback(
    Output("histogram", "figure"),
    #[Input("dist_column_profiler", "value")
    [Input("store", "data")]
)
def update_histogram(data):
    return px.histogram(data_frame=data['data1'],x=data['data1'].columns, height=600)
