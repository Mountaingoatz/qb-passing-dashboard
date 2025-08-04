
# Product Requirements Document (PRD)
## QB Passing Tendencies Interactive Dashboard

### 1 — Background & Rationale
Quarterback decision‑making is the single biggest driver of offensive efficiency. Existing public tools show raw box‑score splits, but they seldom **visualise throw location, direction, depth, timing, and receiver distributions together**.  
This dashboard brings those factors into one interactive view—mirroring the NBA assists app UI your stakeholders already know—so analysts, coaches, and fans can explore a QB’s passing DNA at a glance.

### 2 — Goals
| Priority | Goal | Metric of Success |
|----------|------|-------------------|
| P0 | Allow users to discover a QB’s preferred throw locations & depths | Heatmap renders within 1 s; >90 % of throws mapped |
| P0 | Reveal directional/depth tendencies in a rose plot | Rose plot updates <1 s per filter change |
| P0 | Compare a QB’s time‑to‑throw opportunities to league peers | Line chart with sample‑average overlay |
| P0 | Show which receivers & depths each QB targets most | Sankey view & sortable summary table |
| P1 | Clip integration: click heatmap dot → view play video | Supported for ≥ 10 % of plays with public clips |
| P2 | EPA / Win‑Prob shading toggle | Toggle renders in <1 s |

### 3 — Non‑Goals
* **Real‑time in‑game** analytics (refresh cadence is weekly).
* Modeling proprietary xComp% or player tracking beyond public Next Gen releases.

### 4 — Personas
* **Analyst Alex** – team analyst prepping weekly opponent reports.
* **Content Creator Casey** – builds social graphics highlighting QB trends.
* **Fan Fran** – casual fan exploring favourite QB.

### 5 — Key Data Metrics
* Throw origin (x, y) & catch point (if tracking available)  
* **Direction bins** – 8‑way compass relative to LOS  
* **Depth buckets** – 0‑10 yd, 10‑20 yd, 20 + yd  
* **Completion %**, **EPA/Play**, **Expected Completion Prob.** (xComp)  
* **Play‑clock bucket** at snap: 0‑5 s, 5‑10 s, …  
* **Receiver target counts** and **yards after catch (YAC)**  
* **League‑average overlays** for timing and depth

### 6 — Data Sources
| Dataset | Fields used | Access method |
|---------|-------------|---------------|
| `nfl_data_py` *play‑by‑play* (sourced from nflfastR) | `passer_player_name`, `receiver_player_name`, `air_yards`, `pass_location`, `epa`, `cpoe`, `game_seconds_remaining`, `play_clock` | `nfl.import_pbp_data([2022, 2023])` citeturn0search0 |
| Big Data Bowl sample tracking (optional) | `x`, `y`, `event`, `play_direction` | Kaggle CSV download |
| NFL roster & team look‑ups (`nfl.import_roster`) | player headshots, team colours | `nfl.import_roster(2023)` |

### 7 — High‑Level Workflow
1. **ETL & Cache**  
   * Nightly GitHub Actions job pulls latest PBP via `nfl_data_py`, casts to Parquet, and registers in DuckDB.
2. **API Layer (Python)**  
   * Thin query helpers aggregate throw‑level rows into bins used by each visual.
3. **Dash Front‑End**  
   * Re‑uses existing components: sidebar filters, Plotly figures, modal video player.
4. **Deployment**  
   * Local `python app.py` for dev; containerised (Docker) for prod.

### 8 — Feature Breakdown
| Feature | Description | Component |
|---------|-------------|-----------|
| Field Heatmap | 2‑D KDE of throw origins; density contours coloured by attempt volume | `display_graph` |
| Rose Plot | Polar bar; angle = direction bin, radius = attempts; colour = depth bucket | `rose-plot` |
| Timeline Plot | Line: % of attempts per play‑clock bucket; dashed grey league avg | `line-plot` |
| Sankey | Nodes: (QB)→Receiver→Depth Bucket; widths = completed passes | `sankey-plot` |
| Summary Table | Row per QB with % of throws by depth + EPA/Play columns | `dash_table` |

### 9 — Filters
* Season / week range  
* Down & Distance bucket  
* Play‑clock range  
* Direction / depth checkbox groups  
* Receiver multi‑select  
* EPA toggle (switch)  

### 10 — Non‑Functional Requirements
| Aspect | Requirement |
|--------|-------------|
| Performance | <1 s render on 50k‑row dataset, 16 GB RAM laptop |
| Accessibility | Colour‑blind safe palette |
| Licensing | MIT; source data under nflfastR CC‑BY |

### 11 — Acceptance Criteria (MVP)
1. User can select any QB 2022‑present; visuals update within performance SLA.  
2. All four visuals match totals (tooltip counts) across filters.  
3. App runs locally via `docker compose up --build`.  
4. README documents reproducible data download.

---

