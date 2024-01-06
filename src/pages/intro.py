import dash
from dash import html

dash.register_page(__name__, path='/', name="Use Guide")

layout = html.Div(children=[
    html.Div(children=[
        html.H2("Visualize Embeddings Tool"),
        html.P("This tool is used to visualize the embeddings of the dataset."),
    ]),
    html.Div(children=[
        html.Br(),
        html.H3("Step 1 :Loading Dataset"),
        html.B("File path: "), "Enter the file path of the csv/parquet file",
        html.Br(),
        html.B("Dropdown : "), "Select the type of embedding to be used",
        html.Br(),
        html.B("Taxcodes : "), "Taxcodes to be used for filtering the dataset",
        html.Br(),
        html.B("Embedding column name :"), "Name of the column containing the embeddings",
        html.Br(),
        html.B("Taxcode column name : "), "Name of the column containing the taxcodes",
        html.Br(),
        html.B("File save name : "), "Name of the file to be saved with .csv extension",
        html.Br(),
    ]),
    html.Div(children=[
        html.Br(),
        html.H3("Step 2 : Check the Profiler"),
        html.B("File Path: "), "Enter the file path of the csv/parquet file",
        html.P("This step is used to check the data/distribution of the dataset. This step is optional."),
        html.Br(),
    ]),
    html.Div(children=[
        html.Br(),
        html.H3("Step 3 : Visualize the Embeddings"),])
    
], className="bg-light p-4 m-2")