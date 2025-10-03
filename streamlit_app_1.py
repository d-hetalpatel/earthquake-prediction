# ===============================
# STREAMLIT EARTHQUAKE DASHBOARD
# ===============================
import streamlit as st
import pandas as pd
import numpy as np
import requests
import pydeck as pdk
import plotly.express as px
import pickle
import gzip
from datetime import datetime
import os
import gdown 

# === PAGE CONFIG ===
st.set_page_config(page_title="Earthquake Monitoring Dashboard", layout="wide")
st.title("🌍 Real-Time Earthquake Monitoring & Alert System")

# === SIDEBAR CONTROLS ===
st.sidebar.header("Filters & Alerts")
mag_threshold = st.sidebar.slider("Magnitude Alert Threshold", 3.0, 8.0, 5.0, 0.1)
aftershock_threshold = st.sidebar.slider("Aftershock Probability Threshold", 0.0, 1.0, 0.6, 0.05)
region_filter = st.sidebar.text_input("Region Filter (optional, e.g., California)")
time_window = st.sidebar.selectbox("Time Window", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])
send_webhook = st.sidebar.checkbox("Send Webhook Alerts (Optional)", value=False)

# === LOAD TRAINED MODELS ===
drive_url = "https://drive.google.com/file/d/1kaMuXbIK71zOWu0REDEIVQGC8EL4aLXL"
pickle_path = r"earthquake_models_and_data.pkl.gz"
# Download the file if it doesn't exist locally
if not os.path.exists(pickle_path):
    st.info("Downloading model from Google Drive...")
    gdown.download(drive_url, pickle_path, quiet=False)
#r = requests.get(url)

if os.path.exists(pickle_path):
    with gzip.open(pickle_path, "rb") as f:
        data = pickle.load(f)
    reg_model = data["regression_model"]
    cls_model = data["classification_model"]
    required_features = data["labeled_df"].columns.tolist()
    st.success(f"✅ Pickle file loaded from {pickle_path}")
else:
    st.error(f"❌ Pickle file not found at {pickle_path}")
    st.stop()

# === FETCH LIVE USGS DATA ===
def fetch_usgs_data(time_window):
    url_map = {
        "Last 24 Hours": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
        "Last 7 Days": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson",
        "Last 30 Days": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"
    }
    url = url_map[time_window]
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"Failed to fetch USGS data: {e}")
        st.stop()
    records = []
    for f in data.get("features", []):
        coords = f.get("geometry", {}).get("coordinates", [None, None, None])
        props = f.get("properties", {})
        record = {
            "latitude": coords[1] if len(coords) > 1 else np.nan,
            "longitude": coords[0] if len(coords) > 0 else np.nan,
            "depth": coords[2] if len(coords) > 2 else np.nan,
            "mag": props.get("mag", np.nan),
            "time": pd.to_datetime(props.get("time", None), unit='ms', errors='coerce'),
            "place": props.get("place", "Unknown"),
            "magType": props.get("magType", ""),
            "nst": props.get("nst", 0),
            "gap": props.get("gap", np.nan),
            "dmin": props.get("dmin", np.nan),
            "rms": props.get("rms", np.nan),
            "net": props.get("net", ""),
            "updated": pd.to_datetime(props.get("updated", None), unit='ms', errors='coerce'),
            "type": props.get("type", ""),
            "status": props.get("status", "")
        }
        records.append(record)
    df = pd.DataFrame(records)
    df.dropna(subset=["latitude", "longitude", "mag"], inplace=True)
    if df.empty:
        st.warning("No earthquake data available for the selected filter/time window.")
        st.stop()
    return df

df = fetch_usgs_data(time_window)

# --- Filter by region ---
if region_filter:
    df = df[df['place'].str.contains(region_filter, case=False)]

# === FEATURE ENGINEERING ===
df['is_weekend'] = df['time'].dt.weekday >= 5
df['season'] = df['time'].dt.month % 12 // 3 + 1
df['time_of_day'] = df['time'].dt.hour
df['depth_category'] = pd.cut(df['depth'], bins=[-1,10,30,70,300], labels=[0,1,2,3])
df['distance_to_fault_km'] = 0
df['region'] = df['place']
df['monthly_event_count'] = 0
df['rolling_mag_mean'] = df.groupby('place')['mag'].transform(lambda x: x.rolling(10, min_periods=1).mean())
df['rolling_mag_var'] = df.groupby('place')['mag'].transform(lambda x: x.rolling(10, min_periods=1).var())
df['history_score'] = df['rolling_mag_mean']
df['nearest_volcano_dist_km'] = 0
df['volcano_nearby'] = 0
df['dbscan_cluster'] = 0
df['label_aftershock'] = 0

# Fill missing features
for col in required_features:
    if col not in df.columns:
        df[col] = 0

# === PREDICTIONS ===
df['predicted_magnitude'] = reg_model.predict(df[required_features])
df['aftershock_prob'] = cls_model.predict_proba(df[required_features])[:,1]

# === ALERT SYSTEM ===
def alert_status(row):
    if row['predicted_magnitude'] >= mag_threshold or row['aftershock_prob'] >= aftershock_threshold:
        if row['predicted_magnitude'] >= mag_threshold + 1 or row['aftershock_prob'] >= aftershock_threshold + 0.2:
            return "High Risk ⚠️"
        return "Moderate Risk ⚠️"
    return "Low Risk ✅"

df['Alert_Status'] = df.apply(alert_status, axis=1)

# === WEBHOOK ALERT (OPTIONAL) ===
def send_webhook_alert(row):
    webhook_url = "YOUR_WEBHOOK_URL"
    payload = {
        "content": f"Alert! {row['place']} | Predicted Mag: {row['predicted_magnitude']:.2f} | Aftershock Prob: {row['aftershock_prob']:.2f} | {row['Alert_Status']}"
    }
    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        st.warning(f"Webhook failed: {e}")

if send_webhook:
    high_alerts = df[df['Alert_Status']=="High Risk ⚠️"]
    for _, row in high_alerts.iterrows():
        send_webhook_alert(row)

# === DASHBOARD KPIs ===
st.subheader("🌟 Alert Summary")
col1, col2, col3 = st.columns(3)
col1.metric("High Risk Alerts", df[df['Alert_Status']=="High Risk ⚠️"].shape[0])
col2.metric("Moderate Risk Alerts", df[df['Alert_Status']=="Moderate Risk ⚠️"].shape[0])
col3.metric("Low Risk Alerts", df[df['Alert_Status']=="Low Risk ✅"].shape[0])

# === PREDICTIONS TABLE ===
with st.expander("Predictions Table"):
    st.dataframe(df[['time','place','latitude','longitude','predicted_magnitude','aftershock_prob','Alert_Status']])

# === MAP VISUALIZATION ===
st.subheader("🌎 Seismic Hotspots Map")
def risk_color(row):
    if row['Alert_Status']=="High Risk ⚠️": return [255,0,0]
    elif row['Alert_Status']=="Moderate Risk ⚠️": return [255,255,0]
    return [0,255,0]

df['color'] = df.apply(risk_color, axis=1)

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_radius="predicted_magnitude * 20000",
    get_fill_color='color',
    pickable=True
)

heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_weight='predicted_magnitude',
    radius_pixels=50
)

view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=2
)

tooltip = {
    "html": "<b>Place:</b> {place} <br/>"
            "<b>Predicted Mag:</b> {predicted_magnitude:.2f} <br/>"
            "<b>Aftershock Prob:</b> {aftershock_prob:.2f} <br/>"
            "<b>Status:</b> {Alert_Status}",
    "style": {"color": "white"}
}

st.pydeck_chart(pdk.Deck(
    layers=[scatter_layer, heatmap_layer],
    initial_view_state=view_state,
    tooltip=tooltip
))

# === TREND CHARTS ===
st.subheader("📈 Predicted Magnitude Trend Over Time")
fig = px.line(df.sort_values("time"), x="time", y="predicted_magnitude", title="Predicted Magnitude Trend")
st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Aftershock Probability Distribution")
fig2 = px.histogram(df, x="aftershock_prob", nbins=20, title="Aftershock Probability")
st.plotly_chart(fig2, use_container_width=True)

# === DOWNLOAD PREDICTIONS ===
st.download_button(
    label="📥 Download Predictions as CSV",
    data=df.to_csv(index=False),
    file_name=f"earthquake_predictions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
    mime="text/csv"
)
