import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Placement Dashboard", layout="wide", page_icon="🎓")

@st.cache_data
def load_data():
    df = pd.read_csv("C:\Users\saima\Downloads\NNRG_Placement_2018_2025.csv")
    # Clean branch names
    df['Branch'] = df['Branch'].str.strip()
    df['Branch'] = df['Branch'].replace('B.Pharm acy', 'B.Pharmacy')
    return df

df = load_data()

# Enhanced Dark Theme Power BI Style CSS
st.markdown(
    """
    <style>
    /* Dark background */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Headers styling - white text */
    h1 {
        color: #ffffff;
        font-weight: 700;
        text-align: center;
        padding: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    h2, h3 {
        color: #f1f5f9;
        font-weight: 600;
    }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        color: #60a5fa;
        font-weight: bold;
        font-size: 2rem;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #e2e8f0;
        font-weight: 600;
    }
    
    /* Card-like containers - dark cards */
    .stPlotlyChart {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #334155;
    }
    
    /* Ensure chart text is visible */
    .plot-container {
        background-color: #1e293b !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #3b82f6, #8b5cf6, #ec4899);
        margin: 30px 0;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    /* Input fields */
    .stTextInput input {
        background-color: #334155;
        color: #f1f5f9;
        border: 1px solid #475569;
    }
    
    /* Select boxes */
    .stSelectbox select {
        background-color: #334155;
        color: #f1f5f9;
        border: 1px solid #475569;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: #1e293b;
        color: #f1f5f9;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with custom HTML
st.markdown(
    """
    <h1 style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
    🎓 Student Placement Analytics Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

# Sidebar Filters
with st.sidebar:
    st.markdown("### 🎯 Filters")
    
    # Year filter
    years = ['All'] + sorted(df['Year'].unique().tolist(), reverse=True)
    selected_year = st.selectbox("📅 Select Year", years)
    
    # Branch filter
    branches = ['All'] + sorted(df['Branch'].unique().tolist())
    selected_branch = st.selectbox("🎓 Select Branch", branches)
    
    # Company filter
    companies = ['All'] + sorted(df['Name of the Employer'].unique().tolist())
    selected_company = st.selectbox("🏢 Select Company", companies)
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Info")
    st.info("This dashboard provides comprehensive insights into student placement data with interactive visualizations.")

# Apply filters
filtered_df = df.copy()
if selected_year != 'All':
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]
if selected_branch != 'All':
    filtered_df = filtered_df[filtered_df['Branch'] == selected_branch]
if selected_company != 'All':
    filtered_df = filtered_df[filtered_df['Name of the Employer'] == selected_company]

# Key Metrics
total_students = len(filtered_df)
total_companies = filtered_df["Name of the Employer"].nunique()
total_branches = filtered_df["Branch"].nunique()
total_years = filtered_df["Year"].nunique()

# Metric Cards with enhanced styling
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>👨‍🎓 Students Placed</h3>
        <h1 style='color: white; margin: 10px 0;'>{}</h1>
        </div>
        """.format(total_students),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
        padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>🏢 Companies</h3>
        <h1 style='color: white; margin: 10px 0;'>{}</h1>
        </div>
        """.format(total_companies),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
        padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>🎓 Branches</h3>
        <h1 style='color: white; margin: 10px 0;'>{}</h1>
        </div>
        """.format(total_branches),
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
        padding: 20px; border-radius: 10px; text-align: center;'>
        <h3 style='color: white; margin: 0;'>📅 Years</h3>
        <h1 style='color: white; margin: 10px 0;'>{}</h1>
        </div>
        """.format(total_years),
        unsafe_allow_html=True
    )

st.markdown("---")


# Prepare data aggregations
branch_count = filtered_df["Branch"].value_counts().reset_index()
branch_count.columns = ["Branch", "Placements"]

company_count = filtered_df["Name of the Employer"].value_counts().reset_index()
company_count.columns = ["Company", "Placements"]

year_count = filtered_df.groupby("Year").size().reset_index(name="Placements")

# Branch & Year Analysis Section
st.markdown("## 📊 Branch & Yearly Analysis")

col_left, col_right = st.columns([3, 2])

with col_left:
    # Enhanced bar chart with gradient colors
    fig_bar = px.bar(
        branch_count,
        x="Branch",
        y="Placements",
        color="Placements",
        text="Placements",
        title="📚 Placements by Branch",
        color_continuous_scale="Viridis",
        height=450
    )
    fig_bar.update_traces(
        textposition="outside",
        textfont_size=12,
        hovertemplate="<b>%{x}</b><br>Placements: %{y}<extra></extra>"
    )
    fig_bar.update_layout(
        showlegend=False,
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        xaxis_title="Branch",
        yaxis_title="Number of Placements",
        font=dict(size=12, color='#f1f5f9'),
        xaxis=dict(gridcolor='#334155', color='#f1f5f9'),
        yaxis=dict(gridcolor='#334155', color='#f1f5f9'),
        title_font_color='#f1f5f9'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    # Donut chart with better colors
    fig_donut = px.pie(
        branch_count,
        names="Branch",
        values="Placements",
        hole=0.5,
        title="🎯 Branch Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3,
        height=450
    )
    fig_donut.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
    )
    fig_donut.update_layout(
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(size=11, color='#f1f5f9'),
        title_font_color='#f1f5f9',
        legend=dict(font=dict(color='#f1f5f9'))
    )
    st.plotly_chart(fig_donut, use_container_width=True)


st.markdown("---")

# Company Analysis Section
st.markdown("## 🏢 Top Recruiting Companies")

col_comp1, col_comp2 = st.columns([3, 2])

with col_comp1:
    top_companies = company_count.head(15)
    fig_company = px.bar(
        top_companies,
        y="Company",
        x="Placements",
        orientation="h",
        text="Placements",
        title="🏆 Top 15 Recruiting Companies",
        color="Placements",
        color_continuous_scale="Blues",
        height=500
    )
    fig_company.update_traces(
        textposition="outside",
        textfont_size=11,
        hovertemplate="<b>%{y}</b><br>Placements: %{x}<extra></extra>"
    )
    fig_company.update_layout(
        showlegend=False,
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        xaxis_title="Number of Placements",
        yaxis_title="",
        font=dict(size=11, color='#f1f5f9'),
        xaxis=dict(gridcolor='#334155', color='#f1f5f9'),
        yaxis=dict(categoryorder='total ascending', gridcolor='#334155', color='#f1f5f9'),
        title_font_color='#f1f5f9'
    )
    st.plotly_chart(fig_company, use_container_width=True)

with col_comp2:
    # Treemap for company distribution
    top_10_companies = company_count.head(10)
    fig_tree = px.treemap(
        top_10_companies,
        path=['Company'],
        values='Placements',
        title='🌳 Top Companies (Treemap)',
        color='Placements',
        color_continuous_scale='RdYlGn',
        height=500
    )
    fig_tree.update_traces(
        textinfo="label+value+percent parent",
        hovertemplate="<b>%{label}</b><br>Placements: %{value}<extra></extra>"
    )
    fig_tree.update_layout(
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#f1f5f9'),
        title_font_color='#f1f5f9'
    )
    st.plotly_chart(fig_tree, use_container_width=True)


st.markdown("---")

# Yearly Trends Section
st.markdown("## 📈 Placement Trends Over Years")

col_year1, col_year2 = st.columns([3, 2])

with col_year1:
    # Area chart for yearly trends
    fig_area = px.area(
        year_count,
        x="Year",
        y="Placements",
        title="📅 Year-wise Placement Trend",
        markers=True,
        color_discrete_sequence=["#667eea"],
        height=400
    )
    fig_area.update_traces(
        line=dict(width=3),
        marker=dict(size=10),
        hovertemplate="<b>Year: %{x}</b><br>Placements: %{y}<extra></extra>"
    )
    fig_area.update_layout(
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        xaxis_title="Academic Year",
        yaxis_title="Number of Placements",
        font=dict(size=12, color='#f1f5f9'),
        hovermode='x unified',
        xaxis=dict(gridcolor='#334155', color='#f1f5f9'),
        yaxis=dict(gridcolor='#334155', color='#f1f5f9'),
        title_font_color='#f1f5f9'
    )
    st.plotly_chart(fig_area, use_container_width=True)

with col_year2:
    # Top performers summary
    if len(branch_count) > 0 and len(company_count) > 0:
        top_branch = branch_count.iloc[0]["Branch"]
        top_branch_count = branch_count.iloc[0]["Placements"]
        top_company = company_count.iloc[0]["Company"]
        top_company_count = company_count.iloc[0]["Placements"]
        
        st.markdown("### 🏆 Top Performers")
        
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
            padding: 20px; border-radius: 10px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h4 style='color: #ffffff; margin: 0; font-weight: 600;'>🎓 Leading Branch</h4>
            <h2 style='color: #ffffff; margin: 10px 0; font-weight: 700;'>{top_branch}</h2>
            <p style='color: #f0fdf4; font-size: 18px; margin: 0; font-weight: 500;'>{top_branch_count} Placements</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); 
            padding: 20px; border-radius: 10px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h4 style='color: #ffffff; margin: 0; font-weight: 600;'>🏢 Top Recruiter</h4>
            <h3 style='color: #ffffff; margin: 10px 0; font-size: 16px; font-weight: 700;'>{top_company}</h3>
            <p style='color: #dbeafe; font-size: 18px; margin: 0; font-weight: 500;'>{top_company_count} Students</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Average placements per year
        avg_placements = year_count['Placements'].mean()
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
            padding: 20px; border-radius: 10px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h4 style='color: #ffffff; margin: 0; font-weight: 600;'>📊 Avg/Year</h4>
            <h2 style='color: #ffffff; margin: 10px 0; font-weight: 700;'>{avg_placements:.0f}</h2>
            <p style='color: #fef3c7; margin: 0; font-weight: 500;'>Placements</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# Year-wise Comparison Section
st.markdown("##   Year-wise Placement Comparison")

col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    # Year-wise bar chart
    fig_year_bar = px.bar(
        year_count,
        x="Year",
        y="Placements",
        title="📊 Placements Each Year",
        text="Placements",
        color="Placements",
        color_continuous_scale="Teal",
        height=400
    )
    fig_year_bar.update_traces(
        textposition="outside",
        textfont_size=14,
        hovertemplate="<b>%{x}</b><br>Placements: %{y}<extra></extra>"
    )
    fig_year_bar.update_layout(
        title_font_size=20,
        title_x=0.5,
        showlegend=False,
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        xaxis_title="Academic Year",
        yaxis_title="Number of Students",
        font=dict(size=12, color='#f1f5f9'),
        xaxis=dict(gridcolor='#334155', color='#f1f5f9'),
        yaxis=dict(gridcolor='#334155', color='#f1f5f9'),
        title_font_color='#f1f5f9'
    )
    st.plotly_chart(fig_year_bar, use_container_width=True)

with col_stat2:
    # Company type distribution (simple pie)
    company_top5 = company_count.head(5)
    others_count = company_count.iloc[5:]['Placements'].sum() if len(company_count) > 5 else 0
    
    if others_count > 0:
        company_display = pd.concat([
            company_top5,
            pd.DataFrame({'Company': ['Others'], 'Placements': [others_count]})
        ])
    else:
        company_display = company_top5
    
    fig_simple_pie = px.pie(
        company_display,
        names="Company",
        values="Placements",
        title="  Top 5 Companies vs Others",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=400
    )
    fig_simple_pie.update_traces(
        textposition='outside',
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>Students: %{value}<br>Percentage: %{percent}<extra></extra>"
    )
    fig_simple_pie.update_layout(
        title_font_size=20,
        title_x=0.5,
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(size=12, color='#f1f5f9'),
        title_font_color='#f1f5f9',
        legend=dict(font=dict(color='#f1f5f9'))
    )
    st.plotly_chart(fig_simple_pie, use_container_width=True)

st.markdown("---")

# Data Table Section
st.markdown("## 📋 Detailed Placement Records")

# Add search functionality
search_term = st.text_input("🔍 Search by Student Name, Roll No, or Company", "")

display_df = filtered_df.copy()
if search_term:
    display_df = display_df[
        display_df['Name of the Student'].str.contains(search_term, case=False, na=False) |
        display_df['Roll No'].str.contains(search_term, case=False, na=False) |
        display_df['Name of the Employer'].str.contains(search_term, case=False, na=False)
    ]

st.dataframe(
    display_df[['Year', 'Roll No', 'Name of the Student', 'Branch', 'Name of the Employer']],
    use_container_width=True,
    height=400
)

# Download button
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name='placement_data_filtered.csv',
    mime='text/csv',
)


st.markdown("---")

# Footer
st.markdown(
    """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    padding: 20px; border-radius: 10px; text-align: center; margin-top: 30px;'>
    <h3 style='color: white; margin: 0;'>🎓 Student Placement Analytics Dashboard</h3>
    <p style='color: white; margin: 10px 0;'>Powered by Streamlit & Plotly | Power BI Style Interactive Dashboard</p>
    <p style='color: #e0e7ff; margin: 0; font-size: 14px;'>📊 Data-driven insights for better placement outcomes</p>
    </div>
    """,
    unsafe_allow_html=True
)

