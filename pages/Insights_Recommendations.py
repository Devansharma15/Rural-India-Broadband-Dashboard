import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_generator import generate_state_data, generate_district_data, generate_priority_data
from utils.helper import load_image_from_url

# Page configuration
st.set_page_config(
    page_title="Insights & Recommendations - Rural India Broadband",
    page_icon="💡",
    layout="wide"
)

# Title and introduction
st.title("Insights & Recommendations")
st.markdown("""
Based on the comprehensive analysis of broadband connectivity and usage patterns across
rural India, this section provides key insights and strategic recommendations for
improving digital inclusion in underserved communities.
""")

# Display a banner image
st.image(
    load_image_from_url("https://pixabay.com/get/g53773473f97de9f8b883c092bde5e2c7277d7f669ee17ee95bf48d545be916605f0c3d7382e4a2ee752ef08451bd5e0335592ab2c6a891794733865e92a5257e_1280.jpg"),
    caption="Digital India Initiatives in Rural Areas",
    use_container_width=True
)

# Load data
state_data = generate_state_data()
district_data = generate_district_data()
priority_data = generate_priority_data()

# Key Findings
st.header("Key Findings")

# Summary of key metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Rural Penetration",
        f"{np.mean(state_data['broadband_penetration']) * 100:.1f}%",
        delta="+1.2% YoY"
    )

with col2:
    st.metric(
        "Smartphone Penetration",
        "37.8%",
        delta="+5.4% YoY"
    )

with col3:
    urban_rural_gap = np.mean(state_data['urban_penetration']) / np.mean(state_data['broadband_penetration']) if 'urban_penetration' in state_data.columns else 3.2
    st.metric(
        "Urban-Rural Gap",
        f"{urban_rural_gap:.1f}x",
        delta="-0.2x YoY",
        delta_color="inverse"
    )

# Top Insights
st.subheader("Top Insights from the Analysis")

insights = [
    {
        "title": "Geographic Disparities",
        "description": "There is a significant regional disparity in broadband penetration, with southern and western states showing 2-3x higher penetration rates than central and eastern states.",
        "impact": "High",
        "category": "Geographic"
    },
    {
        "title": "Mobile-First Access",
        "description": "Over 75% of rural internet users access primarily through mobile devices, with limited fixed broadband adoption even in areas with available infrastructure.",
        "impact": "High",
        "category": "Usage"
    },
    {
        "title": "Demographic Divide",
        "description": "The 15-34 age group shows significantly higher adoption rates (>40%) compared to 55+ demographics (<15%), creating a generational digital divide.",
        "impact": "Medium",
        "category": "Demographic"
    },
    {
        "title": "Education Correlation",
        "description": "Education level is the strongest predictor of internet adoption, with secondary education or higher showing 3-5x greater adoption rates than primary education only.",
        "impact": "High",
        "category": "Demographic"
    },
    {
        "title": "Gender Gap",
        "description": "A persistent gender gap exists across all states, with male users outnumbering female users by approximately 60:40, though this gap is narrowing in southern states.",
        "impact": "Medium",
        "category": "Demographic"
    },
    {
        "title": "Entertainment Dominance",
        "description": "Entertainment and social media account for >70% of data consumption, with educational content growing but still representing <15% of usage.",
        "impact": "Medium",
        "category": "Usage"
    },
    {
        "title": "Seasonal Usage Patterns",
        "description": "Data consumption shows seasonal variations tied to agricultural cycles, with 15-20% higher usage during non-peak farming periods.",
        "impact": "Low",
        "category": "Usage"
    },
    {
        "title": "Infrastructure Limitations",
        "description": "Approximately 35% of rural subscribers experience connectivity issues due to inadequate tower density and backhaul capacity rather than last-mile connectivity.",
        "impact": "High",
        "category": "Infrastructure"
    }
]

insights_df = pd.DataFrame(insights)

# Create expandable sections for each insight
for i, insight in insights_df.iterrows():
    with st.expander(f"{insight['title']} (Impact: {insight['impact']})"):
        st.markdown(f"**Category**: {insight['category']}")
        st.markdown(insight['description'])

# Priority Areas
st.header("Priority Areas for Intervention")

# Create a bubble chart for priority areas
fig = px.scatter(
    priority_data,
    x='current_penetration',
    y='potential_impact',
    size='population',
    color='region',
    hover_name='state',
    text='state_code',
    labels={
        'current_penetration': 'Current Broadband Penetration',
        'potential_impact': 'Potential Impact Score (1-10)',
        'population': 'Rural Population',
        'region': 'Region'
    },
    title="Priority Matrix for Broadband Infrastructure Development"
)

fig.update_traces(textposition='top center')
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

# Strategic Recommendations
st.header("Strategic Recommendations")

# Infrastructure Development
st.subheader("1. Infrastructure Development")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### High-Priority Actions:
    - Deploy additional 4G/5G towers in underserved districts of Bihar, Uttar Pradesh, Madhya Pradesh, and Jharkhand
    - Strengthen middle-mile infrastructure with additional fiber points of presence in rural clusters
    - Implement solar-powered mobile towers in regions with unreliable electricity
    
    #### Expected Impact:
    - Increase coverage to 85% of rural population from current 73%
    - Reduce average latency from 120ms to <80ms
    - Improve average available bandwidth from 2.3 Mbps to >5 Mbps
    """)

with col2:
    # Create a simple map highlighting priority states
    priority_states = ['Bihar', 'Uttar Pradesh', 'Madhya Pradesh', 'Jharkhand', 'Rajasthan', 'Chhattisgarh']
    infra_priority = state_data.copy()
    infra_priority['priority'] = infra_priority['state'].apply(lambda x: 'High Priority' if x in priority_states else 'Normal')
    
    fig = px.choropleth(
        infra_priority,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='priority',
        color_discrete_map={
            'High Priority': '#FF0000',
            'Normal': '#AAAAAA'
        },
        hover_data=['state', 'broadband_penetration'],
        title="Infrastructure Development Priority States"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=400, margin={"r":0,"t":30,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

# Digital Literacy and Skills
st.subheader("2. Digital Literacy and Skills Development")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### Target Demographics:
    - Women in rural areas (to address gender gap)
    - Adults aged 35-55 (to bridge generational divide)
    - Agricultural workers and small business owners (to enable economic benefits)
    
    #### Recommended Programs:
    - Mobile-based digital literacy modules in local languages
    - Community training centers at panchayat level
    - Peer learning networks leveraging existing high-adoption demographics
    - Sector-specific training (agriculture, handicrafts, retail)
    """)

with col2:
    # Create a horizontal bar chart showing program impact
    program_data = pd.DataFrame({
        'program': ['Mobile-based literacy modules', 'Community training centers', 'Peer learning networks', 'Sector-specific training'],
        'reach': [65, 40, 30, 25],
        'effectiveness': [0.65, 0.82, 0.75, 0.90]
    })
    
    program_data['impact_score'] = program_data['reach'] * program_data['effectiveness']
    program_data = program_data.sort_values('impact_score', ascending=True)
    
    fig = px.bar(
        program_data,
        y='program',
        x='impact_score',
        orientation='h',
        color='effectiveness',
        color_continuous_scale='Viridis',
        labels={
            'impact_score': 'Projected Impact Score',
            'program': 'Program Type',
            'effectiveness': 'Program Effectiveness'
        },
        title="Projected Impact of Digital Literacy Programs"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Service Development
st.subheader("3. Relevant Service Development")

st.markdown("""
#### Key Service Categories to Develop:
- Agricultural information and market linkage applications
- Localized educational content in regional languages
- Government service delivery platforms optimized for low-bandwidth
- Healthcare information and telemedicine services
- Financial inclusion and digital payment solutions

#### Implementation Approach:
- Partner with local content creators for language-appropriate services
- Optimize applications for low-end smartphones and intermittent connectivity
- Leverage public-private partnerships to develop sector-specific applications
- Create offline-capable applications that sync when connectivity is available
""")

# Create a pie chart showing service relevance
service_relevance = pd.DataFrame({
    'service_category': ['Agriculture', 'Education', 'Government Services', 'Healthcare', 'Financial Services', 'Entertainment', 'Social Media'],
    'relevance_score': [27, 22, 18, 15, 10, 5, 3]
})

fig = px.pie(
    service_relevance,
    names='service_category',
    values='relevance_score',
    title="Relevance of Service Categories for Rural Development",
    color_discrete_sequence=px.colors.sequential.Viridis
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Policy Recommendations
st.subheader("4. Policy Recommendations")

policy_recommendations = [
    {
        "policy": "Rural Broadband Subsidy",
        "description": "Provide direct subsidies to telecom operators based on active rural subscribers",
        "implementation": "Medium",
        "impact": "High"
    },
    {
        "policy": "Spectrum Fee Waiver",
        "description": "Reduce spectrum fees for operators who exceed rural coverage targets",
        "implementation": "Easy",
        "impact": "Medium"
    },
    {
        "policy": "Community Network Licensing",
        "description": "Create simplified licensing for community-operated networks in underserved areas",
        "implementation": "Complex",
        "impact": "Medium"
    },
    {
        "policy": "Digital Literacy in School Curriculum",
        "description": "Integrate digital skills in primary and secondary education curriculum",
        "implementation": "Medium",
        "impact": "High"
    },
    {
        "policy": "Public WiFi Expansion",
        "description": "Deploy public WiFi in all Gram Panchayat buildings with 10 Mbps minimum connectivity",
        "implementation": "Medium",
        "impact": "Medium"
    },
    {
        "policy": "Local Content Development Fund",
        "description": "Create fund to support development of applications and content in local languages",
        "implementation": "Easy",
        "impact": "Medium"
    }
]

policy_df = pd.DataFrame(policy_recommendations)

# Create a quadrant chart for policy recommendations
fig = px.scatter(
    policy_df,
    x='implementation',
    y='impact',
    text='policy',
    size_max=60,
    labels={
        'implementation': 'Ease of Implementation',
        'impact': 'Potential Impact'
    },
    title="Policy Recommendation Matrix",
    category_orders={
        'implementation': ['Easy', 'Medium', 'Complex'],
        'impact': ['Low', 'Medium', 'High']
    }
)

fig.update_traces(textposition='top center', marker=dict(size=20))
fig.update_layout(
    height=500,
    xaxis=dict(
        categoryorder='array',
        categoryarray=['Easy', 'Medium', 'Complex']
    ),
    yaxis=dict(
        categoryorder='array',
        categoryarray=['Low', 'Medium', 'High']
    )
)

# Add quadrant lines
fig.add_shape(
    type="line", line=dict(dash="dash", width=1, color="gray"),
    x0="Easy", y0="Medium", x1="Complex", y1="Medium"
)
fig.add_shape(
    type="line", line=dict(dash="dash", width=1, color="gray"),
    x0="Medium", y0="Low", x1="Medium", y1="High"
)

# Add annotations for quadrants
fig.add_annotation(x="Easy", y="High", text="Quick Wins", showarrow=False, font=dict(size=14))
fig.add_annotation(x="Complex", y="High", text="Major Projects", showarrow=False, font=dict(size=14))
fig.add_annotation(x="Easy", y="Low", text="Low Priority", showarrow=False, font=dict(size=14))
fig.add_annotation(x="Complex", y="Low", text="Avoid", showarrow=False, font=dict(size=14))

st.plotly_chart(fig, use_container_width=True)

# Implementation Roadmap
st.header("Implementation Roadmap")

# Create a timeline chart
timeline_data = pd.DataFrame([
    {"Phase": "Phase 1: Infrastructure Enhancement", "Start": "2023-07", "End": "2024-06", "Category": "Infrastructure"},
    {"Phase": "Phase 2: Digital Literacy Programs", "Start": "2023-10", "End": "2025-03", "Category": "Education"},
    {"Phase": "Phase 3: Content Development", "Start": "2024-01", "End": "2025-06", "Category": "Content"},
    {"Phase": "Phase 4: Policy Reform Implementation", "Start": "2023-07", "End": "2024-12", "Category": "Policy"},
    {"Phase": "Phase 5: Community Network Pilots", "Start": "2024-04", "End": "2025-09", "Category": "Infrastructure"},
    {"Phase": "Phase 6: Monitoring & Evaluation", "Start": "2023-07", "End": "2025-12", "Category": "Evaluation"}
])

# Convert date strings to datetime
timeline_data["Start"] = pd.to_datetime(timeline_data["Start"])
timeline_data["End"] = pd.to_datetime(timeline_data["End"])

# Calculate duration
timeline_data["Duration"] = timeline_data["End"] - timeline_data["Start"]
timeline_data["Duration_Days"] = timeline_data["Duration"].dt.days

# Create a Gantt chart
fig = px.timeline(
    timeline_data, 
    x_start="Start", 
    x_end="End", 
    y="Phase",
    color="Category",
    title="Implementation Roadmap (2023-2025)",
    labels={"Phase": "Initiative"}
)
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# Expected Outcomes
st.header("Expected Outcomes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### Short-term Outcomes (1-2 years):
    - Increase rural broadband penetration by 15 percentage points
    - Reduce urban-rural digital divide ratio from 3.2x to 2.5x
    - Narrow gender gap in internet usage from 60:40 to 55:45
    - Increase average rural data consumption by 25%
    - Deploy 500+ additional mobile towers in high-priority districts
    """)
    
with col2:
    st.markdown("""
    #### Long-term Outcomes (3-5 years):
    - Achieve minimum 50% broadband penetration across all states
    - Reduce urban-rural digital divide ratio to below 2.0x
    - Achieve gender parity in younger demographics (15-34 age group)
    - Increase digital literacy rate to match functional literacy rate
    - Develop thriving ecosystem of locally-relevant digital services
    """)

# Create a forecast chart
years = [2022, 2023, 2024, 2025, 2026, 2027]
baseline_penetration = [0.28, 0.30, 0.32, 0.34, 0.36, 0.38]
intervention_penetration = [0.28, 0.32, 0.38, 0.45, 0.52, 0.60]

forecast_data = pd.DataFrame({
    'Year': years + years,
    'Penetration': baseline_penetration + intervention_penetration,
    'Scenario': ['Baseline'] * len(years) + ['With Interventions'] * len(years)
})

fig = px.line(
    forecast_data,
    x='Year',
    y='Penetration',
    color='Scenario',
    labels={
        'Penetration': 'Rural Broadband Penetration',
        'Year': 'Year',
        'Scenario': 'Scenario'
    },
    title="Projected Impact of Recommended Interventions",
    markers=True,
    line_shape='spline',
    color_discrete_map={
        'Baseline': '#AAAAAA',
        'With Interventions': '#FF9933'  # Saffron from Indian flag
    }
)
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# Monitoring Framework
st.header("Monitoring & Evaluation Framework")

st.markdown("""
#### Key Performance Indicators:
1. **Access Metrics**:
   - Rural broadband penetration rate (overall and by state)
   - Urban-rural penetration gap ratio
   - Gender distribution of internet users
   - Age distribution of internet users

2. **Usage Metrics**:
   - Average data consumption per user (mobile and fixed)
   - Service category distribution (entertainment, education, government services, etc.)
   - Daily active user patterns
   - Application diversity index

3. **Infrastructure Metrics**:
   - Average download/upload speeds
   - Network reliability (uptime percentage)
   - Tower density per rural population
   - Fiber point of presence density

4. **Impact Metrics**:
   - Digital literacy rates
   - Digital service adoption for government programs
   - E-commerce participation from rural areas
   - Digital payment penetration
""")

# Monitoring dashboard example
st.subheader("Sample Monitoring Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    # Create a gauge chart for overall progress
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 38,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Rural Penetration (%)"},
        delta = {'reference': 28, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#FF9933"},
            'steps': [
                {'range': [0, 25], 'color': "#FF9933"},
                {'range': [25, 50], 'color': "#FFFFFF"},
                {'range': [50, 75], 'color': "#138808"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Create a gauge chart for gender ratio
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 42,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Female Users (%)"},
        delta = {'reference': 38, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#138808"},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 40], 'color': "#FFCC00"},
                {'range': [40, 50], 'color': "#FFCC00"},
                {'range': [50, 100], 'color': "#138808"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

with col3:
    # Create a gauge chart for average speed
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = 3.8,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Avg. Speed (Mbps)"},
        delta = {'reference': 2.3, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [0, 10]},
            'bar': {'color': "#0000FF"},
            'steps': [
                {'range': [0, 2], 'color': "lightgray"},
                {'range': [2, 5], 'color': "#FFCC00"},
                {'range': [5, 10], 'color': "#138808"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 5
            }
        }
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)

# Conclusion
st.header("Conclusion")

st.markdown("""
The analysis of broadband connectivity and usage patterns in rural India highlights both challenges and opportunities
for expanding digital inclusion. While significant disparities exist across geographic, demographic, and 
socioeconomic dimensions, there are clear pathways to addressing these gaps through targeted infrastructure 
development, digital literacy programs, relevant service creation, and supportive policy frameworks.

By implementing the recommendations outlined in this dashboard, it is possible to accelerate rural broadband 
adoption substantially beyond the current trajectory, potentially achieving 60% penetration by 2027 compared to 
the baseline projection of 38%.

The most impactful interventions will address multiple dimensions simultaneously:
1. **Expanding physical infrastructure** in underserved regions
2. **Building digital capabilities** among key demographic groups 
3. **Developing locally relevant content and services**
4. **Creating enabling policy environments** for rural connectivity

This multifaceted approach, combined with regular monitoring and adaptation, offers the best path toward 
bridging the digital divide and ensuring that rural India can fully participate in and benefit from the 
digital economy.
""")

# Display a final banner image
st.image(
    load_image_from_url("https://pixabay.com/get/g764ffb370a9ddab5cb82ac8b30b3faf51d80f0a6df9c80f3a146e122139442584983fcb81de49191ba8c929426f34629dfca918cb7f37824f03f2db372e5273f_1280.jpg"),
    caption="The Future of Digital India",
    use_container_width=True
)

# Download report option
st.sidebar.markdown("### Download Full Report")
st.sidebar.info("This feature would allow users to download a comprehensive PDF report with all analyses and recommendations.")
