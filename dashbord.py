import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# 🔁 Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

st.set_page_config(page_title="Live Sales Dashboard", layout="wide")
st.title("📊 Live Sales Dashboard")

# --- PostgreSQL Connection (SAFE TEST) ---
try:
    engine = create_engine(
        "postgresql+psycopg2://postgres:PASSWORD@localhost:5432/SALES_DASHBOARD"
    )
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
except Exception as e:
    st.error(f"❌ Database connection failed:\n{e}")
    st.stop()

st.success("✅ Database connected")

# --- Load Data ---
@st.cache_data(ttl=3)
def load_data():
    query = """
        SELECT region, product, quantity, total_sales, sale_time
        FROM sales_data
        ORDER BY sale_time DESC
        LIMIT 100;
    """
    return pd.read_sql(query, engine)

df = load_data()

if df.empty:
    st.warning("⚠️ No data yet. Simulator may not be running.")
    st.stop()

# --- KPIs ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales ₹", round(df["total_sales"].sum(), 2))
col2.metric("Total Orders", len(df))
col3.metric("Avg Sale ₹", round(df["total_sales"].mean(), 2))

# --- Table ---
st.subheader("🧾 Recent Sales")
st.dataframe(df, use_container_width=True)

# --- Charts ---
st.subheader("📦 Sales by Product")
fig1 = px.bar(df, x="product", y="total_sales", color="region")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🌍 Sales by Region")
region_data = df.groupby("region", as_index=False)["total_sales"].sum()
fig2 = px.pie(region_data, values="total_sales", names="region")
st.plotly_chart(fig2, use_container_width=True)

st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
