from dash import Dash,html, dash_table, dcc, Input, Output, State,callback
import dash
import plotly.express as px
import pandas as pd

px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, external_stylesheets=external_css)


columns = ['PCA','TSNE','UMAP']

app.layout = html.Div([
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
    html.Br(),
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
    
    return {'data1': t1.to_dict('records')}


@callback([Output('data_table_dataset', 'data'),
           Output('data_table_dataset', 'columns')],
            [Input('output-div', 'children')])
def update_data_table(data):
    if data['data1']:
        new_data = data['data1']
        return new_data , [{'name': col, 'id': col} for col in new_data[0].keys()]
    print('empty data')
    return [], []
    





if __name__ == '__main__':
    app.run_server(port=8933,host='0.0.0.0',debug=True)