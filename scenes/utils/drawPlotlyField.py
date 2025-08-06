"""
NFL Field Drawing Utility for Plotly

This module provides functions to draw an NFL football field on Plotly figures,
including field markings, hash marks, end zones, and yard lines.
"""

import plotly.graph_objects as go
import numpy as np

def draw_plotly_field(fig, margins=0, show_axis=False, show_title=False, 
                     labelticks=False, glayer='above', bg_color='white'):
    """
    Draw an NFL football field on a Plotly figure.
    
    Args:
        fig: Plotly figure object
        margins: Margin around the field
        show_axis: Whether to show axis labels
        show_title: Whether to show field title
        labelticks: Whether to label tick marks
        glayer: Grid layer ('above' or 'below')
        bg_color: Background color
    """
    
    # NFL field dimensions (in yards, converted to feet)
    field_length = 120  # 100 yards + 10 yards each end zone
    field_width = 53.33  # Standard NFL field width
    
    # Convert to feet for more precise measurements
    field_length_ft = field_length * 3
    field_width_ft = field_width * 3
    
    # Set up the figure layout with proper aspect ratio
    fig.update_layout(
        xaxis=dict(
            range=[-margins, field_length_ft + margins],
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=show_axis,
            title='' if not show_title else 'Field Length (feet)',
            side='bottom',
            scaleanchor='y',
            scaleratio=1
        ),
        yaxis=dict(
            range=[-margins, field_width_ft + margins],
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=show_axis,
            title='' if not show_title else 'Field Width (feet)',
            side='left'
        ),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        width=900,
        height=450,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    
    # Draw field outline with improved colors
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=field_length_ft, y1=field_width_ft,
        line=dict(color="white", width=4),
        fillcolor="#228B22",  # Forest green
        layer="below"
    )
    
    # Draw end zones
    end_zone_length = 10 * 3  # 10 yards in feet
    
    # Left end zone
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=end_zone_length, y1=field_width_ft,
        line=dict(color="white", width=3),
        fillcolor="#006400",  # Dark green
        layer="below"
    )
    
    # Right end zone
    fig.add_shape(
        type="rect",
        x0=field_length_ft - end_zone_length, y0=0, 
        x1=field_length_ft, y1=field_width_ft,
        line=dict(color="white", width=3),
        fillcolor="#006400",  # Dark green
        layer="below"
    )
    
    # Draw yard lines (every 5 yards)
    yard_line_positions = []
    for i in range(0, 101, 5):  # 0 to 100 yards
        if i == 0:  # Goal line
            x_pos = end_zone_length
        else:
            x_pos = end_zone_length + (i * 3)  # Convert yards to feet
        
        yard_line_positions.append(x_pos)
        
        # Draw yard line with varying thickness
        line_width = 3 if i % 10 == 0 else 2  # Thicker lines every 10 yards
        fig.add_shape(
            type="line",
            x0=x_pos, y0=0, x1=x_pos, y1=field_width_ft,
            line=dict(color="white", width=line_width),
            layer="below"
        )
    
    # Add 50-yard line marking
    fifty_yard_pos = end_zone_length + (50 * 3)
    fig.add_annotation(
        x=fifty_yard_pos, y=field_width_ft/2,
        text="50",
        showarrow=False,
        font=dict(color="white", size=18, family="Arial Black"),
        xanchor="center",
        yanchor="middle",
        bgcolor="rgba(0,0,0,0.3)",
        bordercolor="white",
        borderwidth=1
    )
    
    # Draw hash marks
    hash_mark_distance = 18.5 * 3  # 18.5 yards from sideline in feet
    
    # Left hash marks
    for x_pos in yard_line_positions[1:-1]:  # Skip goal lines
        fig.add_shape(
            type="line",
            x0=x_pos, y0=hash_mark_distance, x1=x_pos, y1=hash_mark_distance + 2,
            line=dict(color="white", width=1),
            layer="below"
        )
        fig.add_shape(
            type="line",
            x0=x_pos, y0=field_width_ft - hash_mark_distance - 2, 
            x1=x_pos, y1=field_width_ft - hash_mark_distance,
            line=dict(color="white", width=1),
            layer="below"
        )
    
    # Draw numbers on field (every 10 yards)
    number_positions = []
    for i in range(10, 91, 10):  # 10 to 90 yards
        x_pos = end_zone_length + (i * 3)
        number_positions.append((x_pos, i))
    
    # Add yard numbers as annotations with better positioning
    for x_pos, yard_num in number_positions:
        # Display yard numbers on both sides of 50-yard line
        display_num = min(yard_num, 100 - yard_num) if yard_num > 50 else yard_num
        
        # Left side numbers
        fig.add_annotation(
            x=x_pos, y=field_width_ft/2 + 20,
            text=str(display_num),
            showarrow=False,
            font=dict(color="white", size=14, family="Arial Black"),
            xanchor="center",
            yanchor="middle"
        )
        
        # Right side numbers
        fig.add_annotation(
            x=x_pos, y=field_width_ft/2 - 20,
            text=str(display_num),
            showarrow=False,
            font=dict(color="white", size=14, family="Arial Black"),
            xanchor="center",
            yanchor="middle"
        )
    
    # Draw goal posts (simplified)
    goal_post_width = 18.5 * 2  # 18.5 feet wide
    
    # Left goal post
    fig.add_shape(
        type="line",
        x0=0, y0=(field_width_ft - goal_post_width)/2,
        x1=-10, y1=(field_width_ft - goal_post_width)/2,
        line=dict(color="yellow", width=3),
        layer="above"
    )
    fig.add_shape(
        type="line",
        x0=0, y0=(field_width_ft + goal_post_width)/2,
        x1=-10, y1=(field_width_ft + goal_post_width)/2,
        line=dict(color="yellow", width=3),
        layer="above"
    )
    fig.add_shape(
        type="line",
        x0=-10, y0=(field_width_ft - goal_post_width)/2,
        x1=-10, y1=(field_width_ft + goal_post_width)/2,
        line=dict(color="yellow", width=3),
        layer="above"
    )
    
    # Right goal post
    fig.add_shape(
        type="line",
        x0=field_length_ft, y0=(field_width_ft - goal_post_width)/2,
        x1=field_length_ft + 10, y1=(field_width_ft - goal_post_width)/2,
        line=dict(color="yellow", width=3),
        layer="above"
    )
    fig.add_shape(
        type="line",
        x0=field_length_ft, y0=(field_width_ft + goal_post_width)/2,
        x1=field_length_ft + 10, y1=(field_width_ft + goal_post_width)/2,
        line=dict(color="yellow", width=3),
        layer="above"
    )
    fig.add_shape(
        type="line",
        x0=field_length_ft + 10, y0=(field_width_ft - goal_post_width)/2,
        x1=field_length_ft + 10, y1=(field_width_ft + goal_post_width)/2,
        line=dict(color="yellow", width=3),
        layer="above"
    )
    
    # Add field title if requested
    if show_title:
        fig.add_annotation(
            x=field_length_ft/2, y=field_width_ft + 10,
            text="NFL Football Field",
            showarrow=False,
            font=dict(size=16, color="black"),
            xanchor="center",
            yanchor="middle"
        )
    
    return fig

def add_field_heatmap(fig, x_data, y_data, colorscale='Viridis', 
                     showscale=True, opacity=0.7):
    """
    Add a heatmap overlay to the football field.
    
    Args:
        fig: Plotly figure with field
        x_data: X coordinates for heatmap
        y_data: Y coordinates for heatmap
        colorscale: Plotly colorscale name
        showscale: Whether to show color scale
        opacity: Opacity of heatmap
    """
    
    # Add heatmap contour
    fig.add_trace(go.Histogram2dContour(
        x=x_data,
        y=y_data,
        colorscale=colorscale,
        showscale=showscale,
        opacity=opacity,
        line=dict(width=0),
        hoverinfo='none'
    ))
    
    return fig

def add_field_scatter(fig, x_data, y_data, color='red', size=5, 
                     name='Data Points', hoverinfo='none'):
    """
    Add scatter points to the football field.
    
    Args:
        fig: Plotly figure with field
        x_data: X coordinates for scatter
        y_data: Y coordinates for scatter
        color: Color of scatter points
        size: Size of scatter points
        name: Name for legend
        hoverinfo: Hover information
    """
    
    # Add scatter trace
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers',
        marker=dict(
            color=color,
            size=size,
            opacity=0.8
        ),
        name=name,
        hoverinfo=hoverinfo
    ))
    
    return fig 