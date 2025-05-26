import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time

st.set_page_config(page_title="Water Quality Dashboard", layout="wide")

PRIMARY_GREEN = "#2E5E4E"
WATER_BLUE = "#66B2FF"
ALERT_ORANGE = "#FFD580"
ALERT_RED = "#FF6B6B"
BACKGROUND = "#F9FAF9"
TEXT_DARK = "#1E1E1E"

st.markdown(f"""
    <style>
        body {{
            background-color: {BACKGROUND};
            color: {TEXT_DARK};
        }}
        .stButton > button {{
            color: white;
            background-color: {PRIMARY_GREEN};
            border-radius: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

role = st.radio("Select Role:", ["Technician", "Viewer"], horizontal=True)

def simulate_sensor_data():
    now = pd.Timestamp.now()
    timestamps = pd.date_range(end=now, periods=20, freq="min")
    data = pd.DataFrame({
        "timestamp": timestamps,
        "pH": np.random.normal(7.2, 0.2, size=20),
        "temperature": np.random.normal(25, 1.5, size=20),
        "DO": np.random.normal(6.5, 0.5, size=20),
        "conductivity": np.random.normal(300, 50, size=20),
        "turbidity": np.random.normal(2.0, 0.5, size=20)
    })
    return data

df = simulate_sensor_data()
latest = df.iloc[-1]

st.title("💧 Water Quality Monitoring Dashboard")

st.markdown("### 📊 Current Sensor Readings")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("pH", f"{latest['pH']:.2f}")
col2.metric("Temperature (°C)", f"{latest['temperature']:.1f}")
col3.metric("Dissolved Oxygen (mg/L)", f"{latest['DO']:.2f}")
col4.metric("Conductivity (µS/cm)", f"{latest['conductivity']:.0f}")
col5.metric("Turbidity (NTU)", f"{latest['turbidity']:.2f}")

def check_alerts(row):
    alerts = []
    if row["pH"] < 6.5 or row["pH"] > 8.5:
        alerts.append(f"pH out of range: {row['pH']:.2f}")
    if row["temperature"] > 30:
        alerts.append(f"High temperature: {row['temperature']:.1f} °C")
    if row["DO"] < 5:
        alerts.append(f"Low dissolved oxygen: {row['DO']:.2f} mg/L")
    if row["conductivity"] > 500:
        alerts.append(f"High conductivity: {row['conductivity']:.0f} µS/cm")
    if row["turbidity"] > 5:
        alerts.append(f"High turbidity: {row['turbidity']:.2f} NTU")
    return alerts

alerts = check_alerts(latest)
if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("All parameters are within acceptable ranges.")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["pH", "Temperature", "DO", "Conductivity", "Turbidity"])

def plot_line(data, col, color):
    fig, ax = plt.subplots()
    ax.plot(data["timestamp"], data[col], color=color, marker="o")
    ax.set_title(col)
    ax.set_xlabel("Time")
    ax.set_ylabel(col)
    plt.xticks(rotation=45)
    st.pyplot(fig)

location_data = pd.DataFrame({
    "Location": ["Site A", "Site B", "Site C"],
    "Status": ["🟢 Active", "🔴 Inactive", "🟢 Active"]
})
st.dataframe(location_data, use_container_width=True)

if role == "Viewer":
    st.warning("Viewer access: Read-only mode. You cannot update or control devices.")
else:
    st.success("Technician mode: Full access enabled.")

# Simulated historical data
data = pd.DataFrame({
    "Time": pd.date_range(start="2025-01-01", periods=10, freq="D"),
    "pH": np.random.uniform(6.5, 8.5, 10),
    "Temperature": np.random.uniform(20, 30, 10),
    "DO": np.random.uniform(5, 9, 10),
    "Conductivity": np.random.uniform(300, 500, 10),
    "Turbidity": np.random.uniform(1, 5, 10)
})

# SESSION STATE for editable data
if "data" not in st.session_state:
    st.session_state.data = data.copy()

# Role selection
st.sidebar.title("User Role")
role = st.sidebar.radio("Select your role:", ["Viewer", "Technician"])

# Technician authentication
if role == "Technician":
    password = st.sidebar.text_input("Enter technician password:", type="password")
    if password != "admin123":
        st.warning("Incorrect password. Viewer access only.")
        role = "Viewer"
    else:
        st.success("Technician access granted!")

# Parameter selection
parameter = st.sidebar.radio("Choose a parameter to view/edit", ["Dashboard", "pH", "Temperature", "DO", "Conductivity", "Turbidity"])

# Main View
st.title("🌊 Water Quality Monitoring Dashboard")

# Technician can edit
if role == "Technician":
    st.subheader("Edit Sensor Data")
    updated_data = st.data_editor(st.session_state.data, use_container_width=True, num_rows="dynamic")
    st.session_state.data = updated_data

# Viewer can only see
else:
    st.subheader("View Sensor Data")
    st.dataframe(st.session_state.data, use_container_width=True)

# Parameter display logic
if parameter == "Dashboard":
    st.line_chart(st.session_state.data.set_index("Time"))
else:
    st.line_chart(
        st.session_state.data.set_index("Time")[[parameter]],
        use_container_width=True
    )

# Default role is Viewer
st.sidebar.title("User Login")
input_role = st.sidebar.radio("Select role (default is Viewer):", ["Viewer", "Technician"])
role = "Viewer"  # Default

# Handle Technician access
if input_role == "Technician":
    password = st.sidebar.text_input("Enter Technician Password:", type="password")
    if password == "admin123":
        st.success("Technician access granted!")
        role = "Technician"
    else:
        st.warning("Incorrect password. You are in Viewer mode.")
else:
    st.info("You are in Viewer mode.")

if role == "Technician":
    print("Technician mode activated.")
else:
    print("Viewer mode activated.")
