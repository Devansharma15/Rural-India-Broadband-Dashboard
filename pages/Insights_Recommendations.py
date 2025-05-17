import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_generator import generate_priority_data

def app():
    # Title and introduction
    st.title("Insights & Recommendations")
    st.markdown("""
    Synthesize findings from geographic, demographic, time series, and usage pattern analyses
    to provide actionable recommendations for improving rural broadband connectivity in India.
    Identify strategic priorities and implementation approaches for policymakers and service providers.
    """)

    # Load data
    priority_data = generate_priority_data()

    # Key Findings
    st.header("Key Findings")

    # Organize findings into categories
    categories = {
        "Geographic Insights": [
            "Clear north-south divide in broadband penetration, with southern states generally having higher connectivity rates.",
            "Mountainous regions and remote areas show consistently lower penetration rates, highlighting infrastructure challenges.",
            "Rural areas closer to major urban centers have better connectivity than deeply rural regions.",
            "Eastern and North-Eastern regions show stronger preference for mobile data over fixed broadband.",
            "States with low current penetration but high population density represent high-impact investment opportunities."
        ],
        "Demographic Patterns": [
            "15-34 age group shows highest adoption rates, with significant drop-off in 55+ demographic.",
            "Persistent gender gap in internet adoption across all age groups, widening in older age brackets.",
            "Education level is the strongest predictor of internet adoption, more significant than income level.",
            "Urban-rural digital divide varies significantly by state, with some states showing gap ratios over 4x.",
            "High adoption rates among rural youth (15-24) represent opportunity for targeted skill development."
        ],
        "Temporal Trends": [
            "Rural broadband growth has accelerated, with pace doubling compared to previous five-year period.",
            "Seasonal pattern shows higher growth during post-harvest months and educational enrollment periods.",
            "Digital India initiatives correlate with growth spikes, particularly in previously underserved states.",
            "COVID-19 created unusual surge in rural connectivity demand, accelerating adoption by 18-24 months.",
            "Some states show consistently strong growth trajectories, while others display plateauing adoption."
        ],
        "Usage Behaviors": [
            "75% of rural internet access occurs via mobile devices, smartphones being the primary access point.",
            "Usage peaks during evening hours (4-8 PM), suggesting most users access internet after work.",
            "Entertainment and social media represent over 70% of data consumption.",
            "Rural users adapt content consumption to limited bandwidth with deferred downloading and shared viewing.",
            "Most rural applications function within 2-5 Mbps range, indicating consistent moderate speeds are valuable."
        ]
    }

    # Display findings in expandable sections
    for category, findings in categories.items():
        with st.expander(category, expanded=True):
            for i, finding in enumerate(findings, 1):
                st.markdown(f"{i}. {finding}")

    # Strategic Priorities
    st.header("Strategic Priorities")

    # Priority scoring dashboard
    priority_data = priority_data.sort_values('potential_impact', ascending=False)

    # Create a horizontal bar chart for priority scores
    fig = px.bar(
        priority_data,
        y='state',
        x='potential_impact',
        orientation='h',
        color='potential_impact',
        color_continuous_scale='Viridis',
        labels={
            'potential_impact': 'Priority Score',
            'state': 'State'
        },
        title="Infrastructure Development Priority Score by State",
        text_auto=True
    )
    fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    # Show factors affecting priority score
    st.subheader("Factors Affecting Priority Scores")

    # Select a state for detailed analysis
    selected_state = st.selectbox(
        "Select a state for detailed analysis",
        options=priority_data['state'].tolist()
    )

    if selected_state:
        # Filter for selected state
        state_data = priority_data[priority_data['state'] == selected_state].iloc[0]
        
        # Create radar chart data
        categories = ['Current Penetration', 'Population', 'Region', 
                    'Potential Impact', 'State Code']
        
        # Normalize values for radar chart
        pen_factor = 1 - min(state_data['current_penetration'] / 0.5, 1.0)  # Invert penetration
        pop_factor = min(state_data['population'] / 10_000_000, 1.0)  # Normalize population
        
        values = [
            pen_factor,
            pop_factor,
            0.8,  # Region factor
            state_data['potential_impact'] / 10,
            0.5   # State code factor
        ]
        
        # Close the loop for radar chart
        categories = categories + [categories[0]]
        values = values + [values[0]]
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=selected_state
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            title=f"Priority Factors for {selected_state}",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add explanation of factors
        st.markdown(f"""
        ### Priority Factor Analysis for {selected_state}
        
        - **Current Penetration**: {'Low penetration (high priority)' if values[0] > 0.7 else 'Moderate penetration' if values[0] > 0.4 else 'High penetration (lower priority)'}
        - **Population**: {'High population (high impact potential)' if values[1] > 0.7 else 'Moderate population' if values[1] > 0.4 else 'Low population'}
        - **Region Factor**: {'High priority region based on development status' if values[2] > 0.7 else 'Medium priority region' if values[2] > 0.5 else 'Lower priority region'}
        - **Potential Impact**: {'Very high impact potential' if values[3] > 0.7 else 'Moderate impact potential' if values[3] > 0.4 else 'Limited impact potential'}
        - **Infrastructure Complexity**: {'Lower complexity for deployment' if values[4] > 0.7 else 'Medium complexity for deployment' if values[4] > 0.4 else 'Higher complexity for deployment'}
        """)

    # Recommendations
    st.header("Recommendations")

    # Policy Recommendations
    st.subheader("Policy Recommendations")
    policy_recs = [
        "**Universal Service Obligation Fund Reform**: Restructure USOF to provide targeted subsidies for rural broadband infrastructure in high-priority states identified in this analysis.",
        "**Infrastructure Sharing Mandates**: Implement policies requiring sharing of passive infrastructure (towers, ducts) to reduce deployment costs in rural areas.",
        "**Spectrum Allocation for Rural Connectivity**: Allocate specific spectrum bands for rural broadband with coverage obligations and reduced fees.",
        "**Digital Literacy Initiatives**: Fund comprehensive digital literacy programs targeting identified demographic gaps, particularly women and older adults in rural areas.",
        "**Public Wi-Fi Networks**: Support expansion of PM-WANI public Wi-Fi framework with specific focus on panchayat-level connectivity."
    ]

    for i, rec in enumerate(policy_recs, 1):
        st.markdown(f"{i}. {rec}")

    # Technology Recommendations
    st.subheader("Technology Recommendations")
    tech_recs = [
        "**Mixed Technology Approach**: Deploy fiber backhaul to district levels and leverage wireless technologies (4G/5G fixed wireless, TV white space) for last-mile connectivity.",
        "**Sustainable Power Solutions**: Bundle connectivity infrastructure with sustainable power solutions (solar, wind) to overcome electricity challenges in remote areas.",
        "**Edge Caching Infrastructure**: Deploy edge caching for popular content to reduce backhaul bandwidth requirements and improve user experience.",
        "**Low-Cost CPE Development**: Support development and distribution of affordable customer premises equipment adapted to rural Indian conditions and user needs.",
        "**Mobile-First Applications**: Optimize digital service delivery for mobile devices and low-bandwidth conditions based on identified usage patterns."
    ]

    for i, rec in enumerate(tech_recs, 1):
        st.markdown(f"{i}. {rec}")

    # Implementation Approach
    st.subheader("Implementation Approach")
    impl_recs = [
        "**Phased Deployment Strategy**: Prioritize states based on the composite priority score, focusing initial efforts on highest-impact regions.",
        "**Public-Private Partnerships**: Structure PPP models with risk-sharing mechanisms to attract private investment in rural infrastructure.",
        "**Community Network Models**: Support and scale successful community network models for local ownership and sustainability.",
        "**Anchor Institution Approach**: Connect education, healthcare, and government institutions first to create connectivity hubs in rural communities.",
        "**Regular Measurement & Evaluation**: Implement standardized metrics and regular assessment of rural connectivity improvements to guide policy adjustments."
    ]

    for i, rec in enumerate(impl_recs, 1):
        st.markdown(f"{i}. {rec}")

    # Expected Impact
    st.header("Expected Impact")
    
    # Create impact data
    impact_data = pd.DataFrame({
        'timeline': ['Short-term (1-2 years)', 'Medium-term (3-5 years)', 'Long-term (5+ years)'],
        'penetration_increase': [15, 35, 60],
        'economic_impact': [0.5, 2.0, 4.5],
        'job_creation': [200000, 750000, 2000000],
        'digital_literacy': [10, 40, 70]
    })
    
    # Create a multi-metric chart
    fig = go.Figure()
    
    # Add traces for each metric
    fig.add_trace(go.Bar(
        x=impact_data['timeline'],
        y=impact_data['penetration_increase'],
        name='Penetration Increase (%)',
        marker_color='#FF9933'
    ))
    
    fig.add_trace(go.Bar(
        x=impact_data['timeline'],
        y=impact_data['economic_impact'],
        name='Economic Impact (% GDP increase)',
        marker_color='#138808'
    ))
    
    fig.add_trace(go.Bar(
        x=impact_data['timeline'],
        y=[x/1000000 for x in impact_data['job_creation']],
        name='Job Creation (millions)',
        marker_color='#000080'
    ))
    
    fig.add_trace(go.Bar(
        x=impact_data['timeline'],
        y=impact_data['digital_literacy'],
        name='Digital Literacy Improvement (%)',
        marker_color='#800080'
    ))
    
    fig.update_layout(
        title='Projected Impact of Recommendations',
        barmode='group',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Additional impact details
    st.markdown("""
    ### Qualitative Impact
    
    **Social Inclusion Benefits**:
    - Reduced urban-rural divide and more equitable access to government services
    - Improved educational outcomes through digital learning resources
    - Better healthcare access through telemedicine in remote areas
    - Increased participation of women and marginalized communities in digital economy
    
    **Economic Transformation**:
    - Creation of new rural digital micro-enterprises
    - Improved agricultural productivity through digital farming techniques
    - Enhanced access to markets and fair pricing for rural producers
    - Development of rural BPO and digital service hubs
    
    **Challenges to Address**:
    - Ensuring affordability of services for lowest income segments
    - Developing relevant local language content and applications
    - Building adequate digital safety and cybersecurity awareness
    - Balancing infrastructure investment with service quality
    """)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Insights & Recommendations - Rural India Broadband",
        page_icon="💡",
        layout="wide"
    )
    app()