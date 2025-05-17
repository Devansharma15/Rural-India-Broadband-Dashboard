import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add current directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import pages
from Geographic_Analysis import app as geographic_analysis
from Demographic_Analysis import app as demographic_analysis
from Time_Series_Analysis import app as time_series_analysis
from Usage_Patterns import app as usage_patterns
from Insights_Recommendations import app as insights_recommendations

# Set page config
st.set_page_config(
    page_title="Rural India Broadband Connectivity Dashboard",
    page_icon="📊",
    layout="wide"
)

# Define the pages
pages = {
    "Geographic Analysis": geographic_analysis,
    "Demographic Analysis": demographic_analysis,
    "Time Series Analysis": time_series_analysis,
    "Usage Patterns": usage_patterns,
    "Insights & Recommendations": insights_recommendations
}

# Add sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(pages.keys()))

# Display the app title
if selection == "Geographic Analysis":
    st.sidebar.info("""
    Explore the geographic distribution of broadband connectivity across rural India. 
    Identify underserved regions and connectivity hotspots.
    """)
elif selection == "Demographic Analysis":
    st.sidebar.info("""
    Examine how demographic factors influence broadband connectivity and usage patterns 
    across rural India.
    """)
elif selection == "Time Series Analysis":
    st.sidebar.info("""
    Analyze the growth and trends in broadband connectivity over time across rural India.
    """)
elif selection == "Usage Patterns":
    st.sidebar.info("""
    Explore how rural communities are using the internet, including data consumption patterns, 
    preferred devices, and popular services.
    """)
elif selection == "Insights & Recommendations":
    st.sidebar.info("""
    Actionable recommendations for improving rural broadband connectivity based on 
    all analyses.
    """)

# Display the selected page
pages[selection]()

# Add footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.markdown("""
This dashboard provides a comprehensive analysis of rural India's broadband connectivity
to support strategic decision-making for digital inclusion initiatives.
""")
st.sidebar.markdown("© 2025 Rural Broadband Initiative")
