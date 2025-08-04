from dash import html
import dash_bootstrap_components as dbc

home_page = dbc.Container([
    html.H1('NFL QB Passing Tendencies Dashboard', className='mt-3'),
    html.Hr(className="my-2"),
    html.H5('Motivation'),
    html.P("Quarterback decision-making is the single biggest driver of offensive efficiency in football. "
           "Existing public tools show raw box-score splits, but they seldom visualize throw location, "
           "direction, depth, timing, and receiver distributions together. "
           "This dashboard brings those factors into one interactive view—mirroring the NBA assists app UI "
           "that analysts already know—so coaches, analysts, and fans can explore a QB's passing DNA at a glance."
    ),
    html.H5('About The Data Source'),
    html.P(["This dashboard uses play-by-play data from ",
            html.A("nflfastR", href="https://www.nflfastr.com/"),
            " via the ",
            html.A("nfl_data_py", href="https://github.com/cooperdff/nfl_data_py"),
            " package. The data includes detailed passing information for the 2022-2023 NFL seasons, "
            "including passer and receiver names, air yards, EPA (Expected Points Added), completion percentage, "
            "play clock information, and more. The dashboard provides interactive visualizations to explore "
            "QB passing tendencies across multiple dimensions."
            ]),
    html.H5('Key Features'),
    html.P([
        "• ",
        html.Strong("Field Heatmap:"),
        " Visualize where QBs throw from most frequently\n",
        "• ",
        html.Strong("Rose Plot:"),
        " Show directional passing tendencies by depth\n",
        "• ",
        html.Strong("Timeline Analysis:"),
        " Compare QB timing patterns vs league average\n",
        "• ",
        html.Strong("Sankey Diagram:"),
        " Trace QB → Receiver → Pass Depth relationships\n",
        "• ",
        html.Strong("Interactive Filters:"),
        " Filter by down, distance, receiver, play clock, and more"
    ]),
    html.H5('Data Coverage'),
    html.P("The dashboard currently includes data for all QBs who attempted passes during the 2022-2023 NFL seasons. "
           "This includes regular season games with detailed play-by-play information. "
           "The data is updated weekly and provides comprehensive coverage of modern NFL passing trends."
           ),
    html.H5('Technical Details'),
    html.P([
        "Built with ",
        html.A("Dash", href="https://dash.plotly.com/"),
        " and ",
        html.A("Plotly", href="https://plotly.com/"),
        " for interactive visualizations. Data is stored in ",
        html.A("DuckDB", href="https://duckdb.org/"),
        " for fast querying. The dashboard is designed to handle large datasets efficiently "
        "while providing real-time filtering and visualization updates."
    ]),
    html.H5('GitHub Code'),
    html.P([
        'Interested in looking at the code for this web-application? ',
        html.A("Click here to view the source code!", href="https://github.com/your-repo/nfl-qb-dashboard"),
    ]),
    html.H5('Developed By:'),
    html.P("AI Assistant - Built for NFL analytics and QB scouting"),
]) 