import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_generator import generate_state_data, generate_district_data
from utils.helper import load_image_from_url

# Page configuration
st.set_page_config(
    page_title="Geographic Analysis - Rural India Broadband",
    page_icon="🗺️",
    layout="wide"
)

# Title and introduction
st.title("Geographic Analysis of Broadband Connectivity")
st.markdown("""
Explore the geographic distribution of broadband connectivity across rural India.
Identify underserved regions and connectivity hotspots to inform strategic decisions
for infrastructure development and digital inclusion initiatives.
""")

# Display a banner image
st.image(
    load_image_from_url("https://pixabay.com/get/gc33443055cc29d03b79702173a4a13707f04ea2308ae05c55dae4ebe057210cb0ea71de91551c69bc868c082a26a760a5f7b7e3da61d513e8737dcab86658b35_1280.jpg"),
    caption="Rural Connectivity Landscape",
    use_container_width=True
)

# Load data
state_data = generate_state_data()
district_data = generate_district_data()

# Filters
st.sidebar.header("Filters")
selected_metric = st.sidebar.selectbox(
    "Select Metric",
    ["Broadband Penetration", "Subscriber Count", "Mobile Data Usage", "Fixed Broadband Usage"]
)

metric_mapping = {
    "Broadband Penetration": "broadband_penetration",
    "Subscriber Count": "subscribers",
    "Mobile Data Usage": "mobile_data_usage",
    "Fixed Broadband Usage": "fixed_broadband_usage"
}

selected_column = metric_mapping[selected_metric]

# State Level Choropleth Map
st.header("State-Level Analysis")

# Customize color scale based on metric
if selected_column == "broadband_penetration":
    color_scale = ["#FFFFFF", "#138808"]  # White to Green (Indian flag colors)
    range_val = (0, 0.5)  # 0 to 50%
elif selected_column in ["subscribers", "mobile_data_usage", "fixed_broadband_usage"]:
    color_scale = ["#FFFFFF", "#FF9933"]  # White to Saffron (Indian flag colors)
    range_val = None
else:
    color_scale = ["#FFFFFF", "#0000FF"]  # White to Blue
    range_val = None

fig = px.choropleth(
    state_data,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='state',
    color=selected_column,
    color_continuous_scale=color_scale,
    range_color=range_val,
    hover_data=['state', 'subscribers', 'population', 'broadband_penetration'],
    labels={
        'broadband_penetration': 'Penetration Rate', 
        'subscribers': 'Subscribers', 
        'population': 'Population',
        'mobile_data_usage': 'Mobile Data (GB/user/month)',
        'fixed_broadband_usage': 'Fixed BB (GB/user/month)'
    }
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# State ranking
st.subheader("State Rankings")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Top 5 States")
    top_states = state_data.sort_values(by=selected_column, ascending=False).head(5)
    
    # Create a horizontal bar chart for top states
    fig = px.bar(
        top_states,
        y='state',
        x=selected_column,
        orientation='h',
        color=selected_column,
        color_continuous_scale=color_scale,
        labels={selected_column: selected_metric, 'state': 'State'},
        text_auto=True
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Bottom 5 States")
    bottom_states = state_data.sort_values(by=selected_column).head(5)
    
    # Create a horizontal bar chart for bottom states
    fig = px.bar(
        bottom_states,
        y='state',
        x=selected_column,
        orientation='h',
        color=selected_column,
        color_continuous_scale=color_scale,
        labels={selected_column: selected_metric, 'state': 'State'},
        text_auto=True
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# Geographic disparities
st.header("Geographic Disparities")

# Group states by region and calculate average metrics
region_data = state_data.copy()
# Define regions (simplified for this example)
region_mapping = {
    'Andhra Pradesh': 'South', 'Karnataka': 'South', 'Kerala': 'South', 'Tamil Nadu': 'South', 'Telangana': 'South',
    'Gujarat': 'West', 'Maharashtra': 'West', 'Goa': 'West', 'Rajasthan': 'West',
    'Bihar': 'East', 'Jharkhand': 'East', 'Odisha': 'East', 'West Bengal': 'East',
    'Delhi': 'North', 'Haryana': 'North', 'Himachal Pradesh': 'North', 'Jammu and Kashmir': 'North', 
    'Punjab': 'North', 'Uttar Pradesh': 'North', 'Uttarakhand': 'North',
    'Assam': 'Northeast', 'Arunachal Pradesh': 'Northeast', 'Manipur': 'Northeast', 
    'Meghalaya': 'Northeast', 'Mizoram': 'Northeast', 'Nagaland': 'Northeast', 'Tripura': 'Northeast',
    'Chhattisgarh': 'Central', 'Madhya Pradesh': 'Central'
}
region_data['region'] = region_data['state'].map(region_mapping)

# Aggregate by region
region_summary = region_data.groupby('region').agg({
    'broadband_penetration': 'mean',
    'subscribers': 'sum',
    'population': 'sum',
    'mobile_data_usage': 'mean',
    'fixed_broadband_usage': 'mean'
}).reset_index()

# Calculate penetration from aggregates 
region_summary['calculated_penetration'] = region_summary['subscribers'] / region_summary['population']

col1, col2 = st.columns(2)

with col1:
    # Regional comparison chart
    fig = px.bar(
        region_summary,
        x='region',
        y='broadband_penetration',
        color='region',
        labels={'broadband_penetration': 'Broadband Penetration', 'region': 'Region'},
        title="Broadband Penetration by Region",
        text_auto=True
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Mobile vs Fixed usage by region
    fig = px.bar(
        region_summary,
        x='region',
        y=['mobile_data_usage', 'fixed_broadband_usage'],
        barmode='group',
        labels={
            'value': 'Average Data Usage (GB/month)', 
            'region': 'Region',
            'variable': 'Connection Type'
        },
        title="Mobile vs Fixed Broadband Usage by Region",
        color_discrete_sequence=['#FF9933', '#138808']  # Saffron and Green
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Key insights
st.header("Key Geographic Insights")

st.markdown("""
Based on the analysis of geographic distribution of broadband connectivity across rural India:

1. **Regional Disparities**: There is a clear north-south divide in broadband penetration, with southern states generally having higher connectivity rates.

2. **Topographical Challenges**: Mountainous regions and remote areas show consistently lower penetration rates, highlighting the challenge of infrastructure deployment.

3. **Urban Proximity Effect**: Rural areas closer to major urban centers tend to have better connectivity than deeply rural regions.

4. **Mobile vs Fixed Preference**: Eastern and North-Eastern regions show stronger preference for mobile data over fixed broadband connections.

5. **Growth Potential**: States with low current penetration but high population density represent high-impact opportunities for infrastructure investment.
""")

# Show sample of district-level data
with st.expander("District-Level Data Sample"):
    st.dataframe(district_data.head(10))
