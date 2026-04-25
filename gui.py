import streamlit as st
import pandas as pd
import numpy as np
import time
import joblib


xgb_model = joblib.load('sleep_health_model.pkl')
scaler = joblib.load('scaler.pkl')
le = joblib.load('encoder_occupation.pkl')
le_target = joblib.load('encoder_target.pkl')

# =========================================
# Page Config
# =========================================
st.set_page_config(page_title="Sleep Health AI", page_icon="💤", layout="wide")

# =========================================
# CSS (Beige Theme)
# =========================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F5F5DC, #D2B48C, #A98467);
    color: #4E342E; 
}

.premium-card {
    background: rgba(255, 255, 255, 0.5);
    border-radius: 20px;
    padding: 25px; 
    margin-bottom: 20px;
    display: block; 
    width: 100%;
}

.premium-h1 {
    text-align: center;
    font-size: 4rem; 
    font-weight: 900;
    color: #3E2723 !important; 
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1); 
    margin-bottom: 30px;
}

h1, h2, h3, h4, h5 {
    color: #4E342E !important;        
    font-weight: 700 !important;
}

label p {
    font-size: 1rem !important; 
    font-weight: 700 !important;
    color: #3E2723 !important;
}

input, div[data-baseweb="select"] {
    font-size: 0.8rem !important;
}

.stCheckbox label p {
    font-size: 1rem !important;
}

button[step] {
    transform: scale(1.3);
}

.stButton>button {
    background-color: #6D4C41; 
    color: #ffffff;
    font-weight: bold;
    padding: 15px 30px;
    border-radius: 12px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    background-color: #4E342E; 
    transform: scale(1.02);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.stSlider > div > div > div {
    background: #6D4C41 !important; 
}

.stSlider > div > div > div > div > div {
    background-color: #ffffff !important;
    border: 2px solid #3E2723 !important; 
}

</style>
""", unsafe_allow_html=True)

# =========================================
# Header
# =========================================
st.markdown('<h1 class="premium-h1">💤 Sleep Health Analyzer</h1>', unsafe_allow_html=True)

# =========================================
# Inputs
# =========================================
col1, col2= st.columns(2)

with col1:
    st.write("### 👤 Personal Info")
    name = st.text_input("Your Name")
    age = st.number_input("Age", min_value=10, max_value=80, value=18)
    height = st.number_input("Height (cm)", 100, 220, 170)
    weight = st.number_input("Weight (kg)", 30, 150, 70)
    occupation = st.selectbox("Occupation", [
            "Software Engineer", "Student", "Nurse", "Manager", 
            "Doctor", "Teacher", "Lawyer", "Sales", "Retired", 
            "Driver", "Freelancer", "Homemaker", "Others"
        ])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.write("### Sleep Metrics")
    duration = st.number_input("Sleep Duration (hrs)", min_value=1.0, max_value=12.0, value=7.0, step=0.5)
    latency = st.number_input("Sleep Latency (mins)", min_value=0, max_value=120, value=15)
    quality = st.number_input("Sleep Quality", min_value=1, max_value=10, value=7)
    wake_episodes = st.number_input("Wake Episodes", min_value=0, max_value=10, value=2)
    deep = st.number_input("Deep Sleep %",min_value=0, max_value=50, value=15)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
st.markdown("---") 
st.subheader("Lifestyle & Habits")
l_col1, l_col2 = st.columns(2)

with l_col1:
    work_hours = st.number_input("Work Hours Today", min_value=0, max_value=20, value=7)
    stress = st.number_input("Stress Score", min_value=0, max_value=10, value=5)
    screen_time = st.number_input("Screen Time Before Bed (mins)", min_value=0, max_value=300, value=30)
    nap = st.number_input("Nap Duration (mins)", min_value=0, max_value=180, value=50)
    mental = st.selectbox("Menatel Health", ['Healthy', 'Anxiety', 'Depression', 'Both'])
    st.markdown('</div>', unsafe_allow_html=True)

with l_col2:
    day_choice = st.segmented_control("Day Type", options=["Weekday", "Weekend"], default="Weekday")
    day = 1 if day_choice == "Weekday" else 0

    shift_choice = st.segmented_control("Shift Work?", options=["Yes", "No"], default="No")
    shift_work = 1 if shift_choice == "Yes" else 0
    
    caffeine_choice = st.segmented_control("Consumed Caffeine before bed?", options=["Yes", "No"], default="No")
    is_caffeine = 1 if caffeine_choice == "Yes" else 0
    
    alcohol_choice = st.segmented_control("Consumed Alcohol before bed?", options=["Yes", "No"], default="No")
    is_alcohol = 1 if alcohol_choice == "Yes" else 0
    
    aid_choice = st.segmented_control("Used Sleep Aid?", options=["Yes", "No"], default="No")
    sleep_aid = 1 if aid_choice == "Yes" else 0
    
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================
# Process data
# =========================================
bmi = weight / ((height / 100) ** 2)

data = {
    "age": age,
    "occupation": occupation,
    "bmi": bmi,
    "sleep_duration_hrs": duration,
    "sleep_quality_score": quality,
    "rem_percentage": 10,
    "deep_sleep_percentage": deep,
    "sleep_latency_mins": latency,
    "wake_episodes_per_night": wake_episodes,
    "screen_time_before_bed_mins": screen_time,
    "nap_duration_mins": nap,
    "stress_score": stress,
    "work_hours_that_day": work_hours,
    "mental_health_condition": mental,
    "sleep_aid_used": int(sleep_aid),
    "shift_work": int(shift_work),
    "day_type": day,
    "is_caffeine_consumed": int(is_caffeine),
    "is_alcohol_consumed": int(is_alcohol),
}

df = pd.DataFrame([data])

scaling_cols = [
    'age', 'bmi', 'sleep_duration_hrs', 'sleep_quality_score', 'deep_sleep_percentage','sleep_latency_mins', 'screen_time_before_bed_mins',
    'nap_duration_mins', 'stress_score', 'work_hours_that_day'
]
mental_health_mapping = {
    'Healthy': 0,
    'Anxiety': 1,
    'Depression': 2,
    'Both': 3
}
df[scaling_cols] = scaler.transform(df[scaling_cols])
df['occupation'] = le.transform(df['occupation'])
df['mental_health_condition'] = df['mental_health_condition'].map(mental_health_mapping)

# =========================================
# Prediction Button
# =========================================
if st.button("🚀 Predict Sleep Quality"):

    with st.spinner("Analyzing..."):
        time.sleep(1)
    prediction = xgb_model.predict(df)
    final_result = le_target.inverse_transform(prediction)[0]
    st.write(f"Based on your data, the sleep status is: **{final_result}**")

# Footer
st.markdown("---")
st.markdown("Sleep Health App © 2026")