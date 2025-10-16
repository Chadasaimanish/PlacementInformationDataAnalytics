import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="🎓 Placement Dashboard", layout="wide")

# --- Custom CSS ---
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(120deg, #f6d365, #fda085);
        color: #000000;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fbc2eb 0%, #a6c1ee 100%);
        color: black;
    }
    [data-testid="stMetricValue"] {
        color: #000;
        font-weight: bold;
    }
    [data-testid="stMetricLabel"] {
        color: #2f3640;
        font-weight: 600;
    }
    h1 {
        text-align: center;
        color: #2d3436;
        font-family: 'Trebuchet MS', sans-serif;
        text-shadow: 1px 1px 2px #fff;
    }
    h3, h2 {
        color: #2d3436;
    }
    div[data-testid="stDataFrame"] {
        background: rgba(255,255,255,0.9);
        border-radius: 12px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Title ---
st.title("🌇 Placement Data Analytics Dashboard")

# --- Load Data ---
df = pd.read_csv("C:\\Users\\saima\\Downloads\\NNRG_Placement_2018_2025.csv")

# --- Sidebar Filter ---
st.sidebar.header("📅 Filter by Year")
selected_year = st.sidebar.selectbox("Select Year", ["All"] + sorted(df['Year'].unique().tolist()))

# --- Filter Data ---
filtered_df = df if selected_year == "All" else df[df['Year'] == selected_year]

# --- Summary Metrics ---
total_students = len(df)
total_branches = df['Branch'].nunique()
total_recruiters = df['Name of the Employer'].nunique()
total_placements = len(filtered_df)

st.markdown("<h3 style='text-align:center;'>📊 Summary Overview</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("👨‍🎓 Total Students", total_students)
col2.metric("🏫 Unique Branches", total_branches)
col3.metric("🏢 Total Recruiters", total_recruiters)
col4.metric("🎯 Total Placements", total_placements)

st.markdown("---")

# --- Top Branch of Selected Year ---
if selected_year != "All":
    st.markdown(f"<h3 style='text-align:center;'>🏆 Top Branch in {selected_year}</h3>", unsafe_allow_html=True)
    if not filtered_df.empty:
        top_branch = filtered_df['Branch'].value_counts().idxmax()
        top_branch_count = filtered_df['Branch'].value_counts().max()
        st.success(f"🎓 **{top_branch}** achieved the highest placements in {selected_year} with **{top_branch_count} students**.")
    else:
        st.warning("No data available for the selected year.")
    st.markdown("---")

# --- Side-by-side Graphs ---
col1, col2 = st.columns(2)

# 1️⃣ Year-wise Placement Bar Chart
year_counts = df['Year'].value_counts().sort_index()
fig_bar = px.bar(
    x=year_counts.index,
    y=year_counts.values,
    color=year_counts.index,
    color_continuous_scale='viridis',
    labels={'x': 'Year', 'y': 'Number of Placements'},
    title="📊 Year-wise Placement Count"
)
fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
col1.plotly_chart(fig_bar, use_container_width=True)

# 2️⃣ Pie chart: Branch-wise distribution
branch_counts = filtered_df['Branch'].value_counts()
fig_pie = px.pie(
    names=branch_counts.index,
    values=branch_counts.values,
    title=f"🧭 Branch-wise Distribution ({'All Years' if selected_year == 'All' else selected_year})",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
col2.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- 🌳 Beautiful Treemap with "Squeeze" Color Palette ---
if not filtered_df.empty:
    branch_counts_df = filtered_df['Branch'].value_counts().reset_index()
    branch_counts_df.columns = ['Branch', 'Count']

    fig_treemap = px.treemap(
        branch_counts_df,
        path=['Branch'],
        values='Count',
        color='Count',
        color_continuous_scale=px.colors.sequential.Sunset,  # <<< SQUEEZE-LIKE GRADIENT
        title=f"🌿 Branch-wise Placement Treemap ({'All Years' if selected_year == 'All' else selected_year})"
    )

    fig_treemap.update_traces(
        textinfo="label+value",
        hovertemplate='<b>%{label}</b><br>Placements: %{value}<extra></extra>',
        marker=dict(line=dict(color='white', width=2))
    )

    fig_treemap.update_layout(
        margin=dict(t=50, l=10, r=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black', size=14)
    )

    st.plotly_chart(fig_treemap, use_container_width=True)
else:
    st.info("No treemap available for the selected year.")

st.markdown("---")

# --- Recruiter-wise Placement Count ---
st.markdown(f"<h3 style='text-align:center;'>🏢 Top Recruiters ({'All Years' if selected_year == 'All' else selected_year})</h3>", unsafe_allow_html=True)
if not filtered_df.empty:
    recruiter_counts = filtered_df['Name of the Employer'].value_counts().reset_index()
    recruiter_counts.columns = ['Recruiter', 'Placements']
    fig_recruiters = px.bar(
        recruiter_counts.head(10),
        x='Recruiter',
        y='Placements',
        color='Placements',
        color_continuous_scale='Sunsetdark',
        title=f"Top 10 Recruiters ({'All Years' if selected_year == 'All' else selected_year})"
    )
    fig_recruiters.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_recruiters, use_container_width=True)
else:
    st.info("No recruiter data available for the selected year.")

st.markdown("---")

# --- Full Data Table ---
st.markdown("<h3 style='text-align:center;'>📋 Full Placement Data</h3>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)
 