from dash import html, dcc, dash_table

from datetime import date, datetime

import dash_daq as daq
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

############################################################################################

from .dashboardComponents.qbImage import qb_image
from .dashboardComponents.qbDropdown import qb_dropdown
from .dashboardComponents.dateFilter import date_filter
from .dashboardComponents.playclockFilter import playclock_filter
from .dashboardComponents.timeFilter import time_filter
from .dashboardComponents.passFilter import pass_filter
from .dashboardComponents.depthDropdown import depth_dropdown
from .dashboardComponents.downDropdown import down_dropdown
from .dashboardComponents.receiverDropdown import receiver_dropdown
from .dashboardComponents.directionDropdown import direction_dropdown

############################################################################################

from .utils.drawPlotlyField import draw_plotly_field

############################################################################################

# create plotly figure, draw field, and create container for the field figure
display_fig = go.Figure()
draw_plotly_field(display_fig, show_title=False, labelticks=False, show_axis=False,
                  glayer='above', bg_color='white', margins=0)
display_graph = dcc.Graph(
    id='display-graph',
    figure=display_fig,
    config={'staticPlot': False,
            'scrollZoom': False,
            },
)

# create plotly figure polar bar graphs, set initial values of theming and colors, and create container for the graphs
dist_fig = px.bar_polar(template="ggplot2",
                        color_discrete_sequence=['#67001f', '#bb2a34', '#e58368', '#fbceb6', '#f7f7f7',
                                                 '#c1ddec', '#6bacd1', '#2a71b2', '#053061'],
                        )

rose_plot = dcc.Graph(
    id='rose-plot',
    figure=dist_fig,
    config={'staticPlot': False,
            'scrollZoom': False},
)

# create plotly figure line plot, set initial values of theming and colors, and create container for the line plot
line_fig = go.Figure()
line_fig.update_layout(
        font_color='black',
        plot_bgcolor='white',
        title='When in the Play Clock does %s find opportunities for completions?' % '(Insert QB Name)',
)

line_plot = dcc.Graph(
    id='line-plot',
    figure=line_fig,
    config={'staticPlot': False,
            'scrollZoom': False}
)

# create plotly figure sankey plot, set initial values of theming and colors, and create container for the sankey plot
sankey_fig = go.Figure()
sankey_fig.update_layout(
        font_color='black',
        plot_bgcolor='white',
        title='Who does %s connect with the most for completions?' % '(Insert QB Name)',
)

sankey_plot = dcc.Graph(
    id='sankey-plot',
    figure=sankey_fig,
    config={'staticPlot': False,
            'scrollZoom': False}
)

dashboard_page = dbc.Container([
    dcc.Store(id='qb-options', storage_type='memory', data=[]),
    dcc.Store(id='stored-qb-data', storage_type='memory', data=[]),
    dbc.Row([
        #########################################
        #### FIRST COLUMN OF DASHBOARD PAGE ####
        dbc.Col([
            html.H4("Pick A Quarterback",
                    className='mt-2 text-center',
                    style={'font=size': '14px'}),
            html.Hr(className="my-2"),
            qb_image,
            qb_dropdown,
            html.H5("Select Filters:", className='mt-2 text-center'),
            html.Hr(className="my-2"),
            pass_filter,
            html.P("Date Filter:", className='mt-2 mb-1 text-left'),
            date_filter,
            html.P("Time Range on Play Clock:", className='mt-2 mb-2 text-left'),
            playclock_filter,
            html.P("Time Range in Quarter:", className='mt-2 mb-2 text-left'),
            time_filter,
            html.P("Game Detail Filters:", className='mt-2 mb-1 text-left'),
            down_dropdown,
            depth_dropdown,
            receiver_dropdown,
            direction_dropdown,
        ],
            width=2,
            className='ml-0 mr-0',
        ),
        #########################################

        #########################################
        #### SECOND COLUMN OF DASHBOARD PAGE ####
        dbc.Col([
            html.Div([
                display_graph,
            ])
        ],
            width=3,
            style={'margin-right': '0px',
                   'margin-left': '0px'}
        ),
        #########################################

        #########################################
        #### THIRD COLUMN OF DASHBOARD PAGE ####
        dbc.Col([
            rose_plot,
            line_plot,
        ],
            width=5,
            style={'margin-right': '0px',
                   'margin-left': '0px'}
        ),
        #########################################

        #########################################
        #### FOURTH COLUMN OF DASHBOARD PAGE ####
        dbc.Col([
            html.H5("How do I interpret these visuals?",
                    className='mt-3 text-center', style={'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Hr(className="my-2"),
            html.P("1. Field Heatmap of Pass Origins", style={'fontWeight': 'bold'}, className='mb-1'),
            html.P("This heatmap shows density contours on the field for where a QB frequently throws the ball "
                   "from. The darker the color, the more frequently the QB finds success from that location.", 
                   style={'fontSize': '14px'}, className='mb-0'
                   ),
            html.P("2. Rose Plot of Passing Tendencies", style={'fontWeight': 'bold'}, className='mb-1'),
            html.P([
                "A rose plot, inspired by ",
                html.A("wind roses used in meteorology", href="https://www.climate.gov/maps-data/dataset/wind-roses-charts-and-tabular-data"),
                ", expresses a QB's directional passing tendencies with the frame of reference being the end zone due North. "
                "Every pass is associated with a vector that indicates where the pass was thrown. "
                "The magnitude of each 'rose' is determined by the number of passes in that direction. "
                ], style={'fontSize': '14px'}, className='mb-0'),
            html.P("3. Line Plot Comparison of Play Clock", style={'fontWeight': 'bold'}, className='mb-1'),
            html.P("The line plot compares how a QB finds opportunities for completions during the play clock versus other QBs.", 
                   style={'fontSize': '14px'}, className='mb-0'),
            html.P("4. Sankey Flow Diagram of Passes", style={'fontWeight': 'bold'}, className='mb-1'),
            html.P(
                "The Sankey Flow Diagram gives a macro-overview for how all of a QB's passes are distributed "
                "amongst his receivers and the depth of the pass.", 
                style={'fontSize': '14px'}, className='mb-0'
            ),
            html.Hr(className="my-2"),
            html.P(
                "Graph Options",
                className='text-center'
            ),
            daq.ToggleSwitch(id='rose-toggle',
                             label='Rose Plot by Pass Depth',
                             labelPosition='top',
                             className='mb-2',
                             value = True,
                             ),
            daq.BooleanSwitch(id='tooltips-toggle', on=True,
                              label='Tooltips are On',
                              labelPosition='top',
                              className='mb-2',
                              color='green',
                              ),
            html.Hr(className="my-2",
                    style={'color': 'black'}),
        ],
            width=2,
            style={'margin-right': '0px',
                   'margin-left': '0px'}
        ),
        #########################################
    ]),
    dbc.Row([
        dbc.Col([
            sankey_plot
        ], 
        width=6
        ),
        dbc.Col([
            html.H5("Pass Stat Breakdown by QB and Type",
                    className='mt-4 mb-4 text-center'),
            dash_table.DataTable(
                id='pass-stats-table',
                columns=[
                    dict( id='Player', name='Player' ),
                    dict( id='% of Short Passes', name='% of Short Passes', type='numeric' ),
                    dict( id='% of Intermediate Passes', name='% of Intermediate Passes', type='numeric' ),
                    dict( id='% of Deep Passes', name='% of Deep Passes', type='numeric' ),
                    dict( id='Avg EPA/Play', name='Avg EPA/Play', type='numeric' ),
                    dict( id='Completion %', name='Completion %', type='numeric' ),
                    dict( id='Avg Air Yards', name='Avg Air Yards', type='numeric' )
                ],
                style_cell={
                    "fontFamily": "Ubuntu", 
                    "fontSize": "12px", 
                    "width": "75px",
                    "whiteSpace": "nowrap",
                    "textAlign": "center",
                    "border": 'none' 
                },
                style_header={
                    "height": "50px",
                    "whiteSpace": "normal",
                    "backgroundColor": "rgb(245,245,245)",
                    "fontWeight": "bold"
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(250,250,250)',
                    }
                ],
                style_table={'border': 'none'},
                cell_selectable=False,
                sort_action='native'
            )
        ], 
        width=6,
        style={'paddingRight': '5rem'}
        )
    ])
], fluid=True) 