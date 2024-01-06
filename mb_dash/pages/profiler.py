## dash file for profile of the loaded data

import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output,State


dash.register_page(__name__, path='/', name="Dataset Profiler")

#def create_distribution(col_name="Age"):
#    return px.histogram(data_frame=None, x=col_name, height=600)

# columns = ["Age", "Fare", "SibSp", "Parch", "Survived", "Pclass", "Sex", "Embarked", "Cabin"]
# dd = dcc.Dropdown(id="dist_column", options=columns, value="Age", clearable=False)

# layout = html.Div(children=[
#     html.Br(),
#     html.P("Select Column:"),
#     dd,
#     dcc.Graph(id="histogram")
# ])

#@callback(Output("histogram", "figure"), [Input("dist_column", "value"), ])
#def update_histogram(dist_column):
#    return create_distribution(dist_column)


layout = html.Div([
    dcc.Input(id='file_path', type='text', placeholder='Enter the file path'),
    dcc.Dropdown(
        id='dropdown-1',
        options=[
            {'label ': '', 'value': 'opt1'},
            {'label': 'Option 3', 'value': 'opt1'},
        ],
        multi=True,
        value=[],
    ),
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