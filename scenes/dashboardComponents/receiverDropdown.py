from dash import html, dcc
import dash_bootstrap_components as dbc

receiver_dropdown = html.Div([
    dbc.DropdownMenu([
        dcc.Checklist(
            id='receiver-filter',
            options=[],
            value=[],
            labelStyle={'display': 'block'},
            inputStyle={"margin-right": "5px"},
            style={"overflow-y": "scroll", "height": "200px"},
            className='ml-1'
        ),
    ],
        id='receiver-dropdown',
        direction="up",
        label="All Receivers Selected",
        color="black",
        className='mb-1',
        toggle_style={'width': '100%'}
    )]
)