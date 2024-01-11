from dash import Dash,html, dash_table, dcc, Input, Output, State,callback
import dash
import plotly.express as px
import mt.pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import argparse
import dash_ag_grid as dag


px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, external_stylesheets=external_css)

columns = ['PCA','TSNE']

def load_data(file_path, taxcodes, emb_column_name='embedding', taxcode_column_name='taxcode', file_save = None):
    """
    Load the data from the file path.
    """
    df = pd.dfload(file_path)
    df = df[df[taxcode_column_name].isin(taxcodes)]

    assert emb_column_name in df.columns, f"Embedding column name {emb_column_name} not found in the dataframe"
    assert taxcode_column_name in df.columns, f"Taxcode column name {taxcode_column_name} not found in the dataframe"
    assert 'event_id' in df.columns, f"Event_id column name not found in the dataframe"
    assert 'after_image_url' in df.columns, f"After_image_url column name not found in the dataframe"
    assert 'before_image_url' in df.columns, f"Before_image_url column name not found in the dataframe"

    df = df[['event_id','after_image_url','before_image_url',emb_column_name, taxcode_column_name]]
    df = df.rename(columns={emb_column_name: "embedding", taxcode_column_name: "taxcode"})

    if file_save:
        df.to_csv(file_save, index=False)
    return df

def dim_red(file, method='pca', n_components=2,file_save_emb='/home/malav/emb_res.csv'):
    """
    Dimensionality reduction using 'pca' or 'tsne'.
    """
    if method == 'pca':
        pca = PCA(n_components=n_components)
        pca_result = pca.fit_transform(file['embedding'].tolist())
        file['pca1'] = pca_result[:,0]
        file['pca2'] = pca_result[:,1]
        if n_components == 3:
            file['pca3'] = pca_result[:,2]
        file.drop(columns=['embedding'], inplace=True)
        if file_save_emb:
            file.to_csv(file_save_emb, index=False)
        return file
    
    elif method == 'tsne':
        tsne = TSNE(n_components=n_components, verbose=1, perplexity=40, n_iter=300)
        tsne_results = tsne.fit_transform(file['embedding'].tolist())
        file['tsne1'] = tsne_results[:,0]
        file['tsne2'] = tsne_results[:,1]
        if n_components == 3:
            file['tsne3'] = tsne_results[:,2]
        file.drop(columns=['embedding'], inplace=True)
        if file_save_emb:
            file.to_csv(file_save_emb, index=False)
        return file
    
    else:
        raise ValueError(f"Method {method} not supported. Please choose between 'pca' and 'tsne'")
    

def plot(df, method='pca', n_components=2, color='taxcode', file_save_plot=None):
    """
    Method to plot the embeddings.
    """
    if method == 'pca':
        fig = px.scatter(df, x="pca1", y="pca2", color=color, hover_data=['event_id','before_image_url','after_image_url'])
        if n_components == 3:
            fig = px.scatter_3d(df, x="pca1", y="pca2", z="pca3", color=color, hover_data=['event_id','before_image_url','after_image_url'])
        if file_save_plot:
            fig.write_html(file_save_plot)
        return fig
    
    elif method == 'tsne':
        fig = px.scatter(df, x="tsne1", y="tsne2", color=color, hover_data=['event_id','before_image_url','after_image_url'])
        if n_components == 3:
            fig = px.scatter_3d(df, x="tsne1", y="tsne2", z="tsne3", color=color, hover_data=['event_id','before_image_url','after_image_url'])
        if file_save_plot:
            fig.write_html(file_save_plot)
        return fig
    
    else:
        raise ValueError(f"Method {method} not supported. Please choose between 'pca' and 'tsne'")
    

def app_layout(grid,dropdown,plot1):
    layout = html.Div(children=[
    html.Br(),
    html.H1(children='Embedding Visualizer', style={'text-align': 'center'}),
    html.Br(),
    #html.Button('Load Data', id='load_data', n_clicks=0, style={'margin-left': '10px'}),
    html.P("Select Column:"),
    #dcc.Dropdown(id="data_table_profile", value="Column", clearable=False),
    grid,
    html.Br(),
    #dcc.Graph(id="histogram"),
    dropdown,
    html.Br(),
    plot1,
    html.Div(id='embeddings plot'),
    html.Br(),
    #html.Graph(id='plot'),
    ])

    return layout

# def app_callbacks(app):
#     @app.callback(
#         [Output("data_table_profile", "options"),
#         Output("data_table_profile", "value")]
#         [Input("load_data", "n_clicks")],
#         prevent_initial_call=True,
#     )
#     def update_data_table_profile(n_clicks):
#         if n_clicks == 0:

#             return [{"label": col, "value": col} for col in columns]

#     @app.callback(
#         Output("histogram", "figure"),
#         [Input("dropdown", "value")],)
#     def update_histogram(column):
#         return px.histogram(data_frame=dim_red_file['data1'],x=dim_red_file['data1_cols'], height=600)


def main(args):
    file_path = args.file_path
    taxcodes = args.taxcodes
    emb_column_name = args.emb_column_name
    taxcode_column_name = args.taxcode_column_name
    file_save = args.file_save
    method = args.method
    n_components = args.n_components
    color = args.color
    file_save_plot = args.file_save_plot
    file_save_emb = args.file_save_emb
    port = args.port
    host = args.host
    debug = args.debug

    loaded_file = load_data(file_path, taxcodes, emb_column_name,taxcode_column_name,file_save)
    dim_red_file = dim_red(loaded_file, method=method, n_components=n_components,file_save_emb=file_save_emb)

    cols = dim_red_file.columns.tolist()

    grid = dag.AgGrid(
        id='grid',
        columnDefs= [{"headerName": x, "field": x, } for x in dim_red_file.columns],
        rowData=dim_red_file.to_dict('records'),
        dashGridOptions={'pagination':True},)

    dropdown = dcc.Dropdown(cols, id='dropdown', clearable=False, value=cols[0])

    plot1 = dcc.Graph(id="histogram")

    app.layout = app_layout(grid,dropdown,plot1)

    # @app.callback(
    #     [Output("data_table_profile", "options"),
    #     Output("data_table_profile", "value")]
    #     [Input("load_data", "n_clicks")],
    #     prevent_initial_call=True,
    # )
    # def update_data_table_profile(n_clicks):
    #     if n_clicks == 0:

    #         return [{"label": col, "value": col} for col in columns]
    
    @app.callback(
        Output("histogram", "figure"),
        [Input("dropdown", "value")],)
    def update_histogram(value):
        return px.histogram(data_frame=dim_red_file,x=dim_red_file[value], height=600)

    app.run_server(port=port,host=host,debug=debug)




# @app.callback(Output("data_table_profile", "options"), 
#               [Input("load_data", "n_clicks")])
# def update_data_table_profile(n_clicks):
#     if n_clicks > 0:

#         return [{"label": col, "value": col} for col in columns]
#     else:
#         return [{"label": col, "value": col} for col in columns]

# @callback(
#     Output("histogram", "figure"),
#     [Input("store", "data")]
# )
# def update_histogram(data):
#     return px.histogram(data_frame=data['data1'],x=data['data1_cols'], height=600)
    


if __name__ == '__main__':
    parcer = argparse.ArgumentParser()
    parcer.add_argument('--port', type=int, default=8935)
    parcer.add_argument('--host', type=str, default='0.0.0.0')
    parcer.add_argument('--debug', type=bool, default=True)
    parcer.add_argument('--file_path', type=str, default='/home/malav/dash_test_1000.csv')
    parcer.add_argument('--taxcodes', type=list, default=['W000E'])
    parcer.add_argument('--emb_column_name', type=str, default='embeddings')
    parcer.add_argument('--taxcode_column_name', type=str, default='taxcode')
    parcer.add_argument('--file_save', type=str, default=None)
    parcer.add_argument('--file_save_emb', type=str, default=None)
    parcer.add_argument('--method', type=str, default='pca')
    parcer.add_argument('--n_components', type=int, default=2)
    parcer.add_argument('--color', type=str, default='taxcode')
    parcer.add_argument('--file_save_plot', type=str, default=None)
    args = parcer.parse_args()

    main(args)

