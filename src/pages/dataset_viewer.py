import pandas as pd
import dash
from dash import html, dash_table, dcc, Input, Output, State,callback

dash.register_page(__name__, path='/dataset', name="Dataset Viewer")

## Initial empty DataFrame
load_db_dataset = pd.DataFrame(columns=['test_A', 'test_B', 'test_C'])

layout = html.Div(children=[
    html.Br(),
    dcc.Input(id='file_path_dataset_viewer', type='text', placeholder='Enter the file path'),
    html.Button('Load File', id='execute_dataset', n_clicks=0),
    dcc.Store(id='loaded-dataset-store', storage_type='memory'),
    dash_table.DataTable(
        id='data_table_dataset',
        data=[],  # Use the stored dataset
        #data=load_db_dataset.to_dict('records'),
        #columns=[{'name': col, 'id': col} for col in load_db_dataset.columns],
        columns = [],
        page_size=20,
        style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
        style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
    ),
])


# Callback to store the loaded dataset in memory
@callback(Output('loaded-dataset-store', 'data'),
          [Input('execute_dataset', 'n_clicks')],
          [State('file_path_dataset_viewer', 'value')])
def store_data_in_memory(n_clicks, file_path_dataset_viewer):
    if n_clicks > 0 and file_path_dataset_viewer:
        try:
            # Load data from the specified file path
            load_db_dataset = pd.read_csv(file_path_dataset_viewer)
            print('Loaded dataset')
            
            # Store the loaded dataset in memory
            return load_db_dataset.to_dict('records') if load_db_dataset is not None else []
        except Exception as e:
            print(f"Error loading data: {e}")
    
    # Return empty data if no file path is provided or button not clicked
    print('empty data')
    return []

# Callback to update DataTable using the stored data
@callback([Output('data_table_dataset', 'data'),
           Output('data_table_dataset', 'columns')],
          [Input('loaded-dataset-store', 'data')])
def update_data_table(loaded_dataset):
    if loaded_dataset:
        # Get updated columns based on the loaded dataset
        updated_columns = [{'name': col, 'id': col} for col in loaded_dataset[0].keys()]
        
        # Return data and updated columns
        return loaded_dataset, updated_columns
    
    # Return empty data and columns if no dataset is stored
    return [], []


# @callback([Output('data_table_dataset', 'data'),
#            Output('data_table_dataset', 'columns'),
#            Output('loaded-dataset-store', 'data')],
#           [Input('execute_dataset', 'n_clicks')],
#           [State('file_path_dataset_viewer', 'value'),
#            State('loaded-dataset-store', 'data')])
# def update_data_table(n_clicks, file_path_dataset_viewer, loaded_dataset):
#     if n_clicks > 0 and file_path_dataset_viewer:
#         try:
#             # Load data from the specified file path
#             load_db_dataset = pd.read_csv(file_path_dataset_viewer)
#             print('Loaded dataset')
            
#             # Get updated columns based on the loaded dataset
#             updated_columns = [{'name': col, 'id': col} for col in load_db_dataset.columns]
            
#             # Return data, updated columns, and store the loaded dataset
#             return load_db_dataset.to_dict('records') if load_db_dataset is not None else [], updated_columns, load_db_dataset.to_dict('records')
#         except Exception as e:
#             print(f"Error loading data: {e}")
    
#     # Return empty data, columns, and the stored dataset if no file path is provided or button not clicked
#     print('empty data')
#     return [], [], loaded_dataset if loaded_dataset else []


# @callback([Output('data_table_dataset', 'data'),
#            Output('data_table_dataset', 'columns')],
#           [Input('execute_dataset', 'n_clicks')],
#           [State('file_path_dataset_viewer', 'value')])
# def update_data_table(n_clicks, file_path_dataset_viewer):
#     if n_clicks > 0 and file_path_dataset_viewer:
#         try:
#             global load_db_dataset
#             load_db_dataset = pd.read_csv(file_path_dataset_viewer)
#             print('Loaded dataset')
            
#             # Get updated columns based on the loaded dataset
#             updated_columns = [{'name': col, 'id': col} for col in load_db_dataset.columns]
            
#             # Return data and updated columns
#             return load_db_dataset.to_dict('records') if load_db_dataset is not None else [], updated_columns
#         except Exception as e:
#             print(f"Error loading data: {e}")
    
#     # Return empty data and columns if no file path is provided or button not clicked
#     print('empty data')
#     return [], []
