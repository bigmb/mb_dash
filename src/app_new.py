from dash import Dash,html, dash_table, dcc, Input, Output, State,callback
import dash
import plotly.express as px
import mt.pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, external_stylesheets=external_css)


columns = ['PCA','TSNE']

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
    html.Br(),
    html.Div(id='output-div'),
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
    dcc.Dropdown(id="data_table_profile", value="Column", clearable=False),
    dcc.Graph(id="histogram")

])
    

@callback(
    [Output('output-div', 'children'),
    Output('data_table_dataset', 'data'),
    Output('data_table_dataset', 'columns'),
    Output('data_table_profile', 'options'),
    Output('data_table_profile', 'value'),
    Output('histogram', 'figure')],
    [Input('run-button', 'n_clicks')],
    [State('file_path', 'value'),
    State('dropdown1', 'value'),
    State('taxcodes', 'value'),
    State('emb_column_name', 'value'),
    State('taxcode_column_name', 'value'),
    State('file_save', 'value')])
def run_function(n_clicks, file_path, dropdown1, taxcodes,emb_column_name,taxcode_column_name,file_save):
    if n_clicks is None:
        return "Click the 'Run' button after making selections.",[],[],[],[],{}

    if not any([file_path, dropdown1, taxcodes]):
        return "Please select at least one option or enter a string.",[],[],[],[],{}

    taxcode_list = list(i.strip() for i in taxcodes.split(','))
    
    print('file path is : ',file_path)
    print('taxcode list is : ',taxcode_list)
    print('embedding column name is : ',emb_column_name)
    t1 = pd.dfload(file_path)
    t1 = t1.dropna()
    t1 = t1.drop_duplicates()
    t1 = t1.reset_index(drop=True)
    print('length of the file is ; ',len(t1))

    if taxcode_column_name not in t1.columns:
        return "Please enter a valid taxcode column name",[],[],[],[],{}
    if emb_column_name not in t1.columns:
        return "Please enter a valid embedding column name",[],[],[],[],{}

    t1 =t1[[taxcode_column_name,emb_column_name,'after_image_url','before_image_url','event_id']]

    t1[taxcode_column_name] = t1[taxcode_column_name].isin(taxcode_list)
    t1 = t1[t1[taxcode_column_name] == True]
    
    print('length of the taxcode file is ; ',len(t1))
    print(t1.head())
    print('File loaded successfully. Starting the embedding process.')

    if dropdown1 == 'PCA':
        pca = PCA(n_components=2)
        pca_emb = pca.fit_transform(list(t1[emb_column_name]))
        temp_res = list(pca_emb)
        t1['emb_res'] = temp_res
    if dropdown1 == 'TSNE':
        tsne = TSNE(n_components=2)
        tsne_emb = tsne.fit_transform(list(t1[emb_column_name]))
        temp_res = list(tsne_emb)
        t1['emb_res'] = temp_res
    
    print('Embedding process completed. Saving the file.')
    # if dropdown1 == 'UMAP':
    #     umap_emb = umap.UMAP(n_components=2).fit_transform(list(t1[emb_column_name]))
    #     temp_res = list(umap_emb)
    #     t1['emb_res'] = temp_res
    
    t1.to_csv(file_save,index=False)
    print('File saved successfully.')

    return t1.to_dict('records'), [{'name': col, 'id': col} for col in t1.columns],t1.columns,t1.columns[0],px.histogram(data_frame=t1,x=t1.columns, height=600)





if __name__ == '__main__':
    app.run_server(port=8933,host='0.0.0.0',debug=True)