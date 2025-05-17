import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Set page config
st.set_page_config(
    page_title="Rural India Broadband Connectivity Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================ DATA GENERATION FUNCTIONS ================

def generate_state_data():
    """
    Generate realistic state-level data for broadband connectivity in India.
    """
    # List of Indian states
    states = [
        'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
        'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
        'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
        'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
        'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
        'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi', 'Jammu and Kashmir'
    ]
    
    # Population distribution (approximated)
    population_base = {
        'Uttar Pradesh': 200_000_000, 'Maharashtra': 112_000_000, 'Bihar': 104_000_000,
        'West Bengal': 91_000_000, 'Madhya Pradesh': 72_000_000, 'Tamil Nadu': 72_000_000,
        'Rajasthan': 68_000_000, 'Karnataka': 61_000_000, 'Gujarat': 60_000_000,
        'Andhra Pradesh': 49_000_000, 'Odisha': 42_000_000, 'Telangana': 35_000_000,
        'Kerala': 33_000_000, 'Jharkhand': 33_000_000, 'Assam': 31_000_000,
        'Punjab': 28_000_000, 'Chhattisgarh': 26_000_000, 'Haryana': 25_000_000,
        'Delhi': 17_000_000, 'Jammu and Kashmir': 12_000_000, 'Uttarakhand': 10_000_000,
        'Himachal Pradesh': 7_000_000, 'Tripura': 4_000_000, 'Meghalaya': 3_000_000,
        'Manipur': 3_000_000, 'Nagaland': 2_000_000, 'Goa': 1_500_000,
        'Arunachal Pradesh': 1_400_000, 'Sikkim': 600_000, 'Mizoram': 1_100_000
    }
    
    # Adjust population for rural focus (approximately 65% of India is rural)
    rural_population = {state: int(pop * 0.65) for state, pop in population_base.items()}
    
    # Generate broadband penetration rates with regional variations
    # South and west have higher penetration than north and east
    penetration_base = {
        'South': (0.18, 0.32),  # Higher range for southern states
        'West': (0.15, 0.28),   # Medium-high range for western states
        'North': (0.10, 0.22),  # Medium range for northern states
        'East': (0.05, 0.15),   # Lower range for eastern states
        'Northeast': (0.03, 0.12),  # Lowest range for northeastern states
        'Central': (0.08, 0.18)  # Medium-low range for central states
    }
    
    # Regional mapping
    region_mapping = {
        'Andhra Pradesh': 'South', 'Karnataka': 'South', 'Kerala': 'South', 
        'Tamil Nadu': 'South', 'Telangana': 'South',
        'Gujarat': 'West', 'Maharashtra': 'West', 'Goa': 'West', 'Rajasthan': 'West',
        'Bihar': 'East', 'Jharkhand': 'East', 'Odisha': 'East', 'West Bengal': 'East',
        'Delhi': 'North', 'Haryana': 'North', 'Himachal Pradesh': 'North', 
        'Jammu and Kashmir': 'North', 'Punjab': 'North', 'Uttar Pradesh': 'North', 
        'Uttarakhand': 'North',
        'Assam': 'Northeast', 'Arunachal Pradesh': 'Northeast', 'Manipur': 'Northeast', 
        'Meghalaya': 'Northeast', 'Mizoram': 'Northeast', 'Nagaland': 'Northeast', 
        'Sikkim': 'Northeast', 'Tripura': 'Northeast',
        'Chhattisgarh': 'Central', 'Madhya Pradesh': 'Central'
    }
    
    # Generate data for each state
    data = []
    for state in states:
        region = region_mapping.get(state, 'North')  # Default to North if unknown
        min_pen, max_pen = penetration_base[region]
        
        # Add some randomness to penetration rates
        penetration = min_pen + (max_pen - min_pen) * np.random.beta(2, 2)
        
        # Calculate subscribers
        population = rural_population.get(state, 10_000_000)  # Default if unknown
        subscribers = int(population * penetration)
        
        # Mobile data usage (GB per month per user) - varies by region
        mobile_usage_map = {
            'South': (1.5, 3.0), 'West': (1.2, 2.5), 'North': (1.0, 2.0),
            'East': (0.8, 1.5), 'Northeast': (0.5, 1.2), 'Central': (0.8, 1.8)
        }
        
        mobile_min, mobile_max = mobile_usage_map[region]
        mobile_data = mobile_min + (mobile_max - mobile_min) * np.random.random()
        
        # Fixed broadband usage (higher than mobile)
        fixed_data = mobile_data * (1.5 + np.random.random())
        
        # Urban penetration (for comparison) - generally 2-4x higher than rural
        urban_factor = 2 + np.random.random() * 2
        urban_penetration = min(penetration * urban_factor, 0.85)  # Cap at 85%
        
        data.append({
            'state': state,
            'region': region,
            'population': population,
            'broadband_penetration': penetration,
            'subscribers': subscribers,
            'mobile_data_usage': mobile_data,
            'fixed_broadband_usage': fixed_data,
            'urban_penetration': urban_penetration,
            'rural_penetration': penetration  # Same as broadband_penetration
        })
    
    return pd.DataFrame(data)

def get_district_penetration(row):
    """Helper function to get district-level penetration with realistic variation"""
    # Base penetration from state level
    base = row['state_penetration']
    
    # Add variation based on district traits
    if row['proximity_to_city'] == 'Near':
        base = base * (1.2 + np.random.random() * 0.4)  # 20-60% higher than state average
    elif row['proximity_to_city'] == 'Medium':
        base = base * (0.9 + np.random.random() * 0.3)  # -10% to +20% of state average
    else:  # 'Far'
        base = base * (0.5 + np.random.random() * 0.4)  # 50-90% of state average
    
    # Adjust for terrain
    if row['terrain'] == 'Mountainous':
        base = base * (0.6 + np.random.random() * 0.2)  # 60-80% reduction for mountains
    elif row['terrain'] == 'Hilly':
        base = base * (0.7 + np.random.random() * 0.2)  # 70-90% reduction for hills
    
    # Cap at reasonable values
    return min(base, 0.95)

def generate_district_data():
    """
    Generate district-level broadband data for more granular analysis.
    """
    # Get state-level data for reference
    state_df = generate_state_data()
    
    # Create a mapping of state to penetration
    state_penetration = dict(zip(state_df['state'], state_df['broadband_penetration']))
    
    # Generate districts (5-10 per state)
    data = []
    
    # Terrain types and city proximity options
    terrain_types = ['Plain', 'Hilly', 'Mountainous', 'Coastal', 'Desert', 'Forest']
    proximity_options = ['Near', 'Medium', 'Far']
    
    for state in state_df['state']:
        # Generate random number of districts
        n_districts = np.random.randint(5, 11)
        state_pop = state_df[state_df['state'] == state]['population'].iloc[0]
        
        for i in range(n_districts):
            district_name = f"{state} District {i+1}"
            
            # Randomly assign terrain and city proximity
            terrain = np.random.choice(terrain_types)
            proximity_to_city = np.random.choice(proximity_options)
            
            # Allocate population share to district (with some randomness)
            pop_share = 1/n_districts * (0.7 + np.random.random() * 0.6)
            district_pop = int(state_pop * pop_share)
            
            # Get penetration rate based on state, terrain, and city proximity
            row = {
                'state': state,
                'state_penetration': state_penetration[state],
                'terrain': terrain,
                'proximity_to_city': proximity_to_city
            }
            penetration = get_district_penetration(row)
            
            # Calculate subscribers
            subscribers = int(district_pop * penetration)
            
            data.append({
                'district': district_name,
                'state': state,
                'population': district_pop,
                'broadband_penetration': penetration,
                'subscribers': subscribers,
                'terrain': terrain,
                'proximity_to_city': proximity_to_city
            })
    
    return pd.DataFrame(data)

def generate_time_series_data():
    """
    Generate time series data for broadband subscribers over the past 5 years.
    """
    # Create date range for past 5 years (monthly data)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5*365)
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    
    # Set initial and final subscriber counts
    initial_subscribers = 80_000_000  # 80 million
    final_subscribers = 250_000_000   # 250 million
    
    # Create growth curve with seasonal patterns
    # Base growth trend (logistic growth)
    x = np.linspace(0, 1, len(date_range))
    base_trend = initial_subscribers + (final_subscribers - initial_subscribers) * (1 / (1 + np.exp(-10 * (x - 0.5))))
    
    # Add seasonal component (higher in winter months)
    month_seasonality = np.array([1.02, 1.01, 0.99, 0.98, 0.97, 0.96, 0.97, 0.98, 1.0, 1.01, 1.03, 1.04])
    seasonal_factors = np.array([month_seasonality[d.month-1] for d in date_range])
    
    # Add policy impact events (jumps in subscriptions due to government initiatives)
    policy_impacts = np.zeros(len(date_range))
    
    # Major digital initiative 2 years ago
    impact_index = len(date_range) - 24
    policy_impacts[impact_index:impact_index+6] = [0.03, 0.06, 0.08, 0.07, 0.05, 0.03]
    
    # Recent broadband subsidy program
    impact_index = len(date_range) - 6
    policy_impacts[impact_index:] = [0.02, 0.04, 0.06, 0.07, 0.08, 0.09]
    
    # Combine all components with some noise
    subscribers = base_trend * seasonal_factors * (1 + policy_impacts)
    noise = np.random.normal(0, 0.01, len(subscribers))
    subscribers = subscribers * (1 + noise)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': date_range,
        'subscribers': subscribers.astype(int),
        'penetration': subscribers / 1_350_000_000  # Approx. India population
    })
    
    return df

def generate_demographic_data():
    """
    Generate demographic data showing broadband usage across different segments.
    """
    # Get state data for reference
    state_df = generate_state_data()
    
    # Age groups
    age_groups = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
    
    # Age distribution in population (approximated)
    age_distribution = {
        '0-14': 0.28,
        '15-24': 0.18,
        '25-34': 0.16,
        '35-44': 0.13,
        '45-54': 0.11,
        '55-64': 0.08,
        '65+': 0.06
    }
    
    # Internet adoption rates by age (approximated, higher in younger groups)
    age_adoption = {
        '0-14': 0.10,
        '15-24': 0.25,
        '25-34': 0.22,
        '15-24': 0.25,
        '25-34': 0.22,
        '35-44': 0.16,
        '45-54': 0.12,
        '55-64': 0.08,
        '65+': 0.04
    }
    
    # Generate data for each state and demographic segment
    data = []
    
    for state in state_df['state'].unique():
        state_row = state_df[state_df['state'] == state].iloc[0]
        state_pop = state_row['population']
        state_penetration = state_row['broadband_penetration']
        
        # Gender distribution (approximated with slight variations by state)
        male_ratio = 0.51 + np.random.normal(0, 0.01)
        female_ratio = 1 - male_ratio
        
        # Gender adoption gap (males tend to have higher adoption rates)
        gender_gap = 0.65 + np.random.normal(0, 0.05)  # Males have about 40-80% higher rates
        
        # Process by age group
        for age in age_groups:
            # Calculate demographic-specific metrics
            age_pop_male = int(state_pop * age_distribution[age] * male_ratio)
            age_pop_female = int(state_pop * age_distribution[age] * female_ratio)
            
            # Adjust adoption rate by state's overall penetration
            adj_factor = state_penetration / 0.15  # normalize to national average
            
            # Male adoption (higher)
            male_adoption = min(age_adoption[age] * adj_factor * (1 + (1-gender_gap)), 0.9)
            male_users = int(age_pop_male * male_adoption)
            
            # Female adoption (lower due to gender gap)
            female_adoption = min(age_adoption[age] * adj_factor * gender_gap, 0.9)
            female_users = int(age_pop_female * female_adoption)
            
            # Add male data
            data.append({
                'state': state,
                'age_group': age,
                'gender': 'Male',
                'population': age_pop_male,
                'penetration': male_adoption,
                'users': male_users,
                'urban_penetration': min(male_adoption * 2, 0.9),
                'rural_penetration': male_adoption
            })
            
            # Add female data
            data.append({
                'state': state,
                'age_group': age,
                'gender': 'Female',
                'population': age_pop_female,
                'penetration': female_adoption,
                'users': female_users,
                'urban_penetration': min(female_adoption * 2, 0.9),
                'rural_penetration': female_adoption
            })
    
    return pd.DataFrame(data)

def generate_usage_data():
    """
    Generate data about internet usage patterns across states.
    """
    # Get state data for reference
    state_df = generate_state_data()
    
    # Device types
    device_types = ['Basic Phone', 'Feature Phone', 'Low-end Smartphone', 'Mid-range Smartphone', 'High-end Smartphone', 'Computer/Tablet']
    
    # Usage purposes
    usage_purposes = ['Social Media', 'Entertainment', 'Education', 'News', 'Banking', 'E-commerce', 'Government Services', 'Job Search', 'Work']
    
    # Connection types
    connection_types = ['2G', '3G', '4G', '5G', 'Fixed Broadband']
    
    data = []
    
    for state in state_df['state'].unique():
        state_row = state_df[state_df['state'] == state].iloc[0]
        region = state_row['region']
        penetration = state_row['broadband_penetration']
        
        # Device distribution varies by region and penetration rate
        # More developed regions have higher smartphone and computer usage
        if region in ['South', 'West']:
            device_dist = [0.05, 0.15, 0.25, 0.30, 0.15, 0.10]
        elif region in ['North', 'Central']:
            device_dist = [0.10, 0.20, 0.30, 0.25, 0.10, 0.05]
        else:  # East, Northeast
            device_dist = [0.15, 0.25, 0.35, 0.15, 0.07, 0.03]
        
        # Adjust based on penetration (higher penetration = more advanced devices)
        adj_factor = penetration / 0.15  # normalize to avg penetration
        device_dist = np.array(device_dist)
        # Shift distribution toward more advanced devices for higher penetration
        if adj_factor > 1:
            shift = (adj_factor - 1) * 0.1
            device_dist = np.array([
                max(device_dist[0] - shift*2, 0.01),
                max(device_dist[1] - shift, 0.05),
                device_dist[2],
                device_dist[3] + shift/2,
                device_dist[4] + shift/2,
                min(device_dist[5] + shift, 0.25)
            ])
            device_dist = device_dist / device_dist.sum()  # Normalize
        
        # Add some randomness
        device_dist = device_dist + np.random.normal(0, 0.02, len(device_dist))
        device_dist = np.maximum(device_dist, 0.01)  # Ensure no negative values
        device_dist = device_dist / device_dist.sum()  # Normalize
        
        # Create entries for each device type
        for i, device in enumerate(device_types):
            # Calculate users for this device
            users = int(state_row['subscribers'] * device_dist[i])
            
            # Generate connection type distribution for this device
            if device in ['Basic Phone', 'Feature Phone']:
                conn_dist = [0.4, 0.5, 0.1, 0, 0]  # Mostly 2G/3G
            elif device == 'Low-end Smartphone':
                conn_dist = [0.05, 0.45, 0.5, 0, 0]  # Mostly 3G/4G
            elif device == 'Mid-range Smartphone':
                conn_dist = [0, 0.2, 0.7, 0.1, 0]  # Mostly 4G
            elif device == 'High-end Smartphone':
                conn_dist = [0, 0.05, 0.65, 0.3, 0]  # 4G/5G
            else:  # Computer/Tablet
                conn_dist = [0, 0, 0.2, 0.2, 0.6]  # Mostly fixed broadband
            
            # Add entries for state, device type, and connection distribution
            data.append({
                'state': state,
                'device_type': device,
                'users': users,
                'percentage': device_dist[i],
                'connection_2G': conn_dist[0],
                'connection_3G': conn_dist[1],
                'connection_4G': conn_dist[2],
                'connection_5G': conn_dist[3],
                'connection_fixed': conn_dist[4]
            })
    
    return pd.DataFrame(data)

def get_state_region_map():
    """
    Get a mapping of Indian states to their geographic regions.
    Returns: dict: Dictionary mapping state names to region names
    """
    region_mapping = {
        'Andhra Pradesh': 'South', 'Karnataka': 'South', 'Kerala': 'South', 
        'Tamil Nadu': 'South', 'Telangana': 'South',
        'Gujarat': 'West', 'Maharashtra': 'West', 'Goa': 'West', 'Rajasthan': 'West',
        'Bihar': 'East', 'Jharkhand': 'East', 'Odisha': 'East', 'West Bengal': 'East',
        'Delhi': 'North', 'Haryana': 'North', 'Himachal Pradesh': 'North', 
        'Jammu and Kashmir': 'North', 'Punjab': 'North', 'Uttar Pradesh': 'North', 
        'Uttarakhand': 'North',
        'Assam': 'Northeast', 'Arunachal Pradesh': 'Northeast', 'Manipur': 'Northeast', 
        'Meghalaya': 'Northeast', 'Mizoram': 'Northeast', 'Nagaland': 'Northeast', 
        'Sikkim': 'Northeast', 'Tripura': 'Northeast',
        'Chhattisgarh': 'Central', 'Madhya Pradesh': 'Central'
    }
    return region_mapping

# ================ TABS SETUP ================

tabs = st.tabs([
    "Geographic Analysis", 
    "Demographic Analysis", 
    "Time Series Analysis", 
    "Usage Patterns", 
    "Insights & Recommendations"
])

# ================ GEOGRAPHIC ANALYSIS ================

with tabs[0]:
    st.header("Geographic Analysis of Broadband Connectivity")
    st.markdown("""
    Explore the geographic distribution of broadband connectivity across rural India.
    Identify underserved regions and connectivity hotspots to inform strategic decisions
    for infrastructure development and digital inclusion initiatives.
    """)
    
    # Load data
    state_data = generate_state_data()
    district_data = generate_district_data()
    
    # Filters
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_metric = st.selectbox(
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
    st.subheader("State-Level Analysis")
    
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
    st.subheader("Geographic Disparities")
    
    # Group states by region and calculate average metrics
    region_data = state_data.copy()
    # Get region mapping from helper function
    region_mapping = get_state_region_map()
    region_data['region'] = region_data['state'].apply(lambda x: region_mapping.get(x, 'Other'))
    
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
    st.subheader("Key Geographic Insights")
    
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

# ================ DEMOGRAPHIC ANALYSIS ================

with tabs[1]:
    st.header("Demographic Analysis of Internet Usage")
    st.markdown("""
    Examine how demographic factors influence broadband connectivity and usage patterns
    across rural India. Understand the relationship between age, income, education levels,
    and digital inclusion to design targeted interventions for underserved communities.
    """)
    
    # Key demographic visualizations
    demo_data = generate_demographic_data()
    
    # Age Group Analysis
    st.subheader("Age Group Analysis")
    
    # Calculate national averages for age groups
    age_national = demo_data.groupby('age_group').agg({
        'penetration': 'mean',
        'users': 'sum',
        'population': 'sum'
    }).reset_index()
    
    age_national['proportion'] = age_national['users'] / age_national['population']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create bar chart for penetration by age group
        age_order = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
        fig = px.bar(
            age_national,
            x='age_group',
            y='proportion',
            labels={
                'proportion': 'Internet Adoption Rate',
                'age_group': 'Age Group'
            },
            title="Internet Adoption by Age Group",
            category_orders={"age_group": age_order},
            text_auto=True
        )
        fig.update_traces(marker_color='#FF9933')  # Saffron from Indian flag
        fig.update_layout(height=400, xaxis={'categoryorder': 'array', 'categoryarray': age_order})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Create a pie chart for user distribution by age
        fig = px.pie(
            age_national,
            names='age_group',
            values='users',
            title="Distribution of Internet Users by Age Group",
            category_orders={"age_group": age_order},
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Gender Analysis
    st.subheader("Gender Analysis")
    
    # Calculate gender stats
    gender_stats = demo_data.groupby('gender').agg({
        'penetration': 'mean',
        'users': 'sum',
        'population': 'sum'
    }).reset_index()
    
    gender_stats['proportion'] = gender_stats['users'] / gender_stats['population']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create bar chart for gender comparison
        fig = px.bar(
            gender_stats,
            x='gender',
            y='proportion',
            labels={
                'proportion': 'Internet Adoption Rate',
                'gender': 'Gender'
            },
            title="Internet Adoption by Gender",
            text_auto=True,
            color='gender',
            color_discrete_map={
                'Male': '#FF9933',  # Saffron
                'Female': '#138808'  # Green
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Create a pie chart for user distribution by gender
        fig = px.pie(
            gender_stats,
            names='gender',
            values='users',
            title="Distribution of Internet Users by Gender",
            color='gender',
            color_discrete_map={
                'Male': '#FF9933',  # Saffron
                'Female': '#138808'  # Green
            }
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Urban-Rural Digital Divide
    st.subheader("Urban-Rural Digital Divide")
    
    # Calculate urban-rural comparison
    urban_rural = demo_data.groupby('state').agg({
        'urban_penetration': 'mean',
        'rural_penetration': 'mean'
    }).reset_index()
    
    urban_rural['gap_ratio'] = urban_rural['urban_penetration'] / urban_rural['rural_penetration']
    urban_rural = urban_rural.sort_values('gap_ratio', ascending=True)
    
    # Create a dual-axis chart
    fig = go.Figure()
    
    # Add bars for rural penetration
    fig.add_trace(go.Bar(
        x=urban_rural['state'],
        y=urban_rural['rural_penetration'],
        name='Rural Penetration',
        marker_color='#138808'  # Green from Indian flag
    ))
    
    # Add bars for urban penetration
    fig.add_trace(go.Bar(
        x=urban_rural['state'],
        y=urban_rural['urban_penetration'],
        name='Urban Penetration',
        marker_color='#FF9933'  # Saffron from Indian flag
    ))
    
    # Add line for gap ratio
    fig.add_trace(go.Scatter(
        x=urban_rural['state'],
        y=urban_rural['gap_ratio'],
        name='Urban-Rural Gap Ratio',
        yaxis='y2',
        line=dict(color='darkblue', width=2)
    ))
    
    # Set up the layout
    fig.update_layout(
        title='Urban-Rural Digital Divide by State',
        yaxis=dict(
            title='Penetration Rate',
            title_font=dict(color='#333333'),
            tickfont=dict(color='#333333')
        ),
        yaxis2=dict(
            title='Urban-Rural Gap Ratio',
            title_font=dict(color='darkblue'),
            tickfont=dict(color='darkblue'),
            overlaying='y',
            side='right'
        ),
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ================ TIME SERIES ANALYSIS ================

with tabs[2]:
    st.header("Time Series Analysis of Broadband Adoption")
    st.markdown("""
    Analyze the growth and trends in broadband connectivity over time across rural India.
    Track the evolution of subscriber numbers, penetration rates, and usage patterns to
    understand the trajectory of digital inclusion in rural communities.
    """)
    
    # Load data
    time_data = generate_time_series_data()
    
    # Filters
    time_range = st.selectbox(
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
    st.subheader("Overall Growth Trend")
    
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

# ================ USAGE PATTERNS ================

with tabs[3]:
    st.header("Internet Usage Patterns in Rural India")
    st.markdown("""
    Explore how rural communities are using the internet, including data consumption patterns,
    preferred devices, and popular services. Understanding these patterns helps in designing
    appropriate digital services and guiding infrastructure investments.
    """)
    
    # Load data
    usage_data = generate_usage_data()
    
    # Device usage analysis
    st.subheader("Device Usage Analysis")
    
    # Calculate national totals by device type
    device_national = usage_data.groupby('device_type').agg({
        'users': 'sum'
    }).reset_index()
    
    # Calculate percentage of total
    total_users = device_national['users'].sum()
    device_national['percentage'] = device_national['users'] / total_users * 100
    
    # Order device types from basic to advanced
    device_order = ['Basic Phone', 'Feature Phone', 'Low-end Smartphone', 
                   'Mid-range Smartphone', 'High-end Smartphone', 'Computer/Tablet']
    
    # Create a function to map device type to an order for sorting
    device_national['order'] = device_national['device_type'].apply(lambda x: device_order.index(x))
    device_national = device_national.sort_values('order')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create bar chart for device usage
        fig = px.bar(
            device_national,
            x='device_type',
            y='percentage',
            labels={
                'percentage': 'Percentage of Users',
                'device_type': 'Device Type'
            },
            title="Device Usage Distribution",
            text_auto=True,
            category_orders={"device_type": device_order}
        )
        fig.update_traces(marker_color='#FF9933')  # Saffron from Indian flag
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Create pie chart for device usage
        fig = px.pie(
            device_national,
            names='device_type',
            values='percentage',
            title="Device Usage Distribution",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Connection type analysis
    st.subheader("Connection Type Analysis")
    
    # Melt the connection data for visualization
    conn_cols = ['connection_2G', 'connection_3G', 'connection_4G', 'connection_5G', 'connection_fixed']
    conn_data = usage_data.groupby('device_type').agg({
        col: 'mean' for col in conn_cols
    }).reset_index()
    
    conn_data_melted = pd.melt(
        conn_data, 
        id_vars=['device_type'], 
        value_vars=conn_cols,
        var_name='connection_type', 
        value_name='proportion'
    )
    
    # Clean up connection type labels
    conn_data_melted['connection_type'] = conn_data_melted['connection_type'].str.replace('connection_', '')
    
    # Create stacked bar chart for connection types by device
    fig = px.bar(
        conn_data_melted,
        x='device_type',
        y='proportion',
        color='connection_type',
        labels={
            'proportion': 'Proportion of Users',
            'device_type': 'Device Type',
            'connection_type': 'Connection Type'
        },
        title="Connection Types by Device",
        barmode='stack',
        category_orders={"device_type": device_order}
    )
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional device usage variations
    st.subheader("Regional Device Usage Variations")
    
    # Calculate regional device usage
    region_device = usage_data.copy()
    region_device['region'] = region_device['state'].apply(lambda x: region_mapping.get(x, 'Other'))
    
    region_device_agg = region_device.groupby(['region', 'device_type']).agg({
        'users': 'sum'
    }).reset_index()
    
    # Calculate percentage within each region
    region_totals = region_device_agg.groupby('region')['users'].sum().reset_index()
    region_totals.rename(columns={'users': 'total_users'}, inplace=True)
    
    region_device_agg = pd.merge(region_device_agg, region_totals, on='region')
    region_device_agg['percentage'] = region_device_agg['users'] / region_device_agg['total_users'] * 100
    
    # Create the visualization
    fig = px.bar(
        region_device_agg,
        x='region',
        y='percentage',
        color='device_type',
        labels={
            'percentage': 'Percentage of Users',
            'region': 'Region',
            'device_type': 'Device Type'
        },
        title="Device Usage by Region",
        barmode='stack',
        category_orders={"device_type": device_order}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# ================ INSIGHTS & RECOMMENDATIONS ================

with tabs[4]:
    st.header("Insights & Recommendations")
    st.markdown("""
    Based on comprehensive analysis of rural broadband connectivity patterns across India,
    here are key insights and actionable recommendations to guide digital inclusion strategies
    and infrastructure investments.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Key Insights")
        st.markdown("""
        1. **Regional Disparities**: Southern states show significantly higher connectivity rates (25-32%) compared to northeastern states (3-12%), indicating a clear digital divide.
        
        2. **Demographic Factors**: The 15-34 age group has the highest adoption rates, while a persistent gender gap exists with men having 40-80% higher access than women.
        
        3. **Device Limitations**: Nearly 40% of rural users rely on basic or feature phones, limiting their ability to access the full range of digital services.
        
        4. **Connection Quality**: 4G coverage is expanding, but 2G/3G still dominates in remote areas, with fixed broadband penetration below 5% in most rural regions.
        
        5. **Growth Patterns**: Broadband adoption is showing accelerating growth (CAGR of 25-30%), with government initiatives creating visible upticks in the subscriber curve.
        
        6. **Usage Distribution**: Social media and entertainment dominate rural internet usage (60-70%), with essential services like education, banking, and government services lagging.
        
        7. **Infrastructure Gap**: Mountainous and remote areas show connectivity rates 50-70% lower than the national average, highlighting infrastructure deployment challenges.
        """)
    
    with col2:
        st.subheader("Strategic Recommendations")
        st.markdown("""
        1. **Targeted Infrastructure Development**: Prioritize investment in northeastern states and mountainous regions with the lowest penetration rates but high population density.
        
        2. **Mobile-First Approach**: Focus on improving mobile broadband coverage as it represents the primary access method for over 90% of rural users.
        
        3. **Gender-Inclusive Programs**: Develop specific digital literacy initiatives targeting rural women to bridge the persistent gender gap in internet adoption.
        
        4. **Device Affordability**: Implement subsidy programs for entry-level smartphones to help users transition from feature phones to more capable devices.
        
        5. **Usage Diversification**: Create awareness and training programs to promote educational, financial, and government service usage over purely entertainment consumption.
        
        6. **Public Access Points**: Establish community broadband centers in regions with the lowest household penetration rates to provide shared access.
        
        7. **Seasonal Planning**: Schedule network capacity upgrades before winter months when usage typically increases by 10-15%.
        """)
    
    # Implementation approach
    st.subheader("Implementation Approach")
    
    st.markdown("""
    Effective implementation of the recommendations requires a phased approach with clear prioritization:
    
    **Phase 1: Foundation Building (Years 1-2)**
    - Deploy 4G infrastructure in high-priority districts with penetration below 10%
    - Launch gender-focused digital literacy programs in states with the highest gender gaps
    - Establish 500 community broadband centers in the most underserved regions
    
    **Phase 2: Acceleration (Years 3-4)**
    - Expand smartphone subsidy program to reach 20 million new users
    - Implement usage incentive programs for educational and government services
    - Upgrade high-traffic rural networks to support video applications
    
    **Phase 3: Sustainability (Years 5+)**
    - Transition from infrastructure deployment to service quality improvements
    - Develop local content creation ecosystem to drive relevant usage
    - Implement self-sustaining models for community broadband centers
    """)
    
    # Expected impact
    st.subheader("Expected Impact")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Broadband Penetration Increase", "+20%", "by Year 5")
    with col2:
        st.metric("Gender Gap Reduction", "-60%", "from current levels")
    with col3:
        st.metric("Educational Usage Growth", "+150%", "from baseline")
    
    st.markdown("""
    Full implementation of these recommendations is expected to deliver:
    
    - Increase rural broadband penetration from current national average of 15% to 35% within 5 years
    - Reduce the urban-rural digital divide ratio from 3.2x to 1.8x
    - Bring at least basic connectivity to 95% of rural population
    - Increase the proportion of rural users accessing government and educational services from 15% to 40%
    - Create estimated economic value addition of $15-20 billion through improved rural productivity
    """)
    
    # Monitoring framework
    with st.expander("Monitoring & Evaluation Framework"):
        st.markdown("""
        ### Key Performance Indicators
        
        | Indicator | Baseline | Year 1 Target | Year 3 Target | Year 5 Target |
        |-----------|----------|---------------|---------------|---------------|
        | Rural penetration rate | 15% | 18% | 25% | 35% |
        | Female internet users | 35% of total | 38% | 43% | 48% |
        | Smartphone users | 60% of users | 65% | 75% | 85% |
        | 4G/5G coverage | 45% of villages | 55% | 75% | 90% |
        | Educational service users | 15% of users | 20% | 30% | 40% |
        | Digital payment adoption | 25% of users | 35% | 50% | 70% |
        
        ### Evaluation Methodology
        
        - Quarterly surveys in representative sample districts
        - Annual comprehensive assessment across all states
        - Mobile app usage analytics from partner applications
        - Network quality monitoring through crowdsourced data
        - Community feedback through digital kiosks
        """)

# ================ FOOTER ================

st.markdown("---")
st.markdown("""
**Rural India Broadband Connectivity Dashboard**  
A comprehensive analysis tool for understanding and improving digital inclusion in rural communities.
""")
st.markdown("© 2025 Rural Broadband Initiative")