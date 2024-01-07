import pandas as pd
import dash
from dash import html, dash_table, dcc, Input, Output, State,callback
import plotly.graph_objects as go

dash.register_page(__name__, path='/dataset', name="Dataset Viewer")

# Initial empty DataFrame
load_db = pd.DataFrame()


layout = html.Div(children=[
    html.Br(),
    dcc.Input(id='file_path', type='text', placeholder='Enter the file path'),
    html.Button('Load File', id='execute-btn', n_clicks=0),
    dash_table.DataTable(
        id='data-table',
        data=load_db.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in load_db.columns],
        page_size=20,
        style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
        style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
    ),
])

# Callback to update DataTable on button click
@callback(Output('data-table', 'data'),
    [Input('execute-btn', 'n_clicks')],
    [State('file_path', 'value')])
def update_data_table(n_clicks, file_path):
    if n_clicks > 0 and file_path:
        try:
            # Load data from the specified file path
            global load_db
            load_db = pd.read_csv(file_path)
            return load_db.to_dict('records')
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # Return empty data if no file path is provided or button not clicked
    return []