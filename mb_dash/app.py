from dash import Dash, html, dcc
import dash
import plotly.express as px
from dash.dependencies import Input, Output

px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css)

# app.layout = html.Div([
# 	html.Br(),
# 	html.P('Winnow Viz Web App', className="text-dark text-center fw-bold fs-1"),
#     html.Div(children=[
# 	    dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5")\
# 			  for page in dash.page_registry.values()]
# 	),
# 	dash.page_container
# ], className="col-8 mx-auto")

app.layout = html.Div([
    html.Br(),
    html.P('Winnow Viz Web App', className="text-dark text-center fw-bold fs-1"),
    html.Div(children=[
        dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5") \
        for page in dash.page_registry.values()
    ]),
    html.Div(id="page-content", className="col-8 mx-auto")
], className="col-8 mx-auto")

# Define callback to update page content based on URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/data_load/":
        return data_load.layout
    elif pathname == "/profiler/":
        return profiler.layout
    else:
        return "404 Page Not Found"



if __name__ == '__main__':
    app.run_server(mode='inline', port=8928,host='0.0.0.0')