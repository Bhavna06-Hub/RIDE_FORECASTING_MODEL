import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# ----------------- SESSION STATE INIT (MUST BE FIRST) -----------------
st.session_state.setdefault("df", None)
st.session_state.setdefault("history", [])

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="OLA Ride Forecasting Dashboard",
    page_icon="🚖",
    layout="wide",
)

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
body { background-color: #f8fafc; }
.kpi {
    background: #16a34a;
    color: white;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ----------------- DEMAND MODEL -----------------
def estimate_base_demand(hour, temp, hum, season, weather, location, is_weekend):
    demand = 85

    if 7 <= hour <= 10:
        demand += 45
    if 17 <= hour <= 21:
        demand += 60
    if hour >= 23 or hour <= 4:
        demand += 30

    weather_factor = {
        "Clear": 0, "Cloudy": 5, "Rainy": 35, "Stormy": 50, "Foggy": 20
    }[weather]

    season_factor = {
        "Spring": 0, "Summer": 10, "Monsoon": 35, "Autumn": 5, "Winter": 20
    }[season]

    location_factor = {
        "Andheri": 5, "Bandra": 50, "Dadar": 15, "Ghatkopar": 40,
        "Thane": 45, "Borivali": 30, "Kurla": 35,
        "Vile Parle": 25, "Colaba": 20, "Mulund": 18
    }[location]

    demand += weather_factor + season_factor + location_factor
    demand += (temp - 25) * 1.1
    demand += (hum - 50) * 0.4

    if is_weekend:
        demand += 25

    return max(0, round(demand))


def generate_24h_forecast(start_dt, temp, hum, season, weather, location):
    rows = []
    is_weekend = start_dt.weekday() >= 5

    for i in range(24):
        dt = start_dt + timedelta(hours=i)
        val = estimate_base_demand(
            dt.hour, temp, hum, season, weather, location, is_weekend
        )
        rows.append({
            "Time": dt.strftime("%I %p"),
            "Predicted Rides": val
        })
    return pd.DataFrame(rows)

# ----------------- SIDEBAR -----------------
st.sidebar.title("🚖 OLA Ride Inputs")

location = st.sidebar.selectbox(
    "City",
    ["Andheri", "Bandra", "Dadar", "Ghatkopar", "Thane",
     "Borivali", "Kurla", "Vile Parle", "Colaba", "Mulund"]
)

selected_date = st.sidebar.date_input("Date", value=date.today())
hour_12 = st.sidebar.selectbox("Hour", list(range(1, 13)), index=8)
ampm = st.sidebar.selectbox("AM / PM", ["AM", "PM"])
hour = hour_12 % 12 + (12 if ampm == "PM" else 0)

temp = st.sidebar.slider("🌡 Temperature (°C)", 0, 45, 28)
hum = st.sidebar.slider("💧 Humidity (%)", 0, 100, 60)

season = st.sidebar.selectbox(
    "Season", ["Spring", "Summer", "Monsoon", "Autumn", "Winter"]
)

weather = st.sidebar.selectbox(
    "Weather", ["Clear", "Cloudy", "Rainy", "Stormy", "Foggy"]
)

# ----------------- HEADER -----------------
st.markdown("""
<div style="
background: linear-gradient(90deg,#16a34a,#22c55e);
padding:18px;
border-radius:16px;
color:white;">
<h1 style="margin:0">🚖 OLA Ride Forecasting Dashboard</h1>
<p style="margin:0;opacity:0.9">Smart city-wise ride demand prediction</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# ----------------- ACTION BUTTONS -----------------
b1, b2, b3 = st.columns([2,1,1])

with b1:
    predict = st.button("⚡ Predict Ride Demand", type="primary")

with b3:
    reset = st.button("🔄 Reset")

# ----------------- PREDICT LOGIC -----------------
if predict:
    start_dt = datetime.combine(selected_date, datetime.min.time()) + timedelta(hours=hour)
    is_weekend = start_dt.weekday() >= 5

    current_demand = estimate_base_demand(
        hour, temp, hum, season, weather, location, is_weekend
    )

    df = generate_24h_forecast(start_dt, temp, hum, season, weather, location)
    st.session_state["df"] = df

    # -------- SAVE TO HISTORY --------
    st.session_state["history"].append({
        "Date": selected_date.strftime("%d-%b-%Y"),
        "Time": f"{hour_12} {ampm}",
        "City": location,
        "Weather": weather,
        "Season": season,
        "Current Demand": current_demand,
        "Peak Demand": int(df["Predicted Rides"].max())
    })

    # ----------------- KPIs -----------------
    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"<div class='kpi'>🚕<br><b>{current_demand}</b><br>Current</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'>🔥<br><b>{df['Predicted Rides'].max()}</b><br>Peak</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi'>📊<br><b>{int(df['Predicted Rides'].mean())}</b><br>Average</div>", unsafe_allow_html=True)

    level = "Low" if current_demand < 120 else "Medium" if current_demand < 180 else "High"
    c4.markdown(f"<div class='kpi'>⚡<br><b>{level}</b><br>Demand</div>", unsafe_allow_html=True)

    st.markdown("### 📈 24-Hour Ride Forecast")
    st.line_chart(df.set_index("Time"))

    peak = df.loc[df["Predicted Rides"].idxmax()]
    st.success(f"🔥 Peak at **{peak['Time']}** → **{peak['Predicted Rides']} rides**")

    with st.expander("📋 View forecast data"):
        st.dataframe(df, use_container_width=True)

# ----------------- DOWNLOAD CSV -----------------
if st.session_state.get("df") is not None:
    csv = st.session_state["df"].to_csv(index=False).encode("utf-8")
    st.download_button(
    "📥 Download Forecast CSV",
    csv,
    f"ola_24h_{location}_forecast.csv",
    "text/csv"
    )

# ----------------- HISTORY BUTTON -----------------
show_history = st.button("📜 Show Prediction History")

if show_history:
    if st.session_state["history"]:
        st.markdown("### 📜 Prediction History")
        st.dataframe(pd.DataFrame(st.session_state["history"]), use_container_width=True)
    else:
        st.info("ℹ️ No prediction history yet")

# ----------------- RESET -----------------
if reset:
    st.session_state["df"] = None
    st.session_state["history"] = []
    st.rerun()
