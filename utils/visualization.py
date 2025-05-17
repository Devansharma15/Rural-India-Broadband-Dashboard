import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.helper import get_color_scale

def create_choropleth(data, location_col, value_col, title, color_scale=None, hover_data=None):
    """
    Create a choropleth map visualization for Indian states.
    
    Args:
        data (DataFrame): Data containing state information
        location_col (str): Column name containing state names
        value_col (str): Column name containing values to plot
        title (str): Title for the chart
        color_scale (list, optional): Color scale for the map. Defaults to None.
        hover_data (list, optional): Additional columns to show on hover. Defaults to None.
        
    Returns:
        Figure: Plotly figure object
    """
    if color_scale is None:
        color_scale = get_color_scale('india_flag')
        
    fig = px.choropleth(
        data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations=location_col,
        color=value_col,
        color_continuous_scale=color_scale,
        hover_data=hover_data,
        title=title
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    
    return fig

def create_time_series(data, date_col, value_col, title, color="#FF9933"):
    """
    Create a time series line chart.
    
    Args:
        data (DataFrame): Data containing time series information
        date_col (str): Column name containing dates
        value_col (str): Column name containing values to plot
        title (str): Title for the chart
        color (str, optional): Line color. Defaults to "#FF9933" (Saffron from Indian flag).
        
    Returns:
        Figure: Plotly figure object
    """
    fig = px.line(
        data,
        x=date_col,
        y=value_col,
        title=title,
        line_shape='spline'
    )
    
    fig.update_traces(line=dict(color=color, width=3))
    
    return fig

def create_bar_chart(data, x_col, y_col, title, color=None, text_auto=False, orientation='v'):
    """
    Create a bar chart visualization.
    
    Args:
        data (DataFrame): Data for the bar chart
        x_col (str): Column name for x-axis
        y_col (str): Column name for y-axis
        title (str): Title for the chart
        color (str or list, optional): Bar color or column to use for color scale. Defaults to None.
        text_auto (bool or str, optional): Whether to show values on bars. Defaults to False.
        orientation (str, optional): 'v' for vertical, 'h' for horizontal. Defaults to 'v'.
        
    Returns:
        Figure: Plotly figure object
    """
    if orientation == 'v':
        fig = px.bar(
            data,
            x=x_col,
            y=y_col,
            title=title,
            color=color,
            text_auto=text_auto
        )
    else:
        fig = px.bar(
            data,
            y=x_col,
            x=y_col,
            title=title,
            color=color,
            text_auto=text_auto,
            orientation='h'
        )
    
    return fig

def create_grouped_bar_chart(data, x_col, y_cols, title, barmode='group', color_sequence=None):
    """
    Create a grouped bar chart with multiple series.
    
    Args:
        data (DataFrame): Data for the chart
        x_col (str): Column name for x-axis
        y_cols (list): List of column names for different bar groups
        title (str): Title for the chart
        barmode (str, optional): 'group' or 'stack'. Defaults to 'group'.
        color_sequence (list, optional): List of colors. Defaults to None.
        
    Returns:
        Figure: Plotly figure object
    """
    if color_sequence is None:
        color_sequence = ["#FF9933", "#138808"]  # Saffron and Green from Indian flag
        
    fig = px.bar(
        data,
        x=x_col,
        y=y_cols,
        title=title,
        barmode=barmode,
        color_discrete_sequence=color_sequence
    )
    
    return fig

def create_pie_chart(data, names_col, values_col, title, color_sequence=None):
    """
    Create a pie chart visualization.
    
    Args:
        data (DataFrame): Data for the pie chart
        names_col (str): Column name for pie slice labels
        values_col (str): Column name for pie slice values
        title (str): Title for the chart
        color_sequence (list, optional): List of colors. Defaults to None.
        
    Returns:
        Figure: Plotly figure object
    """
    fig = px.pie(
        data,
        names=names_col,
        values=values_col,
        title=title,
        color_discrete_sequence=color_sequence
    )
    
    return fig

def create_scatter_plot(data, x_col, y_col, title, color=None, size=None, hover_name=None, text=None):
    """
    Create a scatter plot visualization.
    
    Args:
        data (DataFrame): Data for the scatter plot
        x_col (str): Column name for x-axis
        y_col (str): Column name for y-axis
        title (str): Title for the chart
        color (str, optional): Column name for color encoding. Defaults to None.
        size (str, optional): Column name for size encoding. Defaults to None.
        hover_name (str, optional): Column to use for hover labels. Defaults to None.
        text (str, optional): Column to use for text labels. Defaults to None.
        
    Returns:
        Figure: Plotly figure object
    """
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        title=title,
        color=color,
        size=size,
        hover_name=hover_name,
        text=text
    )
    
    if text:
        fig.update_traces(textposition='top center')
    
    return fig

def create_heatmap(data_frame, x_col, y_col, value_col, title, color_scale='Viridis'):
    """
    Create a heatmap visualization.
    
    Args:
        data_frame (DataFrame): Data for the heatmap
        x_col (str): Column name for x-axis categories
        y_col (str): Column name for y-axis categories
        value_col (str): Column name for values/color intensity
        title (str): Title for the chart
        color_scale (str, optional): Color scale. Defaults to 'Viridis'.
        
    Returns:
        Figure: Plotly figure object
    """
    # Create pivot table for heatmap
    pivot_data = data_frame.pivot(index=y_col, columns=x_col, values=value_col)
    
    fig = px.imshow(
        pivot_data,
        title=title,
        color_continuous_scale=color_scale,
        text_auto=True
    )
    
    return fig

def create_gauge_chart(value, title, min_val=0, max_val=100, reference=None, threshold=None):
    """
    Create a gauge chart visualization.
    
    Args:
        value (float): Current value for the gauge
        title (str): Title for the chart
        min_val (float, optional): Minimum value. Defaults to 0.
        max_val (float, optional): Maximum value. Defaults to 100.
        reference (float, optional): Reference value for delta. Defaults to None.
        threshold (float, optional): Threshold value to mark. Defaults to None.
        
    Returns:
        Figure: Plotly figure object
    """
    # Calculate the percentage for the gauge
    percentage = (value - min_val) / (max_val - min_val) * 100
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title},
        delta={'reference': reference if reference is not None else value},
        gauge={
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': "#FF9933"},
            'steps': [
                {'range': [min_val, (max_val-min_val)*0.3 + min_val], 'color': "#EEEEEE"},
                {'range': [(max_val-min_val)*0.3 + min_val, (max_val-min_val)*0.7 + min_val], 'color': "#DDDDDD"},
                {'range': [(max_val-min_val)*0.7 + min_val, max_val], 'color': "#CCCCCC"}
            ],
            'threshold': {
                'line': {'color': "#138808", 'width': 4},
                'thickness': 0.75,
                'value': threshold if threshold is not None else max_val * 0.8
            }
        }
    ))
    
    return fig