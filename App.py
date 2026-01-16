import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Net Zero Health Impact", layout="wide")

@st.cache_data
def load_data():
    # Loading the compressed Parquet files

    l2 = pd.read_excel("Level_2.xlsx")
    lk = pd.read_excel("lookups.xlsx")

# Save as Parquet to shrink the file size for GitHub/Cloud
    l2.to_parquet("Level_2.parquet")
    lk.to_parquet("lookups.parquet")
    l2 = pd.read_parquet("Level_2.parquet")
    lk = pd.read_parquet("lookups.parquet")
    return pd.merge(l2, lk, on='small_area')

df = load_data()

# 2. Sidebar Filters
st.sidebar.header("Geography Filters")
selected_nation = st.sidebar.selectbox("Select Nation", df['nation'].unique())

# Filter councils based on nation to make the list shorter
councils = df[df['nation'] == selected_nation]['local_authority'].unique()
selected_council = st.sidebar.selectbox("Select Local Authority", councils)

# 3. Data Processing
council_df = df[df['local_authority'] == selected_council]

# 4. Metrics
st.title(f"📈 Health Co-benefits: {selected_council}")
total_benefit = council_df['sum'].sum()
st.metric("Total Cumulative Benefit (2025-2050)", f"£{total_benefit:,.0f}M")

# 5. Annual Trend Chart (Unique to Level 2)
# We identify year columns (2025, 2026...) and 'melt' them for the chart
year_cols = [col for col in council_df.columns if str(col).isdigit()]
trend_data = council_df.melt(id_vars=['co-benefit_type'], value_vars=year_cols, 
                             var_name='Year', value_name='Benefit')

fig_trend = px.line(trend_data, x='Year', y='Benefit', color='co-benefit_type',
                    title="Annual Growth of Health Benefits",
                    labels={'Benefit': 'Value (£ Million)'})

st.plotly_chart(fig_trend, use_container_width=True)

# 6. Summary Bar Chart
fig_bar = px.bar(council_df, x='co-benefit_type', y='sum', 
                 title="Total Benefit by Category",
                 labels={'sum': 'Total Benefit (£M)', 'co-benefit_type': 'Type'})

st.plotly_chart(fig_bar, use_container_width=True)
