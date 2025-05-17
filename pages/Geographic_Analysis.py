import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_state_data():
    """
    Generate realistic state-level data for broadband connectivity in India.
    
    Returns:
        DataFrame: State-level broadband connectivity data
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
            'urban_penetration': urban_penetration
        })
    
    return pd.DataFrame(data)

def get_district_penetration(row):
    """Helper function to get district-level penetration with realistic variation"""
    state_pen = row['broadband_penetration']
    region = row['region']
    
    # Variation depends on region - more developed regions have less variation
    variation_factor = {
        'South': 0.3, 'West': 0.4, 'North': 0.5,
        'East': 0.6, 'Northeast': 0.7, 'Central': 0.6
    }.get(region, 0.5)
    
    # Generate penetration with beta distribution for realistic skew
    alpha = 2
    beta = 2
    variation = np.random.beta(alpha, beta) * variation_factor - variation_factor/2
    pen = state_pen * (1 + variation)
    
    # Ensure reasonable bounds
    return max(0.01, min(pen, 0.9))

def generate_district_data():
    """
    Generate district-level broadband data for more granular analysis.
    
    Returns:
        DataFrame: District-level broadband connectivity data
    """
    # Get state data first
    state_data = generate_state_data()
    
    # Define number of districts per state (approximated)
    districts_per_state = {
        'Uttar Pradesh': 75, 'Maharashtra': 36, 'Bihar': 38,
        'West Bengal': 23, 'Madhya Pradesh': 52, 'Tamil Nadu': 38,
        'Rajasthan': 33, 'Karnataka': 31, 'Gujarat': 33,
        'Andhra Pradesh': 13, 'Odisha': 30, 'Telangana': 33,
        'Kerala': 14, 'Jharkhand': 24, 'Assam': 33,
        'Punjab': 23, 'Chhattisgarh': 28, 'Haryana': 22,
        'Delhi': 11, 'Jammu and Kashmir': 20, 'Uttarakhand': 13,
        'Himachal Pradesh': 12, 'Tripura': 8, 'Meghalaya': 11,
        'Manipur': 16, 'Nagaland': 12, 'Goa': 2,
        'Arunachal Pradesh': 25, 'Sikkim': 4, 'Mizoram': 11
    }
    
    # Create district-level data
    districts = []
    
    for _, state_row in state_data.iterrows():
        state = state_row['state']
        state_pop = state_row['population']
        state_penetration = state_row['broadband_penetration']
        num_districts = districts_per_state.get(state, 15)  # Default to 15 if unknown
        
        # Distribute population among districts (with variation)
        district_pops = np.random.dirichlet(np.ones(num_districts)) * state_pop
        
        for i in range(num_districts):
            district_name = f"{state} District {i+1}"
            
            # District penetration varies around state average
            district_penetration = get_district_penetration(state_row)
            
            # Calculate subscribers
            district_pop = int(district_pops[i])
            district_subs = int(district_pop * district_penetration)
            
            # Geographical factors (random for simulation)
            distance_to_city = np.random.randint(5, 150)  # km
            elevation = np.random.randint(0, 2000)  # meters
            
            # Infrastructure metrics
            tower_density = np.random.uniform(0.1, 1.5)  # per sq km
            fiber_availability = np.random.choice([0, 1], p=[0.7, 0.3])  # binary
            
            districts.append({
                'state': state,
                'district': district_name,
                'population': district_pop,
                'penetration': district_penetration,
                'subscribers': district_subs,
                'distance_to_major_city': distance_to_city,
                'elevation': elevation,
                'tower_density': tower_density,
                'fiber_availability': fiber_availability
            })
    
    return pd.DataFrame(districts)

def generate_time_series_data():
    """
    Generate time series data for broadband subscribers over the past 5 years.
    
    Returns:
        DataFrame: Monthly broadband subscriber data
    """
    # Generate monthly data for 5 years (60 months)
    end_date = datetime.now().replace(day=1) - timedelta(days=1)  # End of last month
    start_date = end_date - timedelta(days=5*365)  # ~5 years ago
    
    # Create date range (monthly)
    date_range = pd.date_range(start=start_date, end=end_date, freq='ME')
    
    # Initial subscriber count (in millions)
    initial_subscribers = 45.0  # 45 million initial rural broadband users
    
    # Generate subscriber growth with seasonal patterns and overall upward trend
    subscribers = []
    current = initial_subscribers
    
    # Growth parameters
    yearly_growth = 0.18  # 18% year-over-year growth
    monthly_growth = (1 + yearly_growth) ** (1/12) - 1  # Convert to monthly growth rate
    
    for date in date_range:
        # Add seasonal pattern (higher in winter months, lower in monsoon)
        month = date.month
        if month in [11, 12, 1, 2]:  # Winter months
            seasonal_factor = 1.03  # Higher usage
        elif month in [6, 7, 8, 9]:  # Monsoon months
            seasonal_factor = 0.98  # Lower growth
        else:
            seasonal_factor = 1.0  # Normal growth
        
        # Add some random noise
        noise = np.random.normal(1, 0.01)  # 1% random variation
        
        # Calculate new subscriber count
        current = current * (1 + monthly_growth) * seasonal_factor * noise
        subscribers.append(current)
    
    # Create DataFrame
    df = pd.DataFrame({
        'date': date_range,
        'subscribers': [s * 1_000_000 for s in subscribers]  # Convert to absolute numbers
    })
    
    # Add data usage metrics
    df['mobile_data'] = np.linspace(0.5, 2.2, len(df)) * (1 + 0.05 * np.random.randn(len(df)))
    df['fixed_data'] = np.linspace(1.0, 5.5, len(df)) * (1 + 0.05 * np.random.randn(len(df)))
    
    # Add categorical columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    
    return df

def generate_state_time_series():
    """
    Generate time series data for each state's broadband penetration.
    
    Returns:
        DataFrame: State-level broadband penetration over time
    """
    # Get current state data
    state_data = generate_state_data()
    
    # Generate monthly data for 3 years (36 months)
    end_date = datetime.now().replace(day=1) - timedelta(days=1)  # End of last month
    start_date = end_date - timedelta(days=3*365)  # ~3 years ago
    
    # Create date range (monthly)
    date_range = pd.date_range(start=start_date, end=end_date, freq='ME')
    
    # Create time series data for each state
    state_time_series = []
    
    for _, state_row in state_data.iterrows():
        state = state_row['state']
        region = state_row['region']
        current_penetration = state_row['broadband_penetration']
        
        # Calculate starting penetration (lower than current)
        # Growth rates vary by region
        growth_factors = {
            'South': 0.45, 'West': 0.50, 'North': 0.55,
            'East': 0.60, 'Northeast': 0.65, 'Central': 0.60
        }
        growth_factor = growth_factors.get(region, 0.55)
        starting_penetration = current_penetration * (1 - growth_factor)
        
        # Generate monthly data with appropriate growth trend
        for i, date in enumerate(date_range):
            # Calculate penetration for this date
            progress = i / (len(date_range) - 1)  # 0 to 1 scale
            
            # Non-linear growth (faster recent growth)
            growth_curve = progress ** 0.8
            penetration = starting_penetration + (current_penetration - starting_penetration) * growth_curve
            
            # Add seasonal variation
            month = date.month
            if month in [11, 12, 1, 2]:  # Winter months
                seasonal_factor = 1.01  # Higher usage
            elif month in [6, 7, 8, 9]:  # Monsoon months
                seasonal_factor = 0.99  # Lower usage
            else:
                seasonal_factor = 1.0  # Normal usage
                
            penetration = penetration * seasonal_factor
            
            # Add some random noise
            noise = np.random.normal(1, 0.005)  # 0.5% random variation
            penetration = penetration * noise
            
            state_time_series.append({
                'state': state,
                'region': region,
                'date': date,
                'penetration': penetration
            })
    
    return pd.DataFrame(state_time_series)

def generate_demographic_data():
    """
    Generate demographic data showing broadband usage across different segments.
    
    Returns:
        DataFrame: Demographic breakdown of broadband usage
    """
    # Get state data
    states = generate_state_data()
    
    # Age groups
    age_groups = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
    
    # Age distribution in India (approximated)
    age_distribution = {
        '0-14': 0.27, '15-24': 0.18, '25-34': 0.17, '35-44': 0.14,
        '45-54': 0.11, '55-64': 0.08, '65+': 0.05
    }
    
    # Internet adoption rate by age (approximated)
    adoption_by_age = {
        '0-14': 0.2, '15-24': 0.65, '25-34': 0.70, '35-44': 0.45,
        '45-54': 0.30, '55-64': 0.20, '65+': 0.10
    }
    
    # Gender distribution
    genders = ['Male', 'Female']
    
    # Generate demographic breakdown for each state
    demographic_data = []
    
    for _, state_row in states.iterrows():
        state = state_row['state']
        state_pop = state_row['population']
        region = state_row['region']
        overall_penetration = state_row['broadband_penetration']
        
        # Regional factors affect gender balance
        gender_ratios = {
            'South': (0.53, 0.47), 'West': (0.56, 0.44), 'North': (0.62, 0.38),
            'East': (0.65, 0.35), 'Northeast': (0.60, 0.40), 'Central': (0.64, 0.36)
        }
        
        male_ratio, female_ratio = gender_ratios.get(region, (0.60, 0.40))
        
        # Generate data for each age group and gender
        for age_group in age_groups:
            age_pop_pct = age_distribution[age_group]
            base_adoption = adoption_by_age[age_group]
            
            # Regional influence on adoption rates
            region_factor = {
                'South': 1.2, 'West': 1.1, 'North': 1.0,
                'East': 0.9, 'Northeast': 0.8, 'Central': 0.9
            }.get(region, 1.0)
            
            # Calculate for each gender
            for gender in genders:
                gender_factor = 1.1 if gender == 'Male' else 0.9  # Male adoption slightly higher
                
                # Calculate population and penetration with some random variation
                gender_ratio = male_ratio if gender == 'Male' else female_ratio
                population = int(state_pop * age_pop_pct * gender_ratio)
                
                # Calculate penetration rate 
                penetration = base_adoption * region_factor * gender_factor
                # Scale to align with overall state penetration
                penetration = penetration * (overall_penetration / 0.35) * np.random.uniform(0.9, 1.1)
                penetration = min(max(penetration, 0.01), 0.95)  # Keep within reasonable bounds
                
                users = int(population * penetration)
                
                demographic_data.append({
                    'state': state,
                    'region': region,
                    'age_group': age_group,
                    'gender': gender,
                    'population': population,
                    'penetration': penetration,
                    'users': users,
                    'urban_penetration': penetration * np.random.uniform(1.4, 2.2),
                    'rural_penetration': penetration
                })
    
    return pd.DataFrame(demographic_data)

def generate_income_education_data():
    """
    Generate data showing the relationship between income, education, and internet adoption.
    
    Returns:
        DataFrame: Income and education related broadband usage data
    """
    # Get state data
    states = generate_state_data()
    
    # Income groups
    income_groups = ['Low', 'Lower-Middle', 'Middle', 'Upper-Middle', 'High']
    
    # Income distribution (approximated for rural India)
    income_distribution = {
        'Low': 0.30, 'Lower-Middle': 0.35, 'Middle': 0.25,
        'Upper-Middle': 0.08, 'High': 0.02
    }
    
    # Base adoption rates by income
    income_adoption = {
        'Low': 0.15, 'Lower-Middle': 0.25, 'Middle': 0.45,
        'Upper-Middle': 0.65, 'High': 0.85
    }
    
    # Education levels
    education_levels = ['Illiterate', 'Primary', 'Secondary', 'Higher Secondary', 'Graduate and Above']
    
    # Education distribution (approximated for rural India)
    education_distribution = {
        'Illiterate': 0.35, 'Primary': 0.30, 'Secondary': 0.20,
        'Higher Secondary': 0.10, 'Graduate and Above': 0.05
    }
    
    # Base adoption rates by education
    education_adoption = {
        'Illiterate': 0.1, 'Primary': 0.2, 'Secondary': 0.4,
        'Higher Secondary': 0.6, 'Graduate and Above': 0.8
    }
    
    # Generate data
    income_education_data = []
    
    for _, state_row in states.iterrows():
        state = state_row['state']
        state_pop = state_row['population']
        region = state_row['region']
        overall_penetration = state_row['broadband_penetration']
        
        # Regional influence on distribution
        region_factor = {
            'South': 1.2, 'West': 1.1, 'North': 1.0,
            'East': 0.9, 'Northeast': 0.85, 'Central': 0.9
        }.get(region, 1.0)
        
        # Generate data for each income group and education level
        for income_group in income_groups:
            for education_level in education_levels:
                # Calculate joint probability (with some correlation)
                # Higher income tends to correlate with higher education
                income_idx = income_groups.index(income_group)
                education_idx = education_levels.index(education_level)
                
                # Simple correlation model: concentration around the diagonal
                diff = abs(income_idx / len(income_groups) - education_idx / len(education_levels))
                correlation_factor = np.exp(-diff * 3)  # Favor combinations close to diagonal
                
                # Calculate population in this segment
                income_pct = income_distribution[income_group]
                education_pct = education_distribution[education_level]
                joint_pct = income_pct * education_pct * correlation_factor * 5
                population = int(state_pop * joint_pct)
                
                # Calculate penetration
                income_factor = income_adoption[income_group]
                education_factor = education_adoption[education_level]
                
                # Combine income and education factors (education has stronger influence)
                penetration = (income_factor * 0.4 + education_factor * 0.6) * region_factor
                # Scale to match overall state penetration
                penetration = penetration * (overall_penetration / 0.35) * np.random.uniform(0.9, 1.1)
                penetration = min(max(penetration, 0.01), 0.95)  # Keep within reasonable bounds
                
                users = int(population * penetration)
                
                income_education_data.append({
                    'state': state,
                    'region': region,
                    'income_group': income_group,
                    'education_level': education_level,
                    'population': population,
                    'penetration': penetration,
                    'users': users
                })
    
    return pd.DataFrame(income_education_data)

def generate_usage_data():
    """
    Generate data about internet usage patterns across states.
    
    Returns:
        DataFrame: Internet usage patterns data
    """
    # Get state data
    states = generate_state_data()
    
    # Device usage patterns (as percentages)
    # Will vary by region and state
    usage_data = []
    
    for _, state_row in states.iterrows():
        state = state_row['state']
        region = state_row['region']
        penetration = state_row['broadband_penetration']
        mobile_usage = state_row['mobile_data_usage']
        fixed_usage = state_row['fixed_broadband_usage']
        
        # Device usage varies by region
        # Base percentages - will be adjusted by region
        base_device_usage = {
            'smartphone_pct': 0.70,
            'feature_phone_pct': 0.15,
            'desktop_pct': 0.10,
            'tablet_pct': 0.05
        }
        
        # Regional adjustments
        if region == 'South' or region == 'West':
            # More smartphones, fewer feature phones
            smartphone_adj = 0.10
            feature_phone_adj = -0.08
            desktop_adj = 0.00
            tablet_adj = -0.02
        elif region == 'North':
            # Balanced
            smartphone_adj = 0.00
            feature_phone_adj = 0.00
            desktop_adj = 0.00
            tablet_adj = 0.00
        elif region == 'East' or region == 'Central':
            # More feature phones, fewer smartphones
            smartphone_adj = -0.10
            feature_phone_adj = 0.15
            desktop_adj = -0.03
            tablet_adj = -0.02
        else:  # Northeast
            # More feature phones, much fewer desktops/tablets
            smartphone_adj = -0.05
            feature_phone_adj = 0.10
            desktop_adj = -0.04
            tablet_adj = -0.01
            
        # Apply adjustments
        device_usage = {
            'smartphone_pct': base_device_usage['smartphone_pct'] + smartphone_adj,
            'feature_phone_pct': base_device_usage['feature_phone_pct'] + feature_phone_adj,
            'desktop_pct': base_device_usage['desktop_pct'] + desktop_adj,
            'tablet_pct': base_device_usage['tablet_pct'] + tablet_adj
        }
        
        # Normalize to ensure percentages sum to 1
        total = sum(device_usage.values())
        device_usage = {k: v/total for k, v in device_usage.items()}
        
        # Connection types - mobile vs fixed broadband
        mobile_share = np.random.uniform(0.7, 0.9)  # 70-90% mobile
        fixed_share = 1 - mobile_share
        
        # Total subscribers
        total_subscribers = state_row['subscribers']
        
        usage_data.append({
            'state': state,
            'region': region,
            'total_subscribers': total_subscribers,
            'mobile_data': mobile_usage,
            'fixed_data': fixed_usage,
            'mobile_share': mobile_share,
            'fixed_share': fixed_share,
            'smartphone_pct': device_usage['smartphone_pct'],
            'feature_phone_pct': device_usage['feature_phone_pct'],
            'desktop_pct': device_usage['desktop_pct'],
            'tablet_pct': device_usage['tablet_pct']
        })
    
    return pd.DataFrame(usage_data)

def generate_service_usage_data():
    """
    Generate data about which online services are most used in rural areas.
    
    Returns:
        DataFrame: Service usage data
    """
    # Get state data
    states = generate_state_data()
    
    # Define common online services
    services = [
        'Social Media', 'Video Streaming', 'Communication', 'News', 
        'Education', 'Gaming', 'Banking', 'Government Services', 
        'E-commerce', 'Healthcare', 'Agriculture Apps'
    ]
    
    # Generate usage data for each state and service
    service_data = []
    
    for _, state_row in states.iterrows():
        state = state_row['state']
        region = state_row['region']
        
        # Base usage percentages (will be adjusted by region)
        base_usage = {
            'Social Media': 75,
            'Video Streaming': 65,
            'Communication': 80,
            'News': 45,
            'Education': 30,
            'Gaming': 25,
            'Banking': 20,
            'Government Services': 15,
            'E-commerce': 18,
            'Healthcare': 10,
            'Agriculture Apps': 12
        }
        
        # Regional adjustments
        regional_factors = {
            'South': {
                'Education': 1.2, 'Banking': 1.3, 'E-commerce': 1.2,
                'Government Services': 1.1, 'Healthcare': 1.2
            },
            'West': {
                'E-commerce': 1.3, 'Banking': 1.2, 'Social Media': 1.1,
                'Video Streaming': 1.1, 'Gaming': 1.2
            },
            'North': {
                'Agriculture Apps': 1.2, 'Government Services': 0.9,
                'News': 1.1, 'Communication': 1.05
            },
            'East': {
                'Agriculture Apps': 1.3, 'Education': 0.9, 'Banking': 0.8,
                'Social Media': 0.95, 'Video Streaming': 0.9
            },
            'Northeast': {
                'News': 0.9, 'E-commerce': 0.7, 'Social Media': 0.9,
                'Communication': 1.1, 'Government Services': 0.8
            },
            'Central': {
                'Agriculture Apps': 1.4, 'Banking': 0.85, 'E-commerce': 0.8,
                'Education': 0.9, 'Healthcare': 0.85
            }
        }
        
        # Apply regional adjustments
        region_adj = regional_factors.get(region, {})
        for service in services:
            # Calculate usage percentage with regional adjustment and some randomness
            base = base_usage[service]
            factor = region_adj.get(service, 1.0)
            random_factor = np.random.uniform(0.9, 1.1)
            
            usage_pct = base * factor * random_factor
            
            # Estimate data volume based on service type (GB/month/user)
            if service in ['Video Streaming', 'Gaming']:
                data_factor = np.random.uniform(1.5, 2.5)  # High data usage
            elif service in ['Social Media', 'Communication', 'News']:
                data_factor = np.random.uniform(0.5, 1.0)  # Medium data usage
            else:
                data_factor = np.random.uniform(0.1, 0.4)  # Low data usage
                
            service_data.append({
                'state': state,
                'service': service,
                'usage_percentage': usage_pct,
                'data_volume': data_factor
            })
    
    return pd.DataFrame(service_data)

def generate_priority_data():
    """
    Generate data to help prioritize areas for infrastructure development.
    
    Returns:
        DataFrame: Priority scoring data for states
    """
    # Get state data
    state_data = generate_state_data()
    
    # Calculate priority metrics
    priority_data = []
    
    for _, state_row in state_data.iterrows():
        state = state_row['state']
        region = state_row['region']
        population = state_row['population']
        penetration = state_row['broadband_penetration']
        
        # Calculate potential impact score (1-10)
        # Lower penetration + higher population = higher impact
        pop_factor = min(population / 10_000_000, 10) / 10  # 0-1 scale for population
        pen_factor = 1 - (penetration / 0.5)  # Inverse penetration factor (0-1 scale)
        if pen_factor < 0:  # Handle high penetration states
            pen_factor = 0
            
        # Additional regional development factor
        dev_factor = {
            'South': 0.7, 'West': 0.75, 'North': 0.8,
            'East': 0.9, 'Northeast': 0.95, 'Central': 0.85
        }.get(region, 0.8)
        
        # Calculate combined impact score
        impact_score = (0.4 * pop_factor + 0.4 * pen_factor + 0.2 * dev_factor) * 10
        impact_score = round(impact_score, 1)
        
        # Create state code (abbreviation)
        state_words = state.split()
        if len(state_words) == 1:
            state_code = state[:2]
        else:
            state_code = ''.join([word[0] for word in state_words])
        
        priority_data.append({
            'state': state,
            'state_code': state_code,
            'region': region,
            'population': population,
            'current_penetration': penetration,
            'potential_impact': impact_score
        })
    
    return pd.DataFrame(priority_data)