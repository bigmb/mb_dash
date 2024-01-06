## File for dimensionality reduction functions

import umap
from mb import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from typing import Optional

__all__ = ['get_emb']

def get_emb(df: pd.DataFrame, emb: str= 'embeddings', emb_type: str='umap', dim: int=2,
            keep_original_emb: Optional[bool]=False,file_save=None, logger: Optional[None] =None,**kwargs):
    """
    Visualize embeddings in 2d or 3d with tf projector and plotly

    Args:
        df (pd.DataFrame): dataframe containing embeddings. File location or DataFrame object.
        emb (str): name of embedding column
        emb_type (str, optional): embedding type. Defaults to 'umap'.
        dim (int, optional): embedding dimension. Defaults to 2.
        keep_original_emb (bool, optional): keep original embedding column. Defaults to False.
        file_save (str, optional): file location to save embeddings csv. Defaults to None.
    Output:
        df (pd.DataFrame): dataframe containing embeddings. Original embedding column is dropped.
    """
    
    if type(df) is not pd.DataFrame:
        if logger:
            logger.info('Type of df :{}'.format(str(type(df))))
        df = pd.load_any_df(df)
        if logger:
            logger.info('Loaded dataframe from path {}'.format(str(df)))
    
    if logger:
        logger.info('Data shape {}'.format(str(df.shape)))
        logger.info('Data columns {}'.format(str(df.columns)))
        logger.info('Performing {} on {} embeddings'.format(emb_type,emb))
    
    if emb_type=='pca':
        pca = PCA(n_components=dim)
        pca_emb = pca.fit_transform(list(df[emb]))
        if logger:
            logger.info('First PCA transform result : {}'.format(str(pca_emb[0])))
        temp_res = list(pca_emb)
    
    if emb_type=='tsne':
        tsne = TSNE(n_components=dim, verbose=1, perplexity=30, n_iter=250, **kwargs)
        df[emb] = df[emb].apply(lambda x: np.array(x))
        k1 = np.vstack(df[emb])
        tsne_emb = tsne.fit_transform(k1)
        if logger:
            logger.info('First TSNE transform result : {}'.format(str(tsne_emb[0])))
        temp_res = list(tsne_emb)
    
    if emb_type=='umap':
        umap_emb = umap.UMAP(n_components=2,**kwargs).fit_transform(list(df[emb]))
        if logger:
            logger.info('First UMAP transform result : {}'.format(str(umap_emb[0])))
        temp_res = list(umap_emb)
    
    df['emb_res'] = temp_res
    if keep_original_emb==False:
        df.drop(emb,axis=1,inplace=True)
        if logger:
            logger.info('Dropped original embedding column')
            
    if file_save:
        df.to_csv(file_save + '/emb_res.csv',index=False)
    else:
        df.to_csv('./emb_res.csv',index=False)
    
    return df