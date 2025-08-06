# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup

```bash
uv venv                        # Create virtual environment
source .venv/bin/activate      # Activate environment (macOS/Linux)
uv pip install -r requirements.txt  # Install dependencies
```

### Data Management

```bash
python scrape_data.py          # Download and prepare NFL data
```

### Running the Application

```bash
uv run app.py                  # Run dashboard locally (http://localhost:8050)
python app.py                  # Alternative run command
docker compose up --build     # Run with Docker
```

### Testing

```bash
pytest tests/                  # Run all tests
pytest tests/test_utils.py     # Run specific test file
```

## Architecture Overview

This is a Dash-based interactive dashboard for analyzing NFL quarterback passing tendencies using 2022-2023 season data. The application provides field heatmaps, directional analysis, timing patterns, and receiver relationships through four main visualizations.

### Core Architecture

**Data Pipeline**: `scrape_data.py` → DuckDB (`data/nfl.db`) → Parquet files → Dashboard queries

- Uses `nfl_data_py` package to fetch NFL play-by-play data
- DuckDB provides fast analytical queries for ~99,000 plays
- Synthetic data generation for missing fields (play_clock, pass coordinates)

**Component Structure**:

- `app.py` - Main Dash application with callbacks and SQL queries
- `scenes/` - Page layouts and dashboard components
- `components/` - Reusable UI components (navigation, filters)
- `scenes/utils/` - Data processing utilities and field drawing

### Key Visualizations

1. **Field Heatmap** (`display_fig`): 2D density plot of pass locations with coordinate conversion (yards→feet)
2. **Rose Plot** (`rose_plot`): Polar bar chart showing directional passing patterns by depth
3. **Timeline Analysis**: Line plot comparing QB timing vs league average
4. **Sankey Diagram**: Flow visualization of QB→Receiver→Depth relationships

### Database Schema

Primary table structure from NFL play-by-play data:

- QB and receiver identifiers, pass coordinates (X/Y in yards)
- Pass depth bins: 0-10yd, 10-20yd, 20+yd
- Direction bins: 8 compass directions (N, NE, E, SE, S, SW, W, NW)
- Play context: down, distance, play_clock, EPA

### Critical Implementation Details

**Coordinate System**: Field visualization uses feet (0-360 length, 0-160 width) while data is in yards. Conversion: `x_feet = 30 + (x * 3)`, `y_feet = y * 3`

**SQL Queries**: All database queries use parameterized statements with `?` placeholders for security and reliability

**Data Quality**: Original NFL data limitations required synthetic generation for:

- Pass coordinates (realistic field positions)
- Play clock distribution (0-40 seconds weighted)
- Pass directions (8-way compass distribution)

### Component Dependencies

The dashboard reuses modular components adapted from an NBA assists dashboard:

- Filter components in `scenes/dashboardComponents/`
- Field drawing utilities in `scenes/utils/drawPlotlyField.py`
- QB-specific helpers in `scenes/utils/qb_helpers.py`

### Environment Variables

Application expects `.env` file for configuration (referenced but optional for local development).
