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

def load_data(file_path, taxcodes, emb_column_name='embedding', taxcode_column_name='taxcode', file_save = None):
    """
    Load the data from the file path.
    """
    df = pd.dfload(file_path)
    df = df[df[taxcode_column_name].isin(taxcodes)]

    assert df.columns.contains(emb_column_name), f"Embedding column name {emb_column_name} not found in the dataframe"
    assert df.columns.contains(taxcode_column_name), f"Taxcode column name {taxcode_column_name} not found in the dataframe"
    assert df.columns.contains('event_id'), f"Event_id column name not found in the dataframe"
    assert df.columns.contains('after_image_url'), f"After_image_url column name not found in the dataframe"
    assert df.columns.contains('before_image_url'), f"Before_image_url column name not found in the dataframe"

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
    


    
