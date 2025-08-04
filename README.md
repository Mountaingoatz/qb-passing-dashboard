# NFL QB Passing Tendencies Dashboard

An interactive dashboard for analyzing NFL quarterback passing tendencies using play-by-play data from the nfl_data_py package. This dashboard provides comprehensive visualizations of QB passing patterns, including field heatmaps, directional analysis, timing patterns, and receiver relationships.

## Features

- **Field Heatmap**: Visualize where QBs throw from most frequently
- **Rose Plot**: Show directional passing tendencies by depth
- **Timeline Analysis**: Compare QB timing patterns vs league average
- **Sankey Diagram**: Trace QB → Receiver → Pass Depth relationships
- **Interactive Filters**: Filter by down, distance, receiver, play clock, and more

## Quick Start

### Prerequisites

- Python 3.9+
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd passing-stats-dash-app
```

2. Create a virtual environment using uv (recommended):
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Download and prepare the data:
```bash
python scrape_data.py
```

5. Run the dashboard:
```bash
uv run app.py
```

6. Open your browser and navigate to `http://localhost:8050`

### Alternative: Using Docker

```bash
docker compose up --build
```

## Data Sources

This dashboard uses play-by-play data from the [nfl_data_py](https://github.com/cooperdff/nfl_data_py) package, which provides access to NFL play-by-play data. The data includes:

- Passer and receiver names
- Air yards and completion percentage
- EPA (Expected Points Added)
- Play clock information
- Down and distance
- Game date and time

## Dashboard Components

### 1. Field Heatmap
Shows density contours of where QBs throw from most frequently. Darker colors indicate higher frequency of successful passes from that location.

### 2. Rose Plot
A polar bar chart showing directional passing tendencies. The angle represents direction (N, NE, E, SE, S, SW, W, NW) and the radius represents frequency. Colors indicate pass depth.

### 3. Timeline Analysis
Line plot comparing a QB's completion percentage across different play clock ranges versus the league average.

### 4. Sankey Diagram
Flow diagram showing how a QB's passes are distributed among receivers and pass depths.

### 5. Summary Table
Statistical breakdown of QB performance including completion percentage, EPA, and pass depth distribution.

## Filters

- **QB Selection**: Choose any QB from the 2022-2023 seasons
- **Date Range**: Filter by game date
- **Play Clock**: Filter by time remaining on play clock
- **Down**: Filter by down (1st, 2nd, 3rd, 4th)
- **Pass Depth**: Filter by air yards (0-10, 10-20, 20+ yards)
- **Receiver**: Filter by specific receivers
- **Direction**: Filter by pass direction

## Technical Details

- **Frontend**: Dash and Plotly for interactive visualizations
- **Backend**: Python with DuckDB for fast data querying
- **Data**: NFL play-by-play data from nfl_data_py
- **Database**: DuckDB for efficient local data storage and querying
- **Deployment**: Can be deployed locally or on cloud platforms
- **Environment Management**: uv for fast Python package management

## Development

### Project Structure
```
passing-stats-dash-app/
├── app.py                 # Main application file
├── scrape_data.py         # Data ETL script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Data storage
├── components/           # Reusable components
├── scenes/              # Dashboard pages and components
│   ├── dashboard.py     # Main dashboard layout
│   ├── home.py         # Home page
│   ├── dashboardComponents/  # Filter components
│   └── utils/          # Utility functions
└── tests/              # Unit tests
```

### Adding New Features

1. **New Filters**: Add components in `scenes/dashboardComponents/`
2. **New Visualizations**: Add callbacks in `app.py`
3. **Data Processing**: Add functions in `scenes/utils/qb_helpers.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- [nfl_data_py](https://github.com/cooperdff/nfl_data_py) for the Python wrapper and play-by-play data
- [Dash](https://dash.plotly.com/) for the web framework
- [Plotly](https://plotly.com/) for the visualizations
- [DuckDB](https://duckdb.org/) for fast analytical database
- [uv](https://github.com/astral-sh/uv) for fast Python package management 