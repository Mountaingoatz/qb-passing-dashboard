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
            'responsive': True,
            },
    style={'height': '400px', 'width': '100%'}
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
            'scrollZoom': False,
            'responsive': True},
    style={'height': '400px', 'width': '100%'}
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
            'scrollZoom': False,
            'responsive': True},
    style={'height': '350px', 'width': '100%'}
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
            'scrollZoom': False,
            'responsive': True},
    style={'height': '600px', 'width': '100%'}
)

dashboard_page = dbc.Container([
    dcc.Store(id='qb-options', storage_type='memory', data=[]),
    dcc.Store(id='stored-qb-data', storage_type='memory', data=[]),
    # Responsive row with proper breakpoints
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
            xs=12, sm=12, md=12, lg=2, xl=2,  # Full width on small screens, 2/12 on large
            className='ml-0 mr-0 mb-3',
        ),
        #########################################
    ]),
    
    # Field heatmap row - always full width to prevent overlap
    dbc.Row([
        dbc.Col([
            html.H6("Pass Origins Field Heatmap", className='text-center mb-2', style={'fontWeight': 'bold'}),
            html.Div([
                display_graph,
            ], style={'min-height': '400px'})
        ],
            xs=12, sm=12, md=12, lg=12, xl=12,  # Always full width
            className='mb-4',
            style={'padding-right': '15px', 'padding-left': '15px'}
        ),
    ]),
    
    # Rose plot and line plot row - side by side on large screens, stacked on small
    dbc.Row([
        dbc.Col([
            html.H6("Top Receivers by Play Outcomes", className='text-center mb-2', style={'fontWeight': 'bold'}),
            html.Div([
                rose_plot,
            ], className='mb-3'),
        ],
            xs=12, sm=12, md=12, lg=6, xl=6,  # Half width on lg+ screens
            className='mb-3',
            style={'padding-right': '15px', 'padding-left': '15px'}
        ),
        
        dbc.Col([
            html.H6("Play Clock Analysis", className='text-center mb-2', style={'fontWeight': 'bold'}),
            html.Div([
                line_plot,
            ])
        ],
            xs=12, sm=12, md=12, lg=6, xl=6,  # Half width on lg+ screens
            className='mb-3',
            style={'padding-right': '15px', 'padding-left': '15px'}
        ),
    ]),
    
    # Explanations row - full width
    dbc.Row([
        dbc.Col([
            html.H5("How do I interpret these visuals?",
                    className='mt-3 text-center', style={'fontWeight': 'bold', 'fontSize': '18px'}),
            html.Hr(className="my-2"),
            html.P("1. Field Heatmap of Pass Origins", style={'fontWeight': 'bold'}, className='mb-1'),
            html.P("This heatmap shows density contours on the field for where a QB frequently throws the ball "
                   "from. The darker the color, the more frequently the QB finds success from that location.", 
                   style={'fontSize': '14px'}, className='mb-0'
                   ),
            html.P("2. Rose Plot of Top Receivers by Play Outcomes", style={'fontWeight': 'bold'}, className='mb-1'),
            html.P([
                "A rose plot showing a QB's top receivers and the results of passes to each receiver. "
                "Each receiver appears as a segment, with colors indicating play outcomes: ",
                html.Span("red for no first down", style={'color': '#dc3545', 'fontWeight': 'bold'}),
                ", ",
                html.Span("orange for first down", style={'color': '#fd7e14', 'fontWeight': 'bold'}),
                ", and ",
                html.Span("green for touchdown", style={'color': '#198754', 'fontWeight': 'bold'}),
                ". The magnitude shows the frequency of each outcome type."
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
            xs=12, sm=12, md=12, lg=12, xl=12,  # Always full width
            className='mb-3',
            style={'padding-right': '15px', 'padding-left': '15px'}
        ),
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