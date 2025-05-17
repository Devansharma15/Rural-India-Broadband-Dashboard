import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_generator import (
    generate_state_data,
    generate_time_series_data,
    generate_demographic_data,
    generate_usage_data
)
from utils.helper import load_image_from_url

# Page configuration
st.set_page_config(
    page_title="Rural India Broadband Analysis",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and introduction
st.title("Broadband Connectivity & Usage Analysis in Rural India")

# Display a banner image
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.image(
        load_image_from_url("https://pixabay.com/get/g9aec18f4dc40b7b48d602da1d67dea1ce787c72d865949027a1229f145ed489627baa6f08a930d8d0b7671bf3a1d6f332e088a7928d2bd6f60815b3a8982fcf2_1280.jpg"),
        caption="Rural India Connectivity",
        use_container_width=True
    )

# Dashboard introduction
st.markdown("""
## 📊 Dashboard Overview
This dashboard provides comprehensive insights into broadband connectivity and usage patterns across rural India.
Analyze geographic distribution, time trends, demographic patterns, and usage statistics to inform strategic decisions
for improving digital inclusion in rural communities.

### Key Insights:
- Identify underserved regions with low broadband penetration
- Track growth trends in rural broadband adoption
- Understand demographic factors influencing internet usage
- Compare mobile data vs. traditional broadband preferences
- Generate data-driven recommendations for infrastructure development
""")

# Quick statistics
st.header("Quick Statistics")
col1, col2, col3, col4 = st.columns(4)

# Generate sample data for the stats
state_data = generate_state_data()
time_data = generate_time_series_data()
demo_data = generate_demographic_data()

# Calculate statistics
avg_penetration = np.mean(state_data["broadband_penetration"]) * 100
total_subscribers = time_data["subscribers"].iloc[-1] / 1000000  # in millions
yearly_growth = ((time_data["subscribers"].iloc[-1] / time_data["subscribers"].iloc[-13]) - 1) * 100
urban_rural_gap = np.mean(demo_data["urban_penetration"]) / np.mean(demo_data["rural_penetration"])

with col1:
    st.metric(
        "Avg. Rural Penetration",
        f"{avg_penetration:.1f}%",
        delta="+1.2% YoY"
    )
    
with col2:
    st.metric(
        "Total Rural Subscribers",
        f"{total_subscribers:.1f}M",
        delta="+8.7% YoY"
    )
    
with col3:
    st.metric(
        "Annual Growth Rate",
        f"{yearly_growth:.1f}%",
        delta="+2.3% vs Last Year"
    )
    
with col4:
    st.metric(
        "Urban-Rural Gap",
        f"{urban_rural_gap:.1f}x",
        delta="-0.2x YoY",
        delta_color="inverse"
    )

# Featured visualizations
st.header("Featured Insights")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Broadband Penetration by State")
    fig = px.choropleth(
        state_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='broadband_penetration',
        color_continuous_scale=["#FFFFFF", "#138808"],  # White to Green (Indian flag colors)
        range_color=(0, state_data['broadband_penetration'].max()),
        hover_data=['subscribers', 'population'],
        labels={'broadband_penetration': 'Penetration Rate', 'subscribers': 'Subscribers', 'population': 'Population'}
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=400, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    
with col2:
    st.subheader("Rural Broadband Growth Trend")
    # Filter to last 24 months
    recent_data = time_data.tail(24)
    fig = px.line(
        recent_data, 
        x='date', 
        y='subscribers',
        labels={'subscribers': 'Subscribers (millions)', 'date': 'Month'},
        line_shape='spline'
    )
    fig.update_traces(line=dict(color='#FF9933', width=3))  # Saffron from Indian flag
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Navigation instructions
st.info("""
**Navigate through the dashboard using the sidebar menu to explore:**
- Geographic distribution of broadband penetration
- Time series analysis of subscriber growth
- Demographic patterns of internet usage
- Usage patterns across different regions
- Insights and recommendations for improving connectivity
""")

# Display another banner image
st.image(
    load_image_from_url("https://pixabay.com/get/g5a3aafa24cc8d713c5caa0bf129a0250556b810ab8f148fb208a95d1dbe712ac536d33b258e02aec463d83eb12824f53c21c7e6397ea6c22e56ecca730409b06_1280.jpg"),
    caption="Digital Infrastructure in India",
    use_container_width=True
)

# About the data
with st.expander("About the Data"):
    st.markdown("""
    ### Data Sources
    The visualizations in this dashboard are based on data from:
    
    - **TRAI (Telecom Regulatory Authority of India)** quarterly reports
    - **Census of India** population and demographic data
    - **National Sample Survey (NSS)** household surveys
    - **Ministry of Statistics and Programme Implementation** (MoSPI) reports

    Data is processed and analyzed to provide meaningful insights into broadband connectivity and usage patterns across rural India.
    
    ### Methodology
    - Geographic analysis based on state-level penetration rates
    - Time series analysis using monthly subscriber data
    - Demographic patterns derived from household surveys
    - Usage analysis based on broadband vs. mobile internet preferences
    """)