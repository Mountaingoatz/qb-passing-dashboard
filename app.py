import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from itertools import product
from datetime import datetime
import os
from dotenv import load_dotenv
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback_context
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import duckdb

############################################################################################

from scenes.home import home_page
from scenes.dashboard import dashboard_page, display_fig, rose_plot
from components.globalComponents.navigationbar import navigation_bar
from scenes.utils.drawPlotlyField import draw_plotly_field
from scenes.utils.qb_helpers import (
    bin_direction, bin_depth, bin_playclock,
    aggregate_heatmap, aggregate_rose, aggregate_timeline, aggregate_sankey
)

############################################################################################

# NFL-specific constants
depths = ['0-10 yd', '10-20 yd', '20+ yd']
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
downs = [1, 2, 3, 4]

############################################################################################

load_dotenv()

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.UNITED],
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                )
server = app.server

# Initialize DuckDB connection
try:
    con = duckdb.connect("data/nfl.db", read_only=True)
except Exception as e:
    print(f"Warning: Could not connect to database: {e}")
    con = None

#############################################################################################

content = html.Div(id='page-content', children=[home_page])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navigation_bar,
    content
])

@app.callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def render_page_content(pathname):
    if pathname == '/home':
        return home_page
    elif pathname == '/dashboard':
        return dashboard_page
    else:
        return html.Div(
            dbc.Container(
                [
                    html.H1("404: Not found", className="text-danger"),
                    html.Hr(),
                    html.P(f"The pathname {pathname} was not recognised..."),
                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )

######################################################################################
############################ Dashboard Callback Functions ############################
######################################################################################

@app.callback(
    Output(component_id='qb-image', component_property='src'),
    Input(component_id='qb-select', component_property='value')
)
def update_image(qb_name):
    # For now, return a placeholder image
    # In production, you'd fetch from NFL roster data
    return 'https://via.placeholder.com/150x150?text=QB'

@app.callback(
    Output(component_id='qb-select', component_property='options'),
    Input(component_id='qb-options', component_property='data'),
)
def update_qb_options(qb_options):
    return qb_options

@app.callback(
    Output(component_id='qb-options', component_property='data'),
    Input(component_id='qb-options', component_property='data'),
)
def get_qb_options(data):
    if con is None:
        return []
    
    try:
        qbs_df = pd.read_sql_query(
            "SELECT DISTINCT passer_player_name FROM pbp WHERE passer_player_name IS NOT NULL", 
            con=con
        )
        qbs_df = qbs_df.rename(columns={'passer_player_name': 'label'})
        qbs_df['value'] = qbs_df['label']
        qbs_df = qbs_df[['label', 'value']].sort_values('label').reset_index(drop=True)
        qb_options = qbs_df.to_dict('records')
        return qb_options
    except Exception as e:
        print(f"Error getting QB options: {e}")
        return []

@app.callback(
    Output(component_id='receiver-filter', component_property='options'),
    Output(component_id='receiver-filter', component_property='value'),
    Input(component_id='qb-select', component_property='value')
)
def update_receiver_data(qb_name):
    if not qb_name or con is None:
        return [], []
    
    try:
        receivers_df = pd.read_sql_query(
            "SELECT DISTINCT receiver_player_name FROM pbp WHERE passer_player_name = ? AND receiver_player_name IS NOT NULL", 
            con=con, params=[qb_name]
        )
        receivers_df = receivers_df.rename(columns={'receiver_player_name': 'label'})
        receivers_df['value'] = receivers_df['label']
        receivers_df = receivers_df[['label', 'value']].sort_values('label').reset_index(drop=True)
        receiver_options = receivers_df.to_dict('records')
        
        return receiver_options, [receiver['value'] for receiver in receiver_options]
    except Exception as e:
        print(f"Error getting receiver data: {e}")
        return [], []

########################### Update Dropdown Label Functions ###########################

@app.callback(
    Output(component_id='down-dropdown', component_property='label'),
    Input(component_id='down-filter', component_property='value'),
)
def update_down_dropdown_label(down_filter):
    if len(down_filter) == 4:
        return 'All Downs Selected'
    elif len(down_filter) == 0:
        return 'No Downs Selected'
    else:
        return '%d Downs Selected' % len(down_filter)

@app.callback(
    Output(component_id='depth-dropdown', component_property='label'),
    Input(component_id='depth-filter', component_property='value')
)
def update_depth_dropdown(depth_filter):
    if len(depth_filter) == 3:
        return 'All Depths Selected'
    else:
        return '%d of 3 Depths Selected' % len(depth_filter)

@app.callback(
    Output(component_id='receiver-dropdown', component_property='label'),
    Input(component_id='receiver-filter', component_property='value'),
    State(component_id='receiver-filter', component_property='options')
)
def update_receiver_dropdown_label(receiver_filter, receiver_options):
    return '%d of %d Receivers Selected' % (len(receiver_filter), len(receiver_options))

@app.callback(
    Output(component_id='direction-dropdown', component_property='label'),
    Input(component_id='direction-filter', component_property='value'),
    Input(component_id='direction-filter', component_property='options')
)
def update_direction_dropdown_label(direction_filter, directions_options):
    return '%d of %d Pass Directions Selected' % (len(direction_filter), len(directions_options))

####################################################################################
############################### FIELD HEATMAP FIGURE ###############################
####################################################################################

@app.callback(
    Output(component_id='display-graph', component_property='figure'),
    Output(component_id='rose-plot', component_property='figure'),
    Input(component_id='pass-detail-filter', component_property='value'),
    Input(component_id='tooltips-toggle', component_property='on'),
    Input(component_id='rose-toggle', component_property='value'),
    Input(component_id='playclock-filter', component_property='value'),
    Input(component_id='time-filter', component_property='value'),
    Input(component_id='receiver-filter', component_property='value'),
    Input(component_id='depth-filter', component_property='value'),
    Input(component_id='down-filter', component_property='value'),
    Input(component_id='direction-filter', component_property='value'),
    Input(component_id='date-filter', component_property='start_date'),
    Input(component_id='date-filter', component_property='end_date'),
    Input(component_id="qb-select", component_property="value"),
)
def update_display_graph(pass_detail, isTooltips_on, rosetype_toggle, 
                        playclock_filter, time_filter, receiver_filter,
                        depth_filter, down_filter, direction_filter, 
                        start_date, end_date, qb_name):
    
    def create_sql_query():
        # Build query with proper parameterization
        conditions = []
        params = []
        
        # Base condition for QB
        conditions.append("passer_player_name = ?")
        params.append(qb_name)
        
        # Play clock filter
        conditions.append("play_clock BETWEEN ? AND ?")
        params.extend([playclock_filter[0], playclock_filter[1]])
        
        # Down filter
        if down_filter:
            placeholders = ','.join(['?' for _ in down_filter])
            conditions.append(f"down IN ({placeholders})")
            params.extend(down_filter)
        
        # Depth filter
        if depth_filter:
            depth_conditions = []
            for depth in depth_filter:
                if depth == '0-10 yd':
                    depth_conditions.append("air_yards BETWEEN 0 AND 10")
                elif depth == '10-20 yd':
                    depth_conditions.append("air_yards BETWEEN 10 AND 20")
                elif depth == '20+ yd':
                    depth_conditions.append("air_yards > 20")
            if depth_conditions:
                conditions.append("(" + " OR ".join(depth_conditions) + ")")
        
        # Receiver filter
        if receiver_filter:
            placeholders = ','.join(['?' for _ in receiver_filter])
            conditions.append(f"receiver_player_name IN ({placeholders})")
            params.extend(receiver_filter)
        
        # Direction filter
        if direction_filter:
            placeholders = ','.join(['?' for _ in direction_filter])
            conditions.append(f"pass_direction IN ({placeholders})")
            params.extend(direction_filter)
        
        query = "SELECT * FROM pbp WHERE " + " AND ".join(conditions)
        return query, params
    
    def filter_date_and_time(df):
        df['game_date'] = pd.to_datetime(df['game_date'])
        filtered_df = df[(df['game_date'] >= start_date) & (df['game_date'] <= end_date)]
        return filtered_df
    
    def update_field_figure(display_fig, df):
        display_fig.data = [] 
        
        # Convert coordinates from yards to feet to match field coordinate system
        # Field: 0-360 feet (120 yards), Data: 0-100 yards
        # Field: 0-160 feet (53.33 yards), Data: 5-48 yards
        
        # Convert X coordinates (yards to feet, with end zone offset)
        x_coords = []
        for x in df['pass_location_x'].to_list():
            # Convert yardline to field position in feet
            # 0 yardline = 30 feet (end zone), 100 yardline = 330 feet
            field_x = 30 + (x * 3)  # 30 feet offset + yards to feet
            x_coords.append(field_x)
        
        # Convert Y coordinates (yards to feet)
        y_coords = []
        for y in df['pass_location_y'].to_list():
            # Convert sideline position to field position in feet
            # Field width is 160 feet, data range is 5-48 yards
            field_y = y * 3  # Convert yards to feet
            y_coords.append(field_y)
        
        # Add heatmap contour
        display_fig.add_trace(go.Histogram2dContour( 
            x=x_coords,
            y=y_coords,
            colorscale=['rgb(255, 255, 255)'] + px.colors.sequential.Magma[1:][::-1],
            xaxis='x2',
            yaxis='y2',
            showscale=False,
            line=dict(width=0),
            hoverinfo='none'
        ))
        
        # Add scatter points
        display_fig.add_trace(go.Scatter(
            x=x_coords,
            y=y_coords,
            xaxis='x2',
            yaxis='y2',
            mode='markers',
            marker=dict(
                symbol='x',
                color='black',
                size=4
            ),
            name='Pass Origin' if pass_detail == 'pass_' else 'Pass Target',
            hoverinfo='none',
        ))

        # Prepare tooltip data
        tooltips_data = np.stack((
            df['receiver_player_name'], 
            df['air_yards'],
            df['down'], 
            df['distance'], 
            df['game_date'],
            df['play_clock'], 
            df['pass_location_x'],
            df['pass_location_y'],
            df['passer_player_name'], 
            df['posteam'],
            df['defteam'], 
            df['epa']
        ), axis=-1)

        display_fig.update_traces(
            customdata=tooltips_data,
            selector=dict(type='scatter'),
            hovertemplate="<b>Date:</b> %{customdata[4]}<br>" +
                            "<b>Down:</b> %{customdata[2]} & %{customdata[3]}<br>" +
                            "<b>Receiver:</b> %{customdata[0]}<br>" +
                            "<b>Air Yards:</b> %{customdata[1]}<br>" +
                            "<b>Play Clock:</b> %{customdata[5]}<br>" +
                            "<b>EPA:</b> %{customdata[11]}<br>" if isTooltips_on else None
        )
        return display_fig
    
    def process_data_for_rose_plot(df):
        # Create rose plot data for pass directions and depths
        directions_df = pd.DataFrame(product(directions, depths, [0]), 
                                   columns=['Direction', 'Pass Depth', 'Frequency']) 

        # Count actual data
        df['direction_bin'] = df['pass_direction'].apply(bin_direction)
        df['depth_bin'] = df['air_yards'].apply(bin_depth)
        
        distcounts_df = df.groupby(['direction_bin', 'depth_bin']).size().reset_index()
        distcounts_df = distcounts_df.rename({
            'direction_bin': 'Direction', 'depth_bin': 'Pass Depth', 0: 'Frequency 2'
        }, axis=1)
        
        # Merge with template
        directions_df = directions_df.merge(distcounts_df, on=['Direction', 'Pass Depth'], how='left')
        directions_df['Frequency'] = np.max(directions_df[['Frequency', 'Frequency 2']], axis=1)
        directions_df = directions_df.drop(columns=['Frequency 2'])
        
        return directions_df
    
    def update_rose_plot(directions_df, rosetype_toggle):
        depths_colors = ['#67001f', '#bb2a34', '#e58368', '#fbceb6', '#f7f7f7',
                        '#c1ddec', '#6bacd1', '#2a71b2', '#053061']
        
        rose_fig = px.bar_polar(directions_df, r="Frequency", theta="Direction",
                               color='Pass Depth',
                               template="ggplot2",
                               color_discrete_sequence=depths_colors,
                               title="Passing Tendencies by Direction and Depth",
                               )
        rose_fig.update_layout(
            legend_title_text='Pass Depth',
            font=dict(family='Ubuntu')
        )
        return rose_fig

    if not qb_name or con is None:
        # Return empty field
        field_fig = go.Figure()
        draw_plotly_field(field_fig, show_title=False, labelticks=False, show_axis=False,
                         glayer='above', bg_color='white', margins=0)
        return field_fig, go.Figure()

    try:
        query, params = create_sql_query()
        df = pd.read_sql_query(query, con=con, params=params)
        df = filter_date_and_time(df)
    except Exception as e:
        print(f"Error querying data: {e}")
        field_fig = go.Figure()
        draw_plotly_field(field_fig, show_title=False, labelticks=False, show_axis=False,
                         glayer='above', bg_color='white', margins=0)
        return field_fig, go.Figure()

    if len(df) != 0:
        new_display_fig = update_field_figure(display_fig, df)
        directions_df = process_data_for_rose_plot(df)
        new_rose_fig = update_rose_plot(directions_df, rosetype_toggle)
        return new_display_fig, new_rose_fig
    
    else:
        field_fig = go.Figure()
        draw_plotly_field(field_fig, show_title=False, labelticks=False, show_axis=False,
                         glayer='above', bg_color='white', margins=0)
        return field_fig, go.Figure()

####################################################################################
################################# LINE PLOT FIGURE #################################
#################################################################################### 

@app.callback(
    Output(component_id='line-plot', component_property='figure'),
    Input(component_id='qb-select', component_property='value'),
)
def update_lineplot(qb_name):
    if not qb_name or con is None:
        return go.Figure()
    
    try:
        bins = [0, 5, 10, 15, 20, 25, 30, 35, 40]
        group_names = ['0-5s', '5-10s', '10-15s', '15-20s', '20-25s', '25-30s', '30-35s', '35-40s']
        playclock_ranges = ['0-5s', '5-10s', '10-15s', '15-20s', '20-25s', '25-30s', '30-35s', '35-40s']

        # Get all data for comparison
        results_df = pd.read_sql_query("SELECT * FROM pbp WHERE passer_player_name IS NOT NULL", con=con)
    except Exception as e:
        print(f"Error in line plot: {e}")
        return go.Figure()

    # Process data logic - calculate distribution of QB's attempts and entire sample's attempts in playclock ranges
    results_df['playclock_range'] = pd.cut(results_df['play_clock'], bins, labels=group_names)
    playclock_df = results_df[['passer_player_name','playclock_range']].groupby(
        by=['passer_player_name','playclock_range'])['playclock_range'].size() \
        .unstack(fill_value=0).stack().reset_index(name='count')
    playclock_df['per_count'] = round(playclock_df['count'] / playclock_df.groupby('passer_player_name')['count'].transform('sum'), 3)
    
    sample_df = playclock_df.groupby(by=['playclock_range'])['count'].sum().reset_index(name='count')
    sample_df['per_count'] = round(sample_df['count'] / sample_df['count'].sum(), 3)

    # Create new figure
    new_fig = go.Figure()

    # Plot every QB's line plot except for the current chosen QB
    for qb in playclock_df['passer_player_name'].unique():
        qb_df = playclock_df[playclock_df['passer_player_name'] == qb].reset_index(drop=True)
        values = qb_df['per_count'].to_list()
        if qb != qb_name:
            new_fig.add_trace(go.Scatter(x=playclock_ranges, y=values, name=qb,
                                         line=dict(color='rgb(195,195,195)', width=3, dash='dot')))

    # Plot sample average of the dataset
    new_fig.add_trace(go.Scatter(x=playclock_ranges, y=sample_df['per_count'].to_list(), name='Sample Average',
                         line=dict(color='rgb(223,80,103)', width=3, dash='dash')))

    chosen_values = playclock_df[playclock_df['passer_player_name'] == qb_name]['per_count'].to_list()

    # Plot the selected QB's line plot
    new_fig.add_trace(go.Scatter(x=playclock_ranges, y=chosen_values,
                                 name=qb_name, line=dict(color='rgb(233,84,32)', width=5), mode="lines+text",
                                 text=['<b>' + str(round(val * 100, 1)) + '%' + '</b>' for val in chosen_values],
                                 textposition='top center', textfont=dict(color='black', size=13)))
    
    # Define line plot figure's theme and colors
    new_fig.update_layout(
        font_color='black',
        plot_bgcolor='#F8F5F0',
        title='When in the Play Clock does %s find opportunities for completions?' % qb_name,
        title_x=0.5,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
        ),
        yaxis=dict(
            gridcolor='white'
        ),
        font=dict(family='Ubuntu')
    )

    new_fig.update_xaxes(title='Play Clock Range', showline=False)
    new_fig.update_yaxes(title='% of Attempts', tickformat='0.0%', showline=False)

    return new_fig

####################################################################################
################################ SANKEY PLOT FIGURE ################################
#################################################################################### 

@app.callback(
    Output(component_id='sankey-plot', component_property='figure'),
    Input(component_id='qb-select', component_property='value'),
)
def update_sankey(qb_name):
    if not qb_name or con is None:
        return go.Figure()
    
    try:
        df = pd.read_sql_query(
            "SELECT * FROM pbp WHERE passer_player_name = ? AND receiver_player_name IS NOT NULL", 
            con=con, params=[qb_name]
        )
    except Exception as e:
        print(f"Error in Sankey plot: {e}")
        return go.Figure()

    counts_by_receiver = df.groupby(by=['passer_player_name','receiver_player_name']).size().reset_index().rename(columns={0: 'counts'}).sort_values(by=['counts'], ascending=False)
    counts_by_receiver_and_depth = df.groupby(by=['passer_player_name','receiver_player_name','depth_bin']).size().reset_index().rename(columns={0: 'counts'}).sort_values(by=['counts'], ascending=False)

    nodes, links, link_colors = [], [], []
    receiver_index_map, depth_index_map = dict(), dict()
    depth_color_map = {
        '0-10 yd': '#511479',
        '10-20 yd': '#8B2880',
        '20+ yd': '#C63E73',
    }
    
    nodes = nodes + [{'label': qb_name} for _ in range(1)]
    nodes = nodes + [{'label': receiver} for receiver in counts_by_receiver['receiver_player_name'].to_list()]
    nodes = nodes + [{'label': depth} for depth in counts_by_receiver_and_depth['depth_bin'].unique()]

    for receiver, num_passes, index in zip(counts_by_receiver['receiver_player_name'].to_list(), counts_by_receiver['counts'].to_list(), [i for i in range(1, len(counts_by_receiver) + 1)]):
        links.append({'source': 0, 'target': index, 'value': num_passes})
        receiver_index_map[receiver] = index
        link_colors.append('#FBCEB6')
        
    for depth in counts_by_receiver_and_depth['depth_bin'].unique():
        index += 1
        depth_index_map[depth] = index
    
    for receiver, depth, num_depth_passes in zip(counts_by_receiver_and_depth['receiver_player_name'].to_list(), counts_by_receiver_and_depth['depth_bin'].to_list(), counts_by_receiver_and_depth['counts'].to_list()):
        links.append({'source': receiver_index_map[receiver], 'target': depth_index_map[depth], 'value': num_depth_passes})
        link_colors.append(depth_color_map[depth])

    # Create the Sankey diagram figure
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=1.0),
            label=[node['label'] for node in nodes],
            color='rgb(233,84,32)',
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
            color=link_colors,
            hovertemplate="QB: %{source.label}<br>"
                        "Receiver: %{target.label}<br>"
                        "No. Passes: %{value:.0f}<br>",
        ),
    )])

    # Customize the layout
    fig.update_layout(
        title_text="Who does %s connect with the most for completions?" % qb_name,
        title_x=0.5,
        font=dict(
            family='Ubuntu',
            size=14
        ),
        height=750
    )

    return fig

####################################################################################
################################ DATA TABLE FIGURE #################################
#################################################################################### 

@app.callback(
    Output(component_id='pass-stats-table', component_property='data'),
    Input(component_id='pass-stats-table', component_property='data'),
)
def update_pass_stats_table(data):
    if con is None:
        return []
    
    try:
        df = pd.read_sql_query("SELECT * FROM pbp WHERE passer_player_name IS NOT NULL", con=con)

        # Add depth binning
        df['depth_bin'] = df['air_yards'].apply(bin_depth)
    except Exception as e:
        print(f"Error in stats table: {e}")
        return []
    
    grouped = df.groupby(['passer_player_name', 'depth_bin']).size()
    total_counts = df.groupby(['passer_player_name']).size()
    percentages = round(grouped / total_counts, 3)

    result = percentages.unstack(level='depth_bin')
    result = result.reset_index()[['passer_player_name','0-10 yd','10-20 yd','20+ yd']]

    result.columns = ['Player','% of Short Passes','% of Intermediate Passes','% of Deep Passes']

    # Add EPA and completion percentage
    qb_stats = df.groupby('passer_player_name').agg({
        'epa': 'mean',
        'complete_pass': 'mean',
        'air_yards': 'mean'
    }).reset_index()
    
    qb_stats = qb_stats.rename(columns={
        'epa': 'Avg EPA/Play',
        'complete_pass': 'Completion %',
        'air_yards': 'Avg Air Yards'
    })

    result = pd.merge(result, qb_stats, how='left', left_on='Player', right_on='passer_player_name')
    result = result.drop(columns=['passer_player_name'])

    return result.to_dict(orient='records')

####################################################################################
################################## GRAPH TOGGLES ###################################
#################################################################################### 

@app.callback(
    Output(component_id='rose-toggle', component_property='label'),
    Input(component_id='rose-toggle', component_property='value'),
)
def update_rose_toggle_info(toggle_on):
    return 'Rose Plot by Pass Depth' if toggle_on else 'Rose Plot by Pass Direction'

@app.callback(
    Output(component_id='tooltips-toggle', component_property='label'),
    Input(component_id='tooltips-toggle', component_property='on')
)
def update_tooltips_toggle_info(tooltips_toggle):
    return 'Tooltips are On' if tooltips_toggle else 'Tooltips are Off'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050) 