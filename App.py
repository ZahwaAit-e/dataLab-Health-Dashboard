import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(page_title = "Heart Health & Net Zero", layout ="wide")

@st.cache_data
def load_and_merge():
    l3 = pd.read_excel("Level_3.xlsx")
    lk = pd.read_excel("lookups.xlsx")
    return pd.merge (l3,lk, on= 'small_area')
df = load_and_merge()
    # 3. Sidebar Filters
st.sidebar.header("Dashboard Filters")
selected_region = st.sidebar.selectbox("Select a Region", df['local_authority'].unique())
# 4. Main Title

st.markdown(f"Exploring co-benefits in **{selected_region}** (2025-2050)")
# 5. Top Level Metrics (KPIs)
# Filter data based on selection
region_df = df[df['local_authority'] == selected_region]
total_benefit = region_df['sum'].sum()

col1, col2 = st.columns(2)
col1.metric("Total Regional Benefit", f"£{total_benefit:,.0f}M", "+12% vs 2025")
col2.metric("Primary Benefit", "Reduced Mortality")

# 6. Simple Chart (Example: Benefit by Pathway)
fig = px.bar(region_df, x='damage_pathway', y='sum', color='co-benefit_type',
             title=f"Economic Benefit Distribution in {selected_region}", labels ={'sum': 'Benefit (£Million)', 'damage_pathway': 'Health Pathway'})

st.plotly_chart(fig, width='stretch')