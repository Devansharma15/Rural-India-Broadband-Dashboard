import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_generator import generate_usage_data, generate_service_usage_data

def app():
    # Title and introduction
    st.title("Internet Usage Patterns in Rural India")
    st.markdown("""
    Explore how rural communities are using the internet, including data consumption patterns,
    preferred devices, popular services, and bandwidth requirements. These insights help
    in designing appropriate connectivity solutions and digital services for rural users.
    """)

    # Load data
    usage_data = generate_usage_data()
    service_data = generate_service_usage_data()

    # Filters
    st.sidebar.header("Filters")
    selected_states = st.sidebar.multiselect(
        "Filter by State",
        options=sorted(usage_data['state'].unique()),
        default=[]
    )

    # Filter data if states are selected
    if selected_states:
        filtered_usage = usage_data[usage_data['state'].isin(selected_states)]
        filtered_service = service_data[service_data['state'].isin(selected_states)]
    else:
        filtered_usage = usage_data
        filtered_service = service_data

    # Mobile vs Fixed Broadband Usage
    st.header("Mobile vs Fixed Broadband Usage")

    # Calculate average usage by connection type
    connection_usage = filtered_usage.groupby('state').agg({
        'mobile_data': 'mean',
        'fixed_data': 'mean',
        'total_subscribers': 'sum'
    }).reset_index()

    connection_usage['mobile_share'] = connection_usage['mobile_data'] / (connection_usage['mobile_data'] + connection_usage['fixed_data'])
    connection_usage['fixed_share'] = connection_usage['fixed_data'] / (connection_usage['mobile_data'] + connection_usage['fixed_data'])

    # Sort by total subscribers for relevance
    connection_usage = connection_usage.sort_values('total_subscribers', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        # Create a stacked bar chart for connection type share
        fig = px.bar(
            connection_usage,
            x='state',
            y=['mobile_share', 'fixed_share'],
            title="Distribution of Data Usage by Connection Type",
            labels={
                'value': 'Share of Total Data Consumption',
                'state': 'State',
                'variable': 'Connection Type'
            },
            color_discrete_map={
                'mobile_share': '#FF9933',  # Saffron
                'fixed_share': '#138808'    # Green
            }
        )
        fig.update_layout(height=500, barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Create a scatter plot with size based on total subscribers
        fig = px.scatter(
            connection_usage,
            x='mobile_data',
            y='fixed_data',
            size='total_subscribers',
            hover_name='state',
            labels={
                'mobile_data': 'Mobile Data Usage (GB/month/user)',
                'fixed_data': 'Fixed Broadband Usage (GB/month/user)',
                'total_subscribers': 'Total Subscribers'
            },
            title="Mobile vs Fixed Broadband Usage by State",
        )
        
        # Add a 45-degree line
        max_val = max(connection_usage['mobile_data'].max(), connection_usage['fixed_data'].max())
        fig.add_trace(
            go.Scatter(
                x=[0, max_val],
                y=[0, max_val],
                mode='lines',
                line=dict(color='gray', dash='dash'),
                name='Equal Usage'
            )
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

    # Device Usage Analysis
    st.header("Device Usage Analysis")

    # Get device usage data
    device_data = filtered_usage[['state', 'smartphone_pct', 'feature_phone_pct', 'desktop_pct', 'tablet_pct']]
    device_melt = pd.melt(
        device_data,
        id_vars=['state'],
        value_vars=['smartphone_pct', 'feature_phone_pct', 'desktop_pct', 'tablet_pct'],
        var_name='device_type',
        value_name='percentage'
    )

    # Clean up device type names
    device_melt['device_type'] = device_melt['device_type'].str.replace('_pct', '')
    device_melt['device_type'] = device_melt['device_type'].str.capitalize()

    # Calculate national average
    national_device = device_melt.groupby('device_type')['percentage'].mean().reset_index()

    # Create a pie chart for device usage
    fig = px.pie(
        national_device,
        names='device_type',
        values='percentage',
        title="Distribution of Internet Usage by Device Type",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Create a bar chart for device usage by state
    fig = px.bar(
        device_melt,
        x='state',
        y='percentage',
        color='device_type',
        barmode='stack',
        labels={
            'percentage': 'Percentage of Usage',
            'state': 'State',
            'device_type': 'Device Type'
        },
        title="Device Usage Patterns by State"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Popular Services and Applications
    st.header("Popular Services and Applications")

    # Get service usage data
    service_summary = filtered_service.groupby('service').agg({
        'usage_percentage': 'mean',
        'data_volume': 'mean'
    }).reset_index()

    service_summary = service_summary.sort_values('usage_percentage', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        # Create a bar chart for service popularity
        fig = px.bar(
            service_summary,
            y='service',
            x='usage_percentage',
            orientation='h',
            labels={
                'usage_percentage': 'Usage Percentage',
                'service': 'Service/Application'
            },
            title="Most Popular Online Services in Rural India",
            text_auto=True
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Create a bar chart for data consumption by service
        fig = px.bar(
            service_summary,
            y='service',
            x='data_volume',
            orientation='h',
            labels={
                'data_volume': 'Average Data Volume (GB/month/user)',
                'service': 'Service/Application'
            },
            title="Data Consumption by Service Type",
            text_auto=True
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    # Usage Time Patterns
    st.header("Usage Time Patterns")

    # Create time of day data
    time_periods = ['Early Morning (5-8 AM)', 'Morning (8-12 PM)', 'Afternoon (12-4 PM)', 
                    'Evening (4-8 PM)', 'Night (8-12 AM)', 'Late Night (12-5 AM)']

    # Sample data - would normally come from actual usage patterns
    time_data = pd.DataFrame({
        'time_period': time_periods,
        'weekday_usage': [0.05, 0.15, 0.20, 0.35, 0.20, 0.05],
        'weekend_usage': [0.03, 0.10, 0.15, 0.30, 0.30, 0.12]
    })

    # Melt the data for plotting
    time_melt = pd.melt(
        time_data,
        id_vars=['time_period'],
        value_vars=['weekday_usage', 'weekend_usage'],
        var_name='day_type',
        value_name='usage_share'
    )

    # Clean up names
    time_melt['day_type'] = time_melt['day_type'].str.replace('_usage', '')
    time_melt['day_type'] = time_melt['day_type'].str.capitalize()

    # Create a grouped bar chart for usage time patterns
    fig = px.bar(
        time_melt,
        x='time_period',
        y='usage_share',
        color='day_type',
        barmode='group',
        labels={
            'usage_share': 'Share of Daily Usage',
            'time_period': 'Time of Day',
            'day_type': 'Day Type'
        },
        title="Internet Usage Time Patterns",
        text_auto=True,
        category_orders={"time_period": time_periods},
        color_discrete_map={
            'Weekday': '#FF9933',  # Saffron
            'Weekend': '#138808'   # Green
        }
    )
    fig.update_layout(height=450, xaxis={'tickangle': -45})
    st.plotly_chart(fig, use_container_width=True)

    # Data Consumption Trends
    st.header("Data Consumption Trends")

    # Calculate average data consumption by purpose
    purpose_data = pd.DataFrame({
        'purpose': ['Entertainment', 'Social Media', 'Education', 'News', 'E-commerce', 'Government Services', 'Banking', 'Healthcare'],
        'data_share': [0.45, 0.25, 0.12, 0.07, 0.05, 0.03, 0.02, 0.01],
        'growth_rate': [15, 10, 25, 5, 30, 40, 35, 50]
    })

    fig = px.scatter(
        purpose_data,
        x='data_share',
        y='growth_rate',
        size='data_share',
        text='purpose',
        labels={
            'data_share': 'Share of Total Data Consumption',
            'growth_rate': 'YoY Growth Rate (%)',
            'purpose': 'Purpose'
        },
        title="Data Consumption by Purpose and Growth Rate"
    )

    fig.update_traces(
        textposition='top center',
        marker=dict(color='#FF9933')
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Speed Requirements
    st.header("Bandwidth Requirements")

    # Create connection speed data
    speed_data = pd.DataFrame({
        'speed_range': ['< 1 Mbps', '1-2 Mbps', '2-5 Mbps', '5-10 Mbps', '10-20 Mbps', '> 20 Mbps'],
        'percentage': [15, 25, 35, 15, 7, 3]
    })

    # Create a bar chart for speed requirements
    fig = px.bar(
        speed_data,
        x='speed_range',
        y='percentage',
        labels={
            'percentage': 'Percentage of Users',
            'speed_range': 'Connection Speed'
        },
        title="Connection Speed Requirements for Rural Users",
        text_auto=True,
        color='percentage',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    # Key insights
    st.header("Key Usage Pattern Insights")

    st.markdown("""
    Analysis of internet usage patterns in rural India reveals:

    1. **Mobile Dominance**: Approximately 75% of rural internet access occurs via mobile devices, with smartphones being the primary access point.

    2. **Evening Peak**: Usage peaks during evening hours (4-8 PM), suggesting most users access the internet after work hours.

    3. **Content Preferences**: Entertainment (video streaming) and social media represent over 70% of data consumption, with education emerging as a growing category.

    4. **Low-Bandwidth Adaptation**: Rural users have developed unique patterns of content consumption that adapt to limited bandwidth, including deferred downloading and shared viewing.

    5. **Video Dominance**: Video content accounts for over 60% of data consumption, regardless of the service category (entertainment, education, or social media).

    6. **Service Diversity**: While popular services dominate overall usage, there is a long tail of specialized applications used by rural communities, particularly in agriculture and local commerce.

    7. **Bandwidth Requirements**: Most rural applications function within 2-5 Mbps range, indicating that consistent moderate speeds may be more valuable than intermittent high speeds.
    """)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Usage Patterns - Rural India Broadband",
        page_icon="📱",
        layout="wide"
    )
    app()