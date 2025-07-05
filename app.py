import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --- Data Simulation ---
def get_data():
    """Simulates fetching data from an API for range bars."""
    return [
        {"id": 1, "title": "Vacation Days", "range_min": 0, "range_max": 55, "bar_start": 15, "bar_end": 37, "start_value": 15, "current_value": 28},
        {"id": 2, "title": "Customer Satisfaction", "range_min": 0, "range_max": 100, "bar_start": 12, "bar_end": 25, "start_value": 20, "current_value": 25},
        {"id": 3, "title": "Server Load (%)", "range_min": 0, "range_max": 100, "bar_start": 40, "bar_end": 80, "start_value": 50, "current_value": 70},
        {"id": 4, "title": "Sprint Progress (Tasks)", "range_min": 0, "range_max": 40, "bar_start": 10, "bar_end": 25, "start_value": 10, "current_value": 18},
        {"id": 5, "title": "Monthly Sales (k$)", "range_min": 0, "range_max": 200, "bar_start": 80, "bar_end": 150, "start_value": 80, "current_value": 120},
        {"id": 6, "title": "Daily Signups", "range_min": 0, "range_max": 150, "bar_start": 50, "bar_end": 110, "start_value": 50, "current_value": 90},
    ]

def get_color_from_scale(value, range_min, range_max):
    """Calculates a color from a green-yellow-red scale based on a value."""
    if range_max == range_min:
        return 'rgb(0,128,0)'
    
    normalized_value = (value - range_min) / (range_max - range_min)
    
    green = np.array([0, 128, 0])
    yellow = np.array([255, 255, 0])
    red = np.array([255, 0, 0])
    
    if normalized_value <= 0.5:
        interp_factor = normalized_value * 2
        color = green * (1 - interp_factor) + yellow * interp_factor
    else:
        interp_factor = (normalized_value - 0.5) * 2
        color = yellow * (1 - interp_factor) + red * interp_factor
        
    r, g, b = color.astype(int)
    return f'rgb({r},{g},{b})'

# --- Range Bar Chart Creation ---
def create_range_bar_chart(range_min, range_max, bar_start, bar_end, start_value, current_value):
    """Creates a horizontal range bar chart using Plotly."""

    fig = go.Figure()

    # --- Create Rounded Gradient Bar ---
    y_res = 20  # Vertical resolution of the heatmap
    x_res = 200 # Horizontal resolution

    y_coords = np.linspace(-0.5, 0.5, y_res)
    x_coords = np.linspace(bar_start, bar_end, x_res)
    
    # Create a 2D grid of the x-coordinates for the color value
    z_values = np.tile(x_coords, (y_res, 1))

    # --- Create a mask for the rounded corners, adjusted for aspect ratio ---
    y_radius = 0.5  # The radius for the y-dimension is half the bar height.
    
    # Calculate an equivalent radius for the x-dimension to make the corners circular.
    # This factor is an approximation of the plot's height-to-width ratio.
    aspect_ratio_correction = 0.015 
    x_radius = (range_max - range_min) * aspect_ratio_correction

    # Prevent the radius from being larger than half the bar's length
    if x_radius > (bar_end - bar_start) / 2:
        x_radius = (bar_end - bar_start) / 2

    # Create coordinate grids
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)
    
    # Define the centers of the semi-circles for the ends of the bar
    left_center_x = bar_start + x_radius
    right_center_x = bar_end - x_radius

    # Mask for the left semi-circle
    left_mask = (x_grid < left_center_x) & (((x_grid - left_center_x) / x_radius)**2 + (y_grid / y_radius)**2 > 1)
    
    # Mask for the right semi-circle
    right_mask = (x_grid > right_center_x) & (((x_grid - right_center_x) / x_radius)**2 + (y_grid / y_radius)**2 > 1)

    # Apply the mask to the z-data, setting corners to None so they are not rendered
    if x_radius > 0: # Only apply mask if the bar is wide enough for a radius
        z_values[left_mask | right_mask] = None

    fig.add_trace(go.Heatmap(
        x=x_coords,
        y=y_coords,
        z=z_values,
        colorscale=[(0, 'green'), (0.5, 'yellow'), (1, 'red')],
        zmin=range_min,
        zmax=range_max,
        showscale=False,
        hoverinfo='none',
    ))

    # Add start value triangle marker
    fig.add_trace(go.Scatter(
        x=[start_value],
        y=[0],
        mode='markers',
        marker=dict(
            symbol='triangle-up',
            color=get_color_from_scale(start_value, range_min, range_max),
            size=28,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hoverinfo='none',
        showlegend=False
    ))

    # Add current value circle marker
    fig.add_trace(go.Scatter(
        x=[current_value],
        y=[0],
        mode='markers',
        marker=dict(
            symbol='circle',
            color=get_color_from_scale(current_value, range_min, range_max),
            size=28,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hoverinfo='none',
        showlegend=False
    ))
    
    fig.update_layout(
        height=70,
        margin=dict(l=30, r=30, t=25, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[range_min, range_max]),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-1, 1]),
        showlegend=False,
        shapes=[
            go.layout.Shape(
                type="rect",
                xref="x",
                yref="y",
                x0=range_min,
                y0=-0.5,
                x1=range_max,
                y1=0.5,
                fillcolor="#E8E8E8",
                line_width=0,
                layer="below"
            )
        ]
    )

    # Add annotations for min and max values
    fig.add_annotation(
        x=range_min, y=0, text=f"{range_min:.0f}",
        showarrow=False, xanchor='right', xshift=-5, font=dict(size=14, color="#333")
    )
    fig.add_annotation(
        x=range_max, y=0, text=f"{range_max:.0f}",
        showarrow=False, xanchor='left', xshift=5, font=dict(size=14, color="#333")
    )

    return fig

# --- Streamlit App Layout ---
st.set_page_config(
    layout="wide", 
    page_title="Metrics Dashboard",
    initial_sidebar_state="collapsed",
)

st.title("Metrics Dashboard")

# Fetch data
data = get_data()

# A single container for all metric rows
with st.container():
    # Apply a border and padding using custom HTML/CSS
    st.markdown("""
    <div style="border: 1px solid #e6e6e6; border-radius: 10px; padding: 15px;">
    """, unsafe_allow_html=True)

    for index, metric in enumerate(data):
        col1, col2 = st.columns([3, 9], vertical_alignment="center")

        with col1:
            st.markdown(f"<p style='font-size: 1.25rem; font-weight: bold; text-align: left;'>{metric['title']}</p>", unsafe_allow_html=True)
        
        with col2:
            chart = create_range_bar_chart(
                metric["range_min"], metric["range_max"], 
                metric["bar_start"], metric["bar_end"],
                metric["start_value"], metric["current_value"]
            )
            st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})
        
        if index < len(data) - 1:
            st.divider()

    # Close the custom div
    st.markdown("</div>", unsafe_allow_html=True) 