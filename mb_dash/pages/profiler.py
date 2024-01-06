## dash file for profile of the loaded data

import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State


dash.register_page(__name__, path='/', name="Dataset Profiler")