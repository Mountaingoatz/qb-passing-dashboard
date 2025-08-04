from dash import html, dcc
import dash_bootstrap_components as dbc

depth_dropdown = html.Div([
    dbc.DropdownMenu([
        dcc.Checklist(
            id='depth-filter',
            options=[
                {'label': '0-10 yards', 'value': '0-10 yd'},
                {'label': '10-20 yards', 'value': '10-20 yd'},
                {'label': '20+ yards', 'value': '20+ yd'}
            ],
            value=['0-10 yd', '10-20 yd', '20+ yd'],
            labelStyle={'display': 'block'},
            inputStyle={"margin-right": "5px"},
            className='ml-1'
        ),
    ],
        id='depth-dropdown',
        direction="up",
        label="All Depths Selected",
        color="black",
        className='mb-1 mb-1 mw-100',
        style={'width': '100%'},
        toggle_style={'width': '100%'}
    )]
)