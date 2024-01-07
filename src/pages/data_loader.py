import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import pandas as pd

dash.register_page(__name__, path='/data_load', name="Loading Dataset")

columns = ['PCA','TSNE','UMAP']

layout = html.Div([
    dcc.Input(id='file_path', type='text', placeholder='Enter the file path'),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id="dropdown1", options=columns, value="PCA", clearable=False),
    html.Br(),
    html.Br(),
    dcc.Input(id='taxcodes', type='text', placeholder='Enter the taxcodes separated by comma'),
    html.Br(),
    html.Br(),
    dcc.Input(id='emb_column_name', type='text', placeholder='Enter the embedding column name'),
    html.Br(),
    html.Br(),
    dcc.Input(id='taxcode_column_name', type='text', placeholder='Enter the taxcodes column name'),
    html.Br(),
    html.Br(),
    dcc.Input(id='file_save', type='text', placeholder='Enter the file save name with .csv extension'),
    html.Br(),
    html.Br(),
    html.Button('Run Selection', id='run-button'),
    html.Div(id='output-div'),
])

def run_all(x):
    if type(x) is pd.DataFrame:
        x1 = x.copy()
        return x1
    else:
        return "Please select pandas df"
    

@callback(
    Output('output-div', 'children'),
    [Input('run-button', 'n_clicks')],
    [State('file_path', 'value'),
    State('dropdown1', 'value'),
    State('taxcodes', 'value'),
    State('emb_column_name', 'value'),
    State('taxcode_column_name', 'value'),
    State('file_save', 'value')])
def run_function(n_clicks, file_path, dropdown1, taxcodes,emb_column_name,taxcode_column_name,file_save):
    if n_clicks is None:
        return "Click the 'Run' button after making selections."

    if not any([file_path, dropdown1, taxcodes]):
        return "Please select at least one option or enter a string."

    taxcode_list = list(i.strip() for i in taxcodes.split(','))
     
    global t1
    t1 = pd.read_csv(file_path)
    t1 = t1.dropna()
    t1 = t1.drop_duplicates()
    t1 = t1.reset_index(drop=True)
    t1[taxcode_column_name] = t1[taxcode_column_name].isin(taxcode_list)
    t1 = t1[t1[taxcode_column_name] == True]
    
    t1.to_csv(file_save,index=False)
    
    run_all(t1)
    return "File saved successfully"