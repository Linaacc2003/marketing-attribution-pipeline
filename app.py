import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Marketing Attribution & ROI Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom UI styling
st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        div.stMetric {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
        }
        div.stMetric label { color: #64748b !important; font-weight: 600 !important; }
        div.stMetric [data-testid="stMetricValue"] { color: #0f172a !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🎯 Multi-Channel Marketing Attribution & ROI Dashboard")
st.markdown("Analyzing ad spend efficiency, customer acquisition cost (CAC), and return on ad spend (ROAS) across acquisition channels.")
st.markdown("---")

# Load data from SQLite database
@st.cache_data
def load_data():
    conn = sqlite3.connect('marketing_data.db')
    df_channel = pd.read_sql('SELECT * FROM channel_performance', conn)
    df_conversions = pd.read_sql('SELECT * FROM raw_conversions', conn)
    conn.close()
    return df_channel, df_conversions

df_channel, df_conversions = load_data()

# --- TOP EXECUTIVE METRICS ---
total_spend = df_channel['Ad_Spend'].sum()
total_revenue = df_channel['Total_Revenue'].sum()
total_conversions = df_channel['Total_Conversions'].sum()
blended_roas = round(total_revenue / total_spend, 2) if total_spend > 0 else 0
blended_cac = round(total_spend / total_conversions, 2) if total_conversions > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Ad Spend", f"${total_spend:,.2f}")
col2.metric("Total Revenue Generated", f"${total_revenue:,.2f}")
col3.metric("Blended ROAS", f"{blended_roas}x", delta="Target > 2.0x")
col4.metric("Blended CAC", f"${blended_cac:,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# --- CHARTS SECTION ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Return on Ad Spend (ROAS) by Channel")
    fig_roas = px.bar(
        df_channel, x='Channel', y='ROAS',
        color='Channel',
        text='ROAS',
        color_discrete_map={'Email Marketing': '#10b981', 'Google Ads': '#2563eb', 'Meta Ads': '#f59e0b', 'LinkedIn Ads': '#64748b'},
        template="plotly_white"
    )
    fig_roas.update_traces(texttemplate='%{text}x', textposition='outside')
    fig_roas.update_layout(yaxis_title="ROAS Multiplier", showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_roas, use_container_width=True)

with col_right:
    st.subheader("💰 Ad Spend vs. Revenue Generated")
    df_melted = df_channel.melt(id_vars=['Channel'], value_vars=['Ad_Spend', 'Total_Revenue'], var_name='Metric', value_name='Amount ($)')
    fig_spend_rev = px.bar(
        df_melted, x='Channel', y='Amount ($)', color='Metric',
        barmode='group',
        color_discrete_map={'Ad_Spend': '#cbd5e1', 'Total_Revenue': '#2563eb'},
        template="plotly_white"
    )
    fig_spend_rev.update_layout(yaxis_title="USD ($)", margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_spend_rev, use_container_width=True)

st.markdown("---")

# --- DETAILED TABLE ---
st.subheader("📋 Channel Unit Economics Breakdown")
st.dataframe(df_channel.style.format({
    'Ad_Spend': '${:,.2f}',
    'Total_Revenue': '${:,.2f}',
    'CAC': '${:,.2f}',
    'ROAS': '{:.2f}x'
}), use_container_width=True)