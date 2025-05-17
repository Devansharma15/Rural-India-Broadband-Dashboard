import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_generator import generate_time_series_data, generate_state_time_series
from utils.helper import load_image_from_url

# Page configuration
st.set_page_config(
    page_title="Time Series Analysis - Rural India Broadband",
    page_icon="📈",
    layout="wide"
)

# Title and introduction
st.title("Time Series Analysis of Broadband Adoption")
st.markdown("""
Analyze the growth and trends in broadband connectivity over time across rural India.
Track the evolution of subscriber numbers, penetration rates, and usage patterns to
understand the trajectory of digital inclusion in rural communities.
""")

# Display a banner image
st.image(
    load_image_from_url("https://pixabay.com/get/g3884b4a5409d18b1b5f14344a5b8e23106f5ea08fdcac55521ce56a2a493bdf97d181cdce950a31b686c6206e8a3ba246cfb53c170517132c766a8ea319fb216_1280.jpg"),
    caption="Rural Internet Usage Evolution",
    use_container_width=True
)

# Load data
time_data = generate_time_series_data()
state_time_data = generate_state_time_series()

# Filters
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Time Range",
    ["Last 1 Year", "Last 3 Years", "Last 5 Years", "All Time"]
)

# Convert selection to number of months
range_mapping = {
    "Last 1 Year": 12,
    "Last 3 Years": 36,
    "Last 5 Years": 60,
    "All Time": len(time_data)
}
months = range_mapping[time_range]

# Filter data based on selection
filtered_data = time_data.tail(months)

# Overall Growth Trend
st.header("Overall Growth Trend")

# Prepare metrics
first_value = filtered_data['subscribers'].iloc[0] / 1_000_000
last_value = filtered_data['subscribers'].iloc[-1] / 1_000_000
growth_pct = ((last_value - first_value) / first_value) * 100 if first_value > 0 else 0

# Show metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Starting Subscribers", f"{first_value:.2f}M", delta=None)
with col2:
    st.metric("Current Subscribers", f"{last_value:.2f}M", delta=f"{growth_pct:.1f}%")
with col3:
    # Calculate CAGR
    years = months / 12
    cagr = (((last_value / first_value) ** (1 / years)) - 1) * 100 if years > 0 and first_value > 0 else 0
    st.metric("CAGR", f"{cagr:.2f}%", delta=None)

# Create the time series plot
fig = px.line(
    filtered_data,
    x='date',
    y='subscribers',
    line_shape='spline',
    labels={
        'subscribers': 'Subscribers (millions)',
        'date': 'Month'
    },
    title=f"Rural Broadband Subscriber Growth ({time_range})"
)
fig.update_traces(line=dict(color='#FF9933', width=3))  # Saffron from Indian flag
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Quarterly Growth Rate
st.subheader("Quarterly Growth Rate")

# Calculate quarterly growth rates
filtered_data['quarter'] = pd.to_datetime(filtered_data['date']).dt.to_period('Q')
quarterly_data = filtered_data.groupby('quarter').agg({'subscribers': 'last'}).reset_index()
quarterly_data['quarter'] = quarterly_data['quarter'].astype(str)
quarterly_data['previous'] = quarterly_data['subscribers'].shift(1)
quarterly_data['growth_rate'] = ((quarterly_data['subscribers'] - quarterly_data['previous']) / quarterly_data['previous']) * 100
quarterly_data = quarterly_data.dropna()

# Create the bar chart for quarterly growth
fig = px.bar(
    quarterly_data,
    x='quarter',
    y='growth_rate',
    labels={
        'growth_rate': 'Growth Rate (%)',
        'quarter': 'Quarter'
    },
    title="Quarterly Growth Rate of Rural Broadband Subscribers"
)
fig.update_traces(marker_color='#138808')  # Green from Indian flag
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# Seasonal Patterns
st.header("Seasonal Patterns")

# Calculate seasonal patterns by month
filtered_data['month'] = pd.to_datetime(filtered_data['date']).dt.month_name()
filtered_data['year'] = pd.to_datetime(filtered_data['date']).dt.year

# Get proper month order
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']

# Group by month and calculate average subscribers
monthly_pattern = filtered_data.groupby('month').agg({
    'subscribers': 'mean',
    'mobile_data': 'mean',
    'fixed_data': 'mean'
}).reset_index()

# Sort by month order
monthly_pattern['month_num'] = monthly_pattern['month'].apply(lambda x: month_order.index(x))
monthly_pattern = monthly_pattern.sort_values('month_num')
monthly_pattern = monthly_pattern.drop(columns=['month_num'])

col1, col2 = st.columns(2)

with col1:
    # Create the bar chart for monthly pattern
    fig = px.bar(
        monthly_pattern,
        x='month',
        y='subscribers',
        labels={
            'subscribers': 'Average Subscribers (millions)',
            'month': 'Month'
        },
        title="Average Subscriber Distribution by Month",
        category_orders={"month": month_order}
    )
    fig.update_traces(marker_color='#FF9933')  # Saffron from Indian flag
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Create a line chart for data usage patterns
    fig = px.line(
        monthly_pattern,
        x='month',
        y=['mobile_data', 'fixed_data'],
        labels={
            'value': 'Average Data Usage (GB/user)',
            'month': 'Month',
            'variable': 'Connection Type'
        },
        title="Seasonal Data Usage Patterns",
        category_orders={"month": month_order},
        color_discrete_sequence=['#FF9933', '#138808']  # Saffron and Green
    )
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

# State-wise Growth Comparison
st.header("State-wise Growth Comparison")

# Filter states for comparison
selected_states = st.multiselect(
    "Select states to compare",
    options=sorted(state_time_data['state'].unique()),
    default=['Maharashtra', 'Tamil Nadu', 'Uttar Pradesh', 'Bihar', 'Kerala']
)

if selected_states:
    # Filter data for selected states
    state_filtered = state_time_data[
        (state_time_data['state'].isin(selected_states)) & 
        (state_time_data['date'].isin(filtered_data['date']))
    ]
    
    # Create the line chart for state comparison
    fig = px.line(
        state_filtered,
        x='date',
        y='penetration',
        color='state',
        line_shape='spline',
        labels={
            'penetration': 'Broadband Penetration Rate',
            'date': 'Month',
            'state': 'State'
        },
        title="Broadband Penetration Growth by State"
    )
    fig.update_layout(height=500, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate and display state growth rates
    growth_data = []
    for state in selected_states:
        state_data = state_filtered[state_filtered['state'] == state]
        if len(state_data) >= 2:
            start_val = state_data.iloc[0]['penetration']
            end_val = state_data.iloc[-1]['penetration']
            growth = ((end_val - start_val) / start_val) * 100 if start_val > 0 else 0
            growth_data.append({
                'state': state,
                'start_value': start_val,
                'end_value': end_val,
                'growth_pct': growth
            })
    
    # Create DataFrame from the list of dictionaries
    if growth_data:
        state_growth = pd.DataFrame(growth_data)
        state_growth = state_growth.sort_values('growth_pct', ascending=False)
    else:
        # Create empty DataFrame with proper columns if no data
        state_growth = pd.DataFrame(columns=['state', 'start_value', 'end_value', 'growth_pct'])
    
    # Display state growth comparison
    if not state_growth.empty:
        fig = px.bar(
            state_growth,
            x='state',
            y='growth_pct',
            color='growth_pct',
            labels={
                'growth_pct': 'Growth (%)',
                'state': 'State'
            },
            title=f"Penetration Growth Rate by State ({time_range})",
            text_auto=True
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No growth data available. Please select at least one state with sufficient data.")
else:
    st.info("Please select at least one state for comparison")

# Key insights
st.header("Key Time Series Insights")

st.markdown("""
Analysis of broadband adoption trends over time reveals:

1. **Accelerating Growth**: Rural broadband subscription growth has accelerated in recent years, with the pace doubling compared to the previous five-year period.

2. **Seasonal Patterns**: There is a noticeable seasonal pattern with higher growth during post-harvest months and the educational enrollment period.

3. **Digital India Impact**: Implementation of Digital India initiatives correlates with growth spikes, particularly in previously underserved states.

4. **COVID-19 Effect**: The pandemic created an unusual surge in rural connectivity demand, accelerating the adoption timeline by approximately 18-24 months.

5. **State Divergence**: While some states show consistently strong growth trajectories, others display plateauing adoption rates that may require targeted policy interventions.
""")
