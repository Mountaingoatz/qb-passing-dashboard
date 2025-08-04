from dash import html, dcc
import dash_bootstrap_components as dbc

down_dropdown = html.Div([
    dbc.DropdownMenu([
        dcc.Checklist(
            id='down-filter',
            options=[
                {'label': '1st Down', 'value': 1},
                {'label': '2nd Down', 'value': 2},
                {'label': '3rd Down', 'value': 3},
                {'label': '4th Down', 'value': 4},
            ],
            value=[1, 2, 3, 4],
            labelStyle={'display': 'block'},
            inputStyle={"margin-right": "5px"},
            className='ml-1'
        ),
    ],
        id='down-dropdown',
        direction="up",
        label="All Downs Selected",
        color="black",
        className='mb-1 d-block',
        toggle_style={'width': '100%'}
    )]
)