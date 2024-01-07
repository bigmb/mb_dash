import pandas as pd
import dash
from dash import html, dash_table, dcc, Input, Output, State,callback
import plotly.express as px


dash.register_page(__name__, path='/new_profiler', name="Dataset Viewer New")

## Initial empty DataFrame
load_db_dataset = pd.DataFrame(columns=['test_A', 'test_B', 'test_C'])

layout = html.Div(children=[
    html.Br(),
    dcc.Input(id='file_path_new', type='text', placeholder='Enter the file path'),
    html.Button('Load File', id='execute_dataset_new', n_clicks=0),
    html.Br(),
    html.P("Select Column:"),
    dcc.Dropdown(id="data_table_new_col", value="Column", clearable=False),
    dcc.Graph(id="histogram_new"),
    dash_table.DataTable(
        id='data_table_new',
        data=[],  # Use the stored dataset
        columns = [],
        page_size=20,
        style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
        style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
    ),
])


# Empty DataFrame for global variable
load_db_profiler = pd.DataFrame(columns=['test_A', 'test_B', 'test_C'])

@callback([Output("data_table_new_col", "options"),
    Output("data_table_new_col", "value"),
    Output("data_table_new", "data"),
    Output("data_table_new", "columns"),],
    [Input('execute_profie_new', 'n_clicks')],
    [State('file_path_new', 'value')]
)
def update_dropdown_options(n_clicks, file_path_profiler):
    global load_db_profiler
    if n_clicks > 0 and file_path_profiler:
        try:
            # Load data from the specified file path
            load_db_profiler = pd.read_csv(file_path_profiler)
            columns = [{'label': col, 'value': col} for col in load_db_profiler.columns]
            return columns, load_db_profiler.columns[0] , load_db_dataset.to_dict('records'),columns if load_db_dataset is not None else []
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # Return empty options and default value if no file path is provided or button not clicked
    return [], None, [],[]

@callback(
    Output("histogram_new", "figure"),
    [Input("data_table_new", "value")]
)
def update_histogram(dist_column):
    return px.histogram(data_frame=load_db_profiler, x=dist_column, height=600)


# Callback to update DataTable using the stored data
@callback([Output('data_table_new', 'data'),
           Output('data_table_new', 'columns'),],
          [Input('data_table_new', 'data')])
def update_data_table(loaded_dataset):
    if loaded_dataset:
        # Get updated columns based on the loaded dataset
        updated_columns = [{'name': col, 'id': col} for col in loaded_dataset[0].keys()]
        
        # Return data and updated columns
        return loaded_dataset, updated_columns
    
    # Return empty data and columns if no dataset is stored
    return [], []
