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
    dash_table.DataTable(
        id='data_table_dataset',
        data=[],  
        #data=load_db_dataset.to_dict('records'),
        #columns=[{'name': col, 'id': col} for col in load_db_dataset.columns],
        columns =[],
        page_size=20,
        style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
        style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
    ),
    ])


# Callback to store the loaded dataset in memory
@callback(Output('store', 'data'),
        [Input('execute_dataset', 'n_clicks')],
        [State('file_path_dataset_viewer', 'value')])
def store_data_in_memory(n_clicks, file_path_dataset_viewer):
    if n_clicks > 0 and file_path_dataset_viewer:
        try:
            load_db_dataset_new = pd.read_csv(file_path_dataset_viewer)
            print('Loaded dataset')
            
            return load_db_dataset_new.to_dict('records') if load_db_dataset_new is not None else []
        except Exception as e:
            print(f"Error loading data: {e}")
    # print('empty data')
    return []

#Callback to update DataTable using the stored data
@callback([Output('data_table_dataset', 'data'),
           Output('data_table_dataset', 'columns')],
          [Input('store', 'data'),
           Input('execute_dataset', 'n_clicks')],)
def update_data_table(data,n_clicks):
    if n_clicks > 0:
        print('updated data table n_click')
        print(n_clicks)
        new_data = pd.DataFrame(data)

        return new_data.to_dict('records'), [{'name': col, 'id': col} for col in new_data.columns]

    elif n_clicks == 0:
        print('updated data table')
        new_data = pd.DataFrame(data)

        return new_data.to_dict('records'), [{'name': col, 'id': col} for col in new_data.columns]
    return data.to_dict('records'), [{'name': col, 'id': col} for col in data.columns]

        #return new_data , [{'name': col, 'id': col} for col in new_data[0].keys()]
    # if loaded_dataset:
    #     # Get updated columns based on the loaded dataset
    #     updated_columns = [{'name': col, 'id': col} for col in loaded_dataset[0].keys()]
        
    #     # Return data and updated columns
    #     return loaded_dataset, updated_columns


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

