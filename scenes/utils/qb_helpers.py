"""
NFL QB Passing Tendencies Dashboard - Utility Functions

This module contains helper functions for processing NFL QB data,
including binning functions and aggregation helpers for visualizations.
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def bin_direction(direction):
    """
    Bin pass direction into 8 compass directions.
    
    Args:
        direction: Raw pass direction data
        
    Returns:
        str: Binned direction (N, NE, E, SE, S, SW, W, NW)
    """
    if pd.isna(direction):
        return 'E'  # Default to East
    
    # Convert to string and standardize
    direction = str(direction).upper()
    
    # Map to 8 compass directions
    direction_map = {
        'N': 'N', 'NORTH': 'N',
        'NE': 'NE', 'NORTHEAST': 'NE',
        'E': 'E', 'EAST': 'E',
        'SE': 'SE', 'SOUTHEAST': 'SE',
        'S': 'S', 'SOUTH': 'S',
        'SW': 'SW', 'SOUTHWEST': 'SW',
        'W': 'W', 'WEST': 'W',
        'NW': 'NW', 'NORTHWEST': 'NW'
    }
    
    return direction_map.get(direction, 'E')

def bin_depth(air_yards):
    """
    Bin air yards into depth categories.
    
    Args:
        air_yards: Air yards value
        
    Returns:
        str: Depth category (0-10 yd, 10-20 yd, 20+ yd)
    """
    if pd.isna(air_yards):
        return '0-10 yd'
    
    air_yards = float(air_yards)
    
    if air_yards <= 10:
        return '0-10 yd'
    elif air_yards <= 20:
        return '10-20 yd'
    else:
        return '20+ yd'

def bin_playclock(play_clock):
    """
    Bin play clock into time ranges.
    
    Args:
        play_clock: Play clock value in seconds
        
    Returns:
        str: Play clock range
    """
    if pd.isna(play_clock):
        return '15-20s'
    
    play_clock = float(play_clock)
    
    if play_clock <= 5:
        return '0-5s'
    elif play_clock <= 10:
        return '5-10s'
    elif play_clock <= 15:
        return '10-15s'
    elif play_clock <= 20:
        return '15-20s'
    elif play_clock <= 25:
        return '20-25s'
    elif play_clock <= 30:
        return '25-30s'
    elif play_clock <= 35:
        return '30-35s'
    else:
        return '35-40s'

def bin_play_outcome(row):
    """
    Bin play outcome into result categories.
    
    Args:
        row: DataFrame row with pass outcome data
        
    Returns:
        str: Play outcome category (Touchdown, First Down, No First Down)
    """
    # Handle touchdown first (highest priority)
    if pd.notna(row.get('pass_touchdown')) and row.get('pass_touchdown') == 1:
        return 'Touchdown'
    
    # Check for first down on passing plays
    if pd.notna(row.get('first_down_pass')) and row.get('first_down_pass') == 1:
        return 'First Down'
    
    # Check general first down field as backup
    if pd.notna(row.get('first_down')) and row.get('first_down') == 1:
        return 'First Down'
    
    # All other outcomes (incomplete, complete but no first down, etc.)
    return 'No First Down'

def aggregate_heatmap(df):
    """
    Aggregate data for heatmap visualization.
    
    Args:
        df: DataFrame with pass location data
        
    Returns:
        dict: Aggregated data for heatmap
    """
    if df.empty:
        return {'x': [], 'y': [], 'counts': []}
    
    # Group by location and count
    heatmap_data = df.groupby(['pass_location_x', 'pass_location_y']).size().reset_index(name='count')
    
    return {
        'x': heatmap_data['pass_location_x'].tolist(),
        'y': heatmap_data['pass_location_y'].tolist(),
        'counts': heatmap_data['count'].tolist()
    }

def aggregate_rose(df):
    """
    Aggregate data for rose plot visualization showing top receivers by play outcomes.
    
    Args:
        df: DataFrame with receiver and play outcome data
        
    Returns:
        DataFrame: Aggregated data for rose plot
    """
    if df.empty:
        return pd.DataFrame(columns=['Receiver', 'Play Outcome', 'Frequency'])
    
    # Add play outcome binning if it doesn't exist
    if 'play_outcome_bin' not in df.columns:
        df['play_outcome_bin'] = df.apply(bin_play_outcome, axis=1)
    
    # Filter to top receivers by total targets (to keep visualization manageable)
    receiver_counts = df.groupby('receiver_player_name').size().reset_index(name='total_targets')
    top_receivers = receiver_counts.nlargest(10, 'total_targets')['receiver_player_name'].tolist()
    
    # Filter data to only include top receivers and passing plays
    filtered_df = df[
        (df['receiver_player_name'].isin(top_receivers)) & 
        (df['receiver_player_name'].notna())
    ].copy()
    
    if filtered_df.empty:
        return pd.DataFrame(columns=['Receiver', 'Play Outcome', 'Frequency'])
    
    # Aggregate by receiver and play outcome
    rose_data = filtered_df.groupby(['receiver_player_name', 'play_outcome_bin']).size().reset_index(name='Frequency')
    rose_data = rose_data.rename(columns={'receiver_player_name': 'Receiver', 'play_outcome_bin': 'Play Outcome'})
    
    return rose_data

def aggregate_timeline(df):
    """
    Aggregate data for timeline visualization.
    
    Args:
        df: DataFrame with play clock data
        
    Returns:
        DataFrame: Aggregated data for timeline
    """
    if df.empty:
        return pd.DataFrame(columns=['Play Clock Range', 'Count', 'Percentage'])
    
    # Add binned play clock if it doesn't exist
    if 'playclock_bin' not in df.columns:
        df['playclock_bin'] = df['play_clock'].apply(bin_playclock)
    
    # Aggregate by play clock range
    timeline_data = df.groupby('playclock_bin').size().reset_index(name='Count')
    timeline_data['Percentage'] = timeline_data['Count'] / timeline_data['Count'].sum()
    timeline_data = timeline_data.rename(columns={'playclock_bin': 'Play Clock Range'})
    
    return timeline_data

def aggregate_sankey(df):
    """
    Aggregate data for Sankey diagram visualization.
    
    Args:
        df: DataFrame with QB, receiver, and depth data
        
    Returns:
        dict: Aggregated data for Sankey diagram
    """
    if df.empty:
        return {'nodes': [], 'links': [], 'link_colors': []}
    
    # Add depth binning if it doesn't exist
    if 'depth_bin' not in df.columns:
        df['depth_bin'] = df['air_yards'].apply(bin_depth)
    
    # Count passes by QB -> Receiver -> Depth
    sankey_data = df.groupby(['passer_player_name', 'receiver_player_name', 'depth_bin']).size().reset_index(name='count')
    
    # Create nodes and links
    nodes = []
    links = []
    link_colors = []
    
    # Color mapping for depths
    depth_colors = {
        '0-10 yd': '#511479',
        '10-20 yd': '#8B2880',
        '20+ yd': '#C63E73'
    }
    
    # Add QB node
    qb_name = df['passer_player_name'].iloc[0]
    nodes.append({'label': qb_name})
    
    # Add receiver nodes and QB->Receiver links
    receiver_counts = df.groupby('receiver_player_name').size().reset_index(name='count')
    receiver_index_map = {}
    
    for idx, (receiver, count) in enumerate(zip(receiver_counts['receiver_player_name'], receiver_counts['count'])):
        nodes.append({'label': receiver})
        receiver_index_map[receiver] = idx + 1
        links.append({'source': 0, 'target': idx + 1, 'value': count})
        link_colors.append('#FBCEB6')
    
    # Add depth nodes and Receiver->Depth links
    depth_index_map = {}
    next_idx = len(nodes)
    
    for depth in sankey_data['depth_bin'].unique():
        nodes.append({'label': depth})
        depth_index_map[depth] = next_idx
        next_idx += 1
    
    # Add receiver->depth links
    for _, row in sankey_data.iterrows():
        receiver_idx = receiver_index_map[row['receiver_player_name']]
        depth_idx = depth_index_map[row['depth_bin']]
        
        links.append({
            'source': receiver_idx,
            'target': depth_idx,
            'value': row['count']
        })
        link_colors.append(depth_colors.get(row['depth_bin'], '#cccccc'))
    
    return {
        'nodes': nodes,
        'links': links,
        'link_colors': link_colors
    }

def calculate_qb_stats(df):
    """
    Calculate QB statistics for the summary table.
    
    Args:
        df: DataFrame with QB passing data
        
    Returns:
        dict: QB statistics
    """
    if df.empty:
        return {}
    
    stats = {}
    
    # Basic stats
    stats['total_attempts'] = len(df)
    stats['completions'] = df['complete_pass'].sum() if 'complete_pass' in df.columns else 0
    stats['completion_pct'] = stats['completions'] / stats['total_attempts'] if stats['total_attempts'] > 0 else 0
    
    # EPA stats
    if 'epa' in df.columns:
        stats['avg_epa'] = df['epa'].mean()
        stats['total_epa'] = df['epa'].sum()
    
    # Air yards stats
    if 'air_yards' in df.columns:
        stats['avg_air_yards'] = df['air_yards'].mean()
        stats['total_air_yards'] = df['air_yards'].sum()
    
    # Depth distribution
    if 'depth_bin' not in df.columns:
        df['depth_bin'] = df['air_yards'].apply(bin_depth)
    
    depth_counts = df['depth_bin'].value_counts()
    for depth in ['0-10 yd', '10-20 yd', '20+ yd']:
        stats[f'{depth}_pct'] = depth_counts.get(depth, 0) / stats['total_attempts'] if stats['total_attempts'] > 0 else 0
    
    return stats 