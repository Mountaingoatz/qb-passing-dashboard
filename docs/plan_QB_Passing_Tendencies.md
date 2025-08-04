
# Build Plan – QB Passing Tendencies Dashboard

> **Goal:** Stand‑up a fully functional Dash app locally in ≤ 30 minutes using only public NFL data.

---

## 0. Prerequisites

| Tool | Tested version |
|------|----------------|
| Python | 3.9+ |
| Git | latest |
| Node (optional for linting) | 20.x |
| Docker | 24.x |

```bash
# macOS example
brew install python git docker
```

---

## 1. Clone & scaffold

```bash
git clone https://github.com/lukarh/assists-tracking-dash-app nfl-qb-dash
cd nfl-qb-dash
git checkout -b feature/nfl-qb-version
```

*We’ll reuse the repo’s Dash structure, renaming basketball‑specific utilities.*

---

## 2. Create virtual environment & install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install dash==2.16.1 dash-daq dash-bootstrap-components plotly>=5 duckdb pandas numpy nfl_data_py
```

---

## 3. Fetch data (one‑time)

```python
# scrape_data.py
import nfl_data_py as nfl
import duckdb

# Pull seasons (takes ~3 min on 2022‑23)
pbp = nfl.import_pbp_data([2022, 2023])   # citeturn0search0
pbp.to_parquet("data/pbp_2022_23.parquet")

# Optional: roster for headshots / colours
roster = nfl.import_roster(2023)
roster.to_parquet("data/roster_2023.parquet")

# Register tables
con = duckdb.connect("data/nfl.db")
con.execute("CREATE OR REPLACE TABLE pbp AS SELECT * FROM read_parquet('data/pbp_2022_23.parquet');")
con.execute("CREATE OR REPLACE TABLE roster AS SELECT * FROM read_parquet('data/roster_2023.parquet');")
```

Run it:

```bash
python scrape_data.py
```

---

## 4. Build field‑drawing utility

`dashboard/utils/drawPlotlyField.py`

```python
def draw_plotly_field(fig, margins=0, show_axis=False):
    # Draw outline, hash marks, end‑zones
    # Convert yards to x‑y (0–120, 0–53.3)
```

Replace calls to `draw_plotly_court` with this function.

---

## 5. Transform helpers (`utils/qb_helpers.py`)

* `bin_direction(row) -> str`  # N, NE, E…
* `bin_depth(air_yards) -> str`   # Short, Intermediate, Deep
* `bin_playclock(play_clock) -> str`
* `aggregate_heatmap(df)`
* `aggregate_rose(df)`
* `aggregate_timeline(df)`
* `aggregate_sankey(df)`

---

## 6. Dash component tweaks

1. **playerDropdown** → list of unique `passer_player_name`.
2. Remove basketball‑specific filters (Shot type, Catch‑and‑shoot) and add:
   * Down selector (1,2,3,4)
   * Depth multiselect
3. Update modal video URL builder (if using clips).

---

## 7. Update callbacks (`callbacks.py`)

* Load from DuckDB based on filter state (SQL templating).
* Return figures using helper aggregates.

---

## 8. Run locally

```bash
python app.py
# or in Docker
docker compose up --build
open http://localhost:8050
```

---

## 9. Lint & test

```bash
pip install black pylint
black .
pylint dashboard
```

Unit test example:

```python
def test_bin_depth():
    assert bin_depth(5) == "Short"
```

---

## 10. Automate refresh (optional)

`.github/workflows/etl.yml`

```yaml
schedule:
  - cron:  '0 9 * * 2'  # every Tue 9 AM ET
run:  python scrape_data.py
```

---

🟢 **You now have a local NFL QB Passing Tendencies Dashboard mirroring the NBA assists UI!**
