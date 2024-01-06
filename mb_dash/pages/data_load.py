import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State


dash.register_page(__name__, path='/', name="Loading Dataset")

layout = html.Div([
    dcc.Dropdown(
        id='dropdown-1',
        options=[
            {'Type of ': 'Option 2', 'value': 'opt2'},
            {'label': 'Option 3', 'value': 'opt3'},
        ],
        multi=True,
        value=[],
    ),
    dcc.Input(id='file_path', type='text', placeholder='Enter the file path'),
    html.Button('Run Selection', id='run-button'),
    html.Div(id='output-div'),
])



@callback(
    Output('output-div', 'children'),
    [Input('run-button', 'n_clicks')],
    [State('dropdown-1', 'value'),
     State('file_path', 'value')]
)
def run_function(n_clicks, dropdown_1_values, dropdown_2_values, file_path):
    if n_clicks is None:
        return "Click the 'Run' button after making selections."

    if not any([dropdown_1_values, dropdown_2_values, file_path]):
        return "Please select at least one option or enter a string."

    # Run your custom function using the selected values and string input
    result = f"Dropdown 1 Selections: {', '.join(dropdown_1_values)}<br>"
    result += f"File Path: {file_path}"

    return result