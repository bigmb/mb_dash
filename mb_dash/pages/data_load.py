import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State


dash.register_page(__name__, path='/', name="Loading Dataset")

layout = html.Div([
    dcc.Input(id='file_path', type='text', placeholder='Enter the file path'),
    dcc.Dropdown(
        id='dropdown1',
        options=[
            {'label ': ' ', 'value': 'opt1'},
            {'label ': 'PCA', 'value': 'opt2'},
            {'label': 'TSNE', 'value': 'opt3'},
            {'label': 'UMAP', 'value': 'opt4'},            
        ],
        multi=True,
        value=[],
    ),
    dcc.Input(id='taxcodes', type='text', placeholder='Enter the taxcodes separated by comma'),
    html.Button('Run Selection', id='run-button'),
    html.Div(id='output-div'),
])


@callback(
    Output('output-div', 'children'),
    [Input('run-button', 'n_clicks')],
    [State('file_path', 'value'),
    State('dropdown1', 'value'),
    State('taxcodes', 'value')])
def run_function(n_clicks, file_path, dropdown1, taxcodes):
    if n_clicks is None:
        return "Click the 'Run' button after making selections."

    if not any([file_path, dropdown1, taxcodes]):
        return "Please select at least one option or enter a string."

    # Run your custom function using the selected values and string input
    result = f"File Path: {file_path}"
    result += f"Dropdown Selection: {', '.join(dropdown1)}<br>"
    result += f"Tacodes: {list(i.strip() for i in taxcodes.split(','))}"

    return result