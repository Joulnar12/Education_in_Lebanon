
# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ======================
# Page Configuration
# ======================
st.set_page_config(
    page_title="Education in Lebanon",
    page_icon="🎓",
    layout="wide"
)

st.title("Education Resources and Outcomes in Lebanon")
st.markdown(
    """
    This dashboard explores the relationship between **educational resources**
    (schools, universities, vocational institutes) and **education outcomes**
    (illiteracy, dropout rates) across Lebanon’s districts and governorates.
    """
)

# ======================
# Load Dataset
# ======================

@st.cache_data
def load_data():
    return pd.read_csv("/Users/joulnarabouchakra/Desktop/Visualisation - FZ/assignment_3/data/education_merged_final.csv", encoding="utf-8")

df = load_data()

# ======================
# Sidebar Controls
# ======================
st.sidebar.header("🔍 Filters")

# Select trend line metric
line_metric = st.sidebar.selectbox(
    "Select Trend Line Metric",
    ["Illiteracy", "SchoolDropout"]
)

# Select geographic filter
geo_filter_type = st.sidebar.radio(
    "Filter By",
    ["All", "Governorate", "District"]
)

# Dropdown for specific governorate/district if selected
if geo_filter_type != "All":
    geo_options = df[geo_filter_type].dropna().unique().tolist()
    selected_geo_value = st.sidebar.selectbox(f"Select {geo_filter_type}", geo_options)
else:
    selected_geo_value = None

# ======================
# Apply Filter
# ======================
if geo_filter_type != "All" and selected_geo_value:
    df_plot = df[df[geo_filter_type] == selected_geo_value]
else:
    df_plot = df.copy()

# ======================
# Aggregate by District
# ======================
df_agg = df_plot.groupby("District").agg({
    "PublicSchools": "sum",
    "PrivateSchools": "sum",
    "Universities": "sum",
    "VocationalInstitutes": "sum",
    "Illiteracy": "mean",
    "SchoolDropout": "mean",
    "Elementary": "mean",
    "Intermediate": "mean",
    "Secondary": "mean",
    "Vocational": "mean",
    "University": "mean",
    "HigherEducation": "mean"
}).reset_index()

# Calculate total resources
df_agg["TotalResources"] = (
    df_agg["PublicSchools"]
    + df_agg["PrivateSchools"]
    + df_agg["Universities"]
    + df_agg["VocationalInstitutes"]
)

# Sort by resources for better visuals
df_agg = df_agg.sort_values("TotalResources", ascending=False)

# ======================
# Visualization
# ======================
fig = go.Figure()

# Bar: total resources
fig.add_trace(go.Bar(
    x=df_agg["District"],
    y=df_agg["TotalResources"],
    name="Total Resources",
    marker_color="lightskyblue",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "Total Resources: %{y}<br>"
        "Elementary: %{customdata[0]:.1f}%<br>"
        "Intermediate: %{customdata[1]:.1f}%<br>"
        "Secondary: %{customdata[2]:.1f}%<br>"
        "Vocational: %{customdata[3]:.1f}%<br>"
        "University: %{customdata[4]:.1f}%<br>"
        "Higher Education: %{customdata[5]:.1f}%"
    ),
    customdata=df_agg[["Elementary", "Intermediate", "Secondary", "Vocational", "University", "HigherEducation"]].values
))

# Line: selected metric
fig.add_trace(go.Scatter(
    x=df_agg["District"],
    y=df_agg[line_metric],
    name=f"{line_metric} (%)",
    mode="lines+markers",
    marker_color="crimson",
    yaxis="y2"
))

# Layout
fig.update_layout(
    title=f"Educational Resources and {line_metric}",
    xaxis_tickangle=-45,
    yaxis=dict(title="Total Resources"),
    yaxis2=dict(title=f"{line_metric} (%)", overlaying="y", side="right"),
    legend=dict(orientation="h", y=-0.3),
    hovermode="x unified",
    height=600
)

# ======================
# Show Chart
# ======================
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

# ======================
# Aggregate for pie chart
# ======================
df_pie = df_plot.groupby(["Governorate", "District"]).agg({
    "PublicSchools": "sum",
    "PrivateSchools": "sum",
    "Universities": "sum",
    "VocationalInstitutes": "sum"
}).reset_index()

# If user selects a district, show only that
if geo_filter_type == "District" and selected_geo_value:
    df_pie = df_pie[df_pie["District"] == selected_geo_value]

# If user selects a governorate, show all districts together (aggregate at governorate level)
elif geo_filter_type == "Governorate" and selected_geo_value:
    df_pie = df_pie[df_pie["Governorate"] == selected_geo_value].groupby("Governorate").sum(numeric_only=True).reset_index()

# Otherwise, aggregate over all Lebanon
elif geo_filter_type == "All":
    df_pie = df_pie.sum(numeric_only=True).to_frame().T

# Reshape for pie chart
resource_totals = {
    "Public Schools": int(df_pie["PublicSchools"].sum()),
    "Private Schools": int(df_pie["PrivateSchools"].sum()),
    "Universities": int(df_pie["Universities"].sum()),
    "Vocational Institutes": int(df_pie["VocationalInstitutes"].sum())
}

labels = list(resource_totals.keys())
values = list(resource_totals.values())

# ======================
# Plot donut chart
# ======================
fig_pie = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    hole=0.5,  # makes it a donut
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}"
)])

fig_pie.update_layout(
    title="Educational Resource Distribution",
    legend=dict(orientation="h", y=-0.2),
    height=500
)

st.plotly_chart(fig_pie, use_container_width=True)

