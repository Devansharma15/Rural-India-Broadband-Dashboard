import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.data_generator import generate_demographic_data, generate_income_education_data

def app():
    # Title and introduction
    st.title("Demographic Analysis of Internet Usage")
    st.markdown("""
    Examine how demographic factors influence broadband connectivity and usage patterns
    across rural India. Understand the relationship between age, income, education levels,
    and digital inclusion to design targeted interventions for underserved communities.
    """)

    # Load data
    demo_data = generate_demographic_data()
    income_edu_data = generate_income_education_data()

    # Filters
    st.sidebar.header("Filters")
    selected_states = st.sidebar.multiselect(
        "Filter by State",
        options=sorted(demo_data['state'].unique()),
        default=[]
    )

    # Filter data if states are selected
    if selected_states:
        filtered_demo = demo_data[demo_data['state'].isin(selected_states)]
        filtered_income_edu = income_edu_data[income_edu_data['state'].isin(selected_states)]
    else:
        filtered_demo = demo_data
        filtered_income_edu = income_edu_data

    # Age Group Analysis
    st.header("Age Group Analysis")

    # Calculate national averages for age groups
    age_national = filtered_demo.groupby('age_group').agg({
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
    st.header("Gender Analysis")

    # Calculate gender stats
    gender_stats = filtered_demo.groupby('gender').agg({
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

    # Gender Gap by Age
    gender_age = filtered_demo.groupby(['gender', 'age_group']).agg({
        'penetration': 'mean',
        'users': 'sum',
        'population': 'sum'
    }).reset_index()

    gender_age['proportion'] = gender_age['users'] / gender_age['population']

    # Create a grouped bar chart for gender gap by age
    age_order = ['0-14', '15-24', '25-34', '35-44', '45-54', '55-64', '65+']
    fig = px.bar(
        gender_age,
        x='age_group',
        y='proportion',
        color='gender',
        barmode='group',
        labels={
            'proportion': 'Internet Adoption Rate',
            'age_group': 'Age Group',
            'gender': 'Gender'
        },
        title="Gender Gap in Internet Adoption by Age Group",
        category_orders={"age_group": age_order},
        text_auto=True,
        color_discrete_map={
            'Male': '#FF9933',  # Saffron
            'Female': '#138808'  # Green
        }
    )
    fig.update_layout(height=500, xaxis={'categoryorder': 'array', 'categoryarray': age_order})
    st.plotly_chart(fig, use_container_width=True)

    # Income and Education Analysis
    st.header("Income and Education Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Prepare income data
        income_data = filtered_income_edu.groupby('income_group').agg({
            'penetration': 'mean',
            'population': 'sum',
            'users': 'sum'
        }).reset_index()
        
        income_data['proportion'] = income_data['users'] / income_data['population']
        
        # Set proper order
        income_order = ['Low', 'Lower-Middle', 'Middle', 'Upper-Middle', 'High']
        income_data['order'] = income_data['income_group'].apply(lambda x: income_order.index(x))
        income_data = income_data.sort_values('order')
        
        # Create bar chart for income groups
        fig = px.bar(
            income_data,
            x='income_group',
            y='proportion',
            labels={
                'proportion': 'Internet Adoption Rate',
                'income_group': 'Income Group'
            },
            title="Internet Adoption by Income Group",
            text_auto=True,
            category_orders={"income_group": income_order}
        )
        fig.update_traces(marker_color='#FF9933')  # Saffron from Indian flag
        fig.update_layout(height=400, xaxis={'categoryorder': 'array', 'categoryarray': income_order})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Prepare education data
        education_data = filtered_income_edu.groupby('education_level').agg({
            'penetration': 'mean',
            'population': 'sum',
            'users': 'sum'
        }).reset_index()
        
        education_data['proportion'] = education_data['users'] / education_data['population']
        
        # Set proper order
        education_order = ['Illiterate', 'Primary', 'Secondary', 'Higher Secondary', 'Graduate and Above']
        education_data['order'] = education_data['education_level'].apply(lambda x: education_order.index(x))
        education_data = education_data.sort_values('order')
        
        # Create bar chart for education levels
        fig = px.bar(
            education_data,
            x='education_level',
            y='proportion',
            labels={
                'proportion': 'Internet Adoption Rate',
                'education_level': 'Education Level'
            },
            title="Internet Adoption by Education Level",
            text_auto=True,
            category_orders={"education_level": education_order}
        )
        fig.update_traces(marker_color='#138808')  # Green from Indian flag
        fig.update_layout(height=400, xaxis={'categoryorder': 'array', 'categoryarray': education_order})
        st.plotly_chart(fig, use_container_width=True)

    # Relationship between Income and Education
    st.subheader("Income, Education, and Internet Adoption")

    # Create a heatmap of penetration by income and education
    heatmap_data = filtered_income_edu.groupby(['income_group', 'education_level']).agg({
        'penetration': 'mean'
    }).reset_index()

    # Create a pivot table for the heatmap
    heatmap_pivot = heatmap_data.pivot(index='income_group', columns='education_level', values='penetration')

    # Ensure proper order of rows and columns
    heatmap_pivot = heatmap_pivot.reindex(income_order)
    heatmap_pivot = heatmap_pivot.reindex(columns=education_order)

    # Create the heatmap
    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Education Level", y="Income Group", color="Adoption Rate"),
        title="Internet Adoption Rate by Income and Education",
        color_continuous_scale='Viridis',
        text_auto=True,
        aspect="auto"
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Urban-Rural Digital Divide
    st.header("Urban-Rural Digital Divide")

    # Calculate urban-rural comparison
    urban_rural = filtered_demo.groupby('state').agg({
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

    # Key insights
    st.header("Key Demographic Insights")

    st.markdown("""
    Analysis of demographic factors reveals important patterns in rural internet adoption:

    1. **Age Divide**: The 15-34 age group shows the highest adoption rates, with a significant drop-off in the 55+ demographic, indicating a generational digital divide.

    2. **Gender Gap**: There is a persistent gender gap in internet adoption across all age groups, with the gap widening in older age brackets.

    3. **Education Impact**: Education level is the strongest predictor of internet adoption, with those having higher secondary education or above showing 3-5x higher adoption rates than illiterate groups.

    4. **Income Correlation**: While income shows a strong positive correlation with adoption, education level appears to be a more significant factor, especially in middle-income households.

    5. **Urban-Rural Gap**: The urban-rural digital divide varies significantly by state, with some states showing a gap ratio of over 4x while others have achieved more equitable access.

    6. **Youth Opportunity**: The relatively high adoption rates among rural youth (15-24) represent an opportunity for targeted skill development and digital literacy programs.
    """)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Demographic Analysis - Rural India Broadband",
        page_icon="👨‍👩‍👧‍👦",
        layout="wide"
    )
    app()