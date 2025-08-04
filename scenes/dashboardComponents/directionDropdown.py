from dash import html, dcc
import dash_bootstrap_components as dbc

direction_dropdown = html.Div([
    dbc.DropdownMenu([
        dcc.Checklist(
            id='direction-filter',
            options=[
                {'label': 'N', 'value': 'N'},
                {'label': 'NE', 'value': 'NE'},
                {'label': 'E', 'value': 'E'},
                {'label': 'SE', 'value': 'SE'},
                {'label': 'S', 'value': 'S'},
                {'label': 'SW', 'value': 'SW'},
                {'label': 'W', 'value': 'W'},
                {'label': 'NW', 'value': 'NW'},
            ],
            value=['N','NE','E','SE','S','SW','W','NW'],
            labelStyle={'display': 'block'},
            inputStyle={"margin-right": "5px"},
            style={"overflow-y": "scroll", "height": "200px"},
            className='ml-1'
        ),
    ],
        id='direction-dropdown',
        direction="up",
        label="All Pass Directions Selected",
        color="black",
        className='mb-1',
        toggle_style={'width': '100%'},
        style={'borderColor': 'black'}
    )]
)