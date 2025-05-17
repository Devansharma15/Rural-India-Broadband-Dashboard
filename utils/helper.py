import pandas as pd
import numpy as np
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os

@st.cache_data
def load_image_from_url(url):
    """
    Load an image from a URL with caching.
    
    Args:
        url (str): URL of the image
        
    Returns:
        Image: Loaded image object or default placeholder
    """
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch image, status code: {response.status_code}")
        
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        # Create a placeholder image with text
        placeholder = Image.new('RGB', (800, 400), color=(240, 240, 240))
        # Don't show the error to users, just return the placeholder
        return placeholder

def format_large_number(num):
    """
    Format large numbers for display with appropriate suffixes.
    
    Args:
        num (float): Number to format
        
    Returns:
        str: Formatted number string
    """
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.2f}K"
    else:
        return f"{num:.2f}"

def format_percentage(num, decimals=1):
    """
    Format a number as a percentage.
    
    Args:
        num (float): Number to format (0.1 = 10%)
        decimals (int, optional): Number of decimal places. Defaults to 1.
        
    Returns:
        str: Formatted percentage string
    """
    return f"{num*100:.{decimals}f}%"

@st.cache_data
def get_state_region_map():
    """
    Get a mapping of Indian states to their geographic regions.
    
    Returns:
        dict: Dictionary mapping state names to region names
    """
    regions = {
        'North': ['Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Punjab', 'Rajasthan', 'Uttar Pradesh', 'Uttarakhand'],
        'South': ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana'],
        'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal'],
        'West': ['Goa', 'Gujarat', 'Maharashtra'],
        'Central': ['Chhattisgarh', 'Madhya Pradesh'],
        'Northeast': ['Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Sikkim', 'Tripura']
    }
    
    # Create the reverse mapping
    state_to_region = {}
    for region, states in regions.items():
        for state in states:
            state_to_region[state] = region
            
    return state_to_region

def calculate_growth_rate(start_value, end_value, time_periods):
    """
    Calculate compound annual growth rate.
    
    Args:
        start_value (float): Starting value
        end_value (float): Ending value
        time_periods (float): Number of time periods (typically years)
        
    Returns:
        float: Growth rate as a decimal (0.05 = 5%)
    """
    if start_value <= 0 or time_periods <= 0:
        return 0
    
    return (end_value / start_value) ** (1 / time_periods) - 1

def interpolate_missing_values(df, date_column, value_column, method='linear'):
    """
    Interpolate missing values in a time series.
    
    Args:
        df (DataFrame): DataFrame containing time series data
        date_column (str): Name of column containing dates
        value_column (str): Name of column containing values to interpolate
        method (str, optional): Interpolation method. Defaults to 'linear'.
        
    Returns:
        DataFrame: DataFrame with interpolated values
    """
    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Sort by date
    df = df.sort_values(date_column)
    
    # Interpolate
    df[value_column] = df[value_column].interpolate(method=method)
    
    return df

def create_date_features(df, date_column):
    """
    Create additional date-based features from a date column.
    
    Args:
        df (DataFrame): DataFrame containing date column
        date_column (str): Name of date column
        
    Returns:
        DataFrame: DataFrame with additional date features
    """
    # Ensure date column is datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Extract features
    df['year'] = df[date_column].dt.year
    df['quarter'] = df[date_column].dt.quarter
    df['month'] = df[date_column].dt.month
    df['month_name'] = df[date_column].dt.month_name()
    df['is_quarter_end'] = df[date_column].dt.is_quarter_end
    df['is_year_end'] = df[date_column].dt.is_year_end
    
    return df

def get_color_scale(theme='india_flag'):
    """
    Get a color scale based on a theme.
    
    Args:
        theme (str, optional): Color theme name. Defaults to 'india_flag'.
        
    Returns:
        list: List of colors for the scale
    """
    if theme == 'india_flag':
        return ["#FFFFFF", "#FF9933", "#138808"]  # White, Saffron, Green
    elif theme == 'blue_gradient':
        return ["#E8F4F8", "#8BBBD9", "#4B86B4", "#2A4D69"]  # Light to dark blue
    elif theme == 'green_gradient':
        return ["#E8F8E8", "#8BD98B", "#4BB44B", "#2A692A"]  # Light to dark green
    elif theme == 'sequential':
        return ['#FFFFD9', '#EDF8B1', '#C7E9B4', '#7FCDBB', '#41B6C4', '#1D91C0', '#225EA8', '#0C2C84']
    else:
        return None  # Use default color scale

def add_region_to_data(df, state_column):
    """
    Add a region column to a DataFrame based on state names.
    
    Args:
        df (DataFrame): DataFrame containing state data
        state_column (str): Name of column containing state names
        
    Returns:
        DataFrame: DataFrame with additional region column
    """
    state_region_map = get_state_region_map()
    df['region'] = df[state_column].map(state_region_map)
    return df

def display_formatter():
    """
    Return a dictionary of formatting functions for displaying data values.
    
    Returns:
        dict: Dictionary of formatting functions
    """
    return {
        'large_number': format_large_number,
        'percentage': format_percentage,
        'growth_rate': lambda x: format_percentage(x, decimals=2)
    }