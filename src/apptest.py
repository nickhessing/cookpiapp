from dash import Dash, html
import pandas as pd

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div(id='nav', children=[html.Button('ToggleNavBar', id='toggleNav', className='toggle'),

        html.Div([html.Div('Light Mode', className='mode-text'),
        html.Button('Toggle DarkMode',className="toggle-switch")])]),
        html.Div([html.Button('Open Search', className="search-box"),
                  ], id='page-content')
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)