import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests
import json
import pandas as pd
import math
from datetime import datetime

def get_rounding_precision(range_min, range_max):
    """
    Calculates the number of decimal places for rounding based on
    2 significant digits of the range difference.
    """
    if range_max == range_min:
        return 2

    diff = abs(range_max - range_min)
    if diff <= 0:
        return 2

    precision = 2 - math.floor(math.log10(diff))
    return max(0, min(10, precision))


# --- Data Simulation ---
def get_data():
    
    # Get data from API
    response = requests.get('https://python-server-e4a8c032b69c.herokuapp.com/bitcoin-data')
    priceData = response.json()
    #--------------------------------
    # Extract Momentum Z-Index

    # Convert price history to DataFrame
    df_plrr = pd.DataFrame(priceData['price_history'])


    #Get latest value
    plrr_latest = df_plrr.iloc[-1]['value']
    #Get 30d prior value
    plrr_30d_prior = df_plrr.iloc[-30]['value']
    # Get 1yr range
    plrr_1yr_range = df_plrr.iloc[-365:]['value']
    # max and min of 1yr range
    plrr_1yr_range_max = plrr_1yr_range.max()
    plrr_1yr_range_min = plrr_1yr_range.min()

    #--------------------------------
    # Extract Price Quantile
    df_quantile_index = pd.DataFrame(priceData['quantile_index'])
    quantile_index_latest = df_quantile_index.iloc[-1]['value']*100
    quantile_index_30d_prior = df_quantile_index.iloc[-30]['value']*100
    quantile_index_1yr_range = df_quantile_index.iloc[-365:]['value']*100
    quantile_index_1yr_range_max = quantile_index_1yr_range.max()
    quantile_index_1yr_range_min = quantile_index_1yr_range.min()


    #--------------------------------
    # Extract Volatility
    # Make GET request to API endpoint
    response = requests.get('https://python-server-e4a8c032b69c.herokuapp.com/volatility')
    volatilityData = response.json()
    df_volatility = pd.DataFrame(volatilityData['historical'])
    volatility_latest = df_volatility.iloc[-1]['volatility']*100
    volatility_30d_prior = df_volatility.iloc[-30]['volatility']*100
    volatility_1yr_range = df_volatility.iloc[-365:]['volatility']*100
    volatility_1yr_range_max = volatility_1yr_range.max()
    volatility_1yr_range_min = volatility_1yr_range.min()
    #--------------------------------

    #--------------------------------
    # Extract Optimal Leverage
    days_since_genesis = (datetime.now() - datetime(2009, 1, 3)).days
    PLR = 5.7*np.log(1+365/(days_since_genesis+np.arange(-365,0)))
    Leverage = (PLR/df_volatility.iloc[-365:]['volatility']**1.5).to_numpy()+0.2*(df_plrr.iloc[-365:]['value'].to_numpy())/(df_volatility.iloc[-365:]['volatility']).to_numpy()
    Leverage_latest = Leverage[-1]
    Leverage_30d_prior = Leverage[-30]
    Leverage_1yr_range = Leverage[-365:]
    Leverage_1yr_range_max = Leverage_1yr_range.max()
    Leverage_1yr_range_min = Leverage_1yr_range.min()

    output = [
        {"id": 1, "title": "Price Quantile ", "info_url": "https://example.com/price-quantile", "range_min": 0, "range_max": 100, "bar_start": quantile_index_1yr_range_min, "bar_end": quantile_index_1yr_range_max, "start_value": quantile_index_30d_prior, "current_value": quantile_index_latest, "suffix": "%"},
        {"id": 2, "title": "Momentum Z-Index", "info_url": "https://example.com/momentum", "range_min": -3, "range_max": 3, "bar_start": plrr_1yr_range_min, "bar_end": plrr_1yr_range_max, "start_value": plrr_30d_prior, "current_value": plrr_latest},
        {"id": 3, "title": "Volatility", "info_url": "https://example.com/volatility", "range_min": 0, "range_max": 100, "bar_start": volatility_1yr_range_min, "bar_end": volatility_1yr_range_max, "start_value": volatility_30d_prior, "current_value": volatility_latest, "suffix": "%"}
        # {"id": 4, "title": "Optimal Leverage", "info_url": "https://example.com/leverage", "range_min": 0.0, "range_max": 2.3, "bar_start": Leverage_1yr_range_min, "bar_end": Leverage_1yr_range_max, "start_value": Leverage_30d_prior, "current_value": Leverage_latest, "suffix": "x"},
        # {"id": 5, "title": "MVRV", "info_url": "https://example.com/mvrv", "range_min": 0.5, "range_max": 3.5, "bar_start": 1.8, "bar_end": 2.5, "start_value": 2.5, "current_value": 1.8},
    ]


    return output

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
def create_range_bar_chart(range_min, range_max, bar_start, bar_end, start_value, current_value, suffix=""):
    """Creates a horizontal range bar chart using Plotly."""

    fig = go.Figure()

    # --- Bar Vertical Positioning ---
    y_bottom = -0.2
    y_top = 0.3
    y_center = (y_top + y_bottom) / 2
    y_radius = (y_top - y_bottom) / 2

    # --- Create Rounded Gradient Bar ---
    y_res = 20  # Vertical resolution of the heatmap
    x_res = 200 # Horizontal resolution

    y_coords = np.linspace(y_bottom, y_top, y_res)
    x_coords = np.linspace(bar_start, bar_end, x_res)
    
    # Create a 2D grid of the x-coordinates for the color value
    z_values = np.tile(x_coords, (y_res, 1))

    # --- Create a mask for the rounded corners, adjusted for aspect ratio ---
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
    left_mask = (x_grid < left_center_x) & (((x_grid - left_center_x) / x_radius)**2 + ((y_grid - y_center) / y_radius)**2 > 1)
    
    # Mask for the right semi-circle
    right_mask = (x_grid > right_center_x) & (((x_grid - right_center_x) / x_radius)**2 + ((y_grid - y_center) / y_radius)**2 > 1)

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
        y=[y_center],
        mode='markers',
        marker=dict(
            symbol='diamond',
            color=get_color_from_scale(start_value, range_min, range_max),
            size=18,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hoverinfo='none',
        showlegend=False
    ))

    # Add current value circle marker
    fig.add_trace(go.Scatter(
        x=[current_value],
        y=[y_center],
        mode='markers',
        marker=dict(
            symbol='circle',
            color=get_color_from_scale(current_value, range_min, range_max),
            size=22,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        hoverinfo='none',
        showlegend=False
    ))
    
    # Calculate padding for the x-axis to make the bar appear shorter
    padding_percentage = 0.12  # 12% padding on each side
    total_range = range_max - range_min
    padding = total_range * padding_percentage if total_range > 0 else 1
    padded_min = range_min - padding
    padded_max = range_max + padding

    precision = get_rounding_precision(range_min, range_max)
    tick_format = f".{precision}f"

    fig.update_layout(
        height=90,
        margin=dict(l=1, r=1, t=1, b=30),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis=dict(
            showticklabels=True,
            showgrid=False,
            zeroline=False,
            range=[padded_min, padded_max],
            ticks="outside",
            tickcolor='lightgrey',
            tickfont=dict(size=10, color='grey'),
            tickformat=tick_format
        ),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-0.2, 0.8]),
        showlegend=False,
        shapes=[
            go.layout.Shape(
                type="rect",
                xref="x",
                yref="y",
                x0=range_min,
                y0=y_bottom,
                x1=range_max,
                y1=y_top,
                fillcolor="#E8E8E8",
                line_width=0,
                layer="below"
            )
        ]
    )

    return fig

# --- Streamlit App Layout ---
st.set_page_config(
    layout="wide", 
    page_title="Metrics Dashboard",
    initial_sidebar_state="collapsed",
)

st.title("Valuation Metrics")

# Fetch data
data = get_data()

# Loop through data and create a bordered container for each metric
for metric in data:
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([2.5, 1, 1, 6.5], vertical_alignment="center")
        suffix = metric.get("suffix", "")
        precision = get_rounding_precision(metric['range_min'], metric['range_max'])

        with col1:
            info_url = metric.get("info_url")
            info_icon_html = f"""
                <a href="{info_url}" target="_blank" style="text-decoration: none; padding: 4px 0px;">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 1.5C4.41 1.5 1.5 4.41 1.5 8C1.5 11.59 4.41 14.5 8 14.5C11.59 14.5 14.5 11.59 14.5 8C14.5 4.41 11.59 1.5 8 1.5ZM8 0.5C12.1421 0.5 15.5 3.85786 15.5 8C15.5 12.1421 12.1421 15.5 8 15.5C3.85786 15.5 0.5 12.1421 0.5 8C0.5 3.85786 3.85786 0.5 8 0.5Z" fill="#a0a0a0"/>
                        <path d="M7.5 11.5H8.5V7.5H7.5V11.5ZM8 6.5C8.55228 6.5 9 6.05228 9 5.5C9 4.94772 8.55228 4.5 8 4.5C7.44772 4.5 7 4.94772 7 5.5C7 6.05228 7.44772 6.5 8 6.5Z" fill="#a0a0a0"/>
                    </svg>
                </a>
            """ if info_url else ""
            
            st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style='font-size: clamp(0.9rem, 1.2vw, 1.1rem); font-weight: bold; text-align: left;'>{metric['title']}</span>
                    {info_icon_html}
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<p style='font-size: clamp(1.2rem, 2vw, 2.2rem); text-align: center;'>{metric['current_value']:.{precision}f}{suffix}</p>", unsafe_allow_html=True)

        with col3:
            # Calculate absolute change
            start_val = metric['start_value']
            current_val = metric['current_value']
            
            absolute_change = current_val - start_val
            color = "green" if absolute_change >= 0 else "red"
            symbol = "▲" if absolute_change >= 0 else "▼"
            
            st.markdown(f"<p style='font-size: clamp(0.8rem, 1.2vw, 1.0rem); color: {color}; text-align: center;'>{symbol} {absolute_change:.{precision}f}{suffix}</p>", unsafe_allow_html=True)


        with col4:
            chart = create_range_bar_chart(
                metric["range_min"], metric["range_max"], 
                metric["bar_start"], metric["bar_end"],
                metric["start_value"],
                metric["current_value"],
                suffix=suffix
            )
            st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False}) 

# --- Legend ---
with st.container(border=True):
    st.markdown("<h4 style='text-align: center;'>Legend</h4>", unsafe_allow_html=True)
    l_col1, l_col2, l_col3, l_col4 = st.columns(4, vertical_alignment="center")

    with l_col1:
        st.markdown("""
<div style="display: flex; align-items: center; justify-content: flex-start; gap: 10px; padding: 10px;">
    <svg width="28" height="28" viewBox="0 0 30 30">
        <circle cx="15" cy="15" r="12" fill="#FFD700" stroke="DarkSlateGrey" stroke-width="1.5"/>
    </svg>
    <span>Current Value</span>
</div>
        """, unsafe_allow_html=True)

    with l_col2:
        st.markdown("""
<div style="display: flex; align-items: center; justify-content: flex-start; gap: 10px; padding: 10px;">
    <svg width="28" height="28" viewBox="0 0 30 30">
        <path d="M15 2 L28 15 L15 28 L2 15 Z" fill="#90ee90" stroke="DarkSlateGrey" stroke-width="1.5"/>
    </svg>
    <span>30d Prior Value</span>
</div>
        """, unsafe_allow_html=True)

    with l_col3:
        st.markdown("""
<div style="display: flex; align-items: center; justify-content: flex-start; gap: 10px; padding: 10px;">
    <div style="width: 80px; height: 20px; background: linear-gradient(to right, green, yellow, red); border-radius: 10px;"></div>
    <span>1yr Range</span>
</div>
        """, unsafe_allow_html=True)

    with l_col4:
        st.markdown("""
<div style="display: flex; align-items: center; justify-content: flex-start; gap: 10px; padding: 10px;">
    <div style="width: 80px; height: 20px; background: #E8E8E8; border-radius: 10px;"></div>
    <span>Max Range</span>
</div>
        """, unsafe_allow_html=True) 