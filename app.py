import streamlit as st
import pickle
import pandas as pd
import base64

# Set page config
st.set_page_config(page_title="IPL Win Predictor", layout="wide", page_icon="🏏")

# Load model
pipe = pickle.load(open("Final_Pipeline.pkl", "rb"))

# Teams & Logos
# Teams & Logos (Relative Paths for Cloud Compatibility)
team_logos = {
    'Chennai Super Kings': 'Logos/CSK.png',
    'Delhi Capitals': 'Logos/DC.jpeg',
    'Kings XI Punjab': 'Logos/KXIP.png',
    'Kolkata Knight Riders': 'Logos/KKR.jpeg',
    'Mumbai Indians': 'Logos/MI.jpeg',
    'Rajasthan Royals': 'Logos/RR.png',
    'Royal Challengers Bangalore': 'Logos/RCB.jpeg',
    'Sunrisers Hyderabad': 'Logos/SRH.jpeg'
}

teams = list(team_logos.keys())

cities = sorted([
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur',
    'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London',
    'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur',
    'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah',
    'Mohali', 'Bengaluru'
])

# Custom CSS for aesthetics
st.markdown("""
    <style>
    .logo-card {
    background-color: #ffffff10;
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    margin-bottom: 1rem;
    }
    .logo-card img {
    border-radius: 8px;
    }
            
    .main {
        background-color: #f7f9fb;
    }
    .stButton > button {
        background-color: #00aaff;
        color: white;
        font-size: 16px;
        padding: 8px 20px;
        border-radius: 8px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #007acc;
    }
    .block-container {
        padding-top: 2rem;
    }
    .input-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .logo {
        height: 60px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='color:#1f77b4;'>🏏 IPL Win Probability Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p>Predict your team's chances based on live match inputs</p>", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("Match Setup ⚙️")

batting_team = st.sidebar.selectbox("🏏 Batting Team", teams)
bowling_team = st.sidebar.selectbox("🎯 Bowling Team", [team for team in teams if team != batting_team])
city = st.sidebar.selectbox("📍 Match City", cities)

target = st.sidebar.number_input("🎯 Target Score", min_value=1)
score = st.sidebar.number_input("📊 Current Score", min_value=0)
overs = st.sidebar.number_input("⏱️ Overs Completed", min_value=0.0, max_value=20.0, step=0.1)
wickets = st.sidebar.number_input("🚨 Wickets Lost", min_value=0, max_value=10)

# Display team logos side by side
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.image(team_logos[batting_team], width=100)
        st.markdown(f"#### 🏏 Batting:\n{batting_team}")

with col2:
    with st.container():
        st.image(team_logos[bowling_team], width=100)
        st.markdown(f"#### 🎯 Bowling:\n{bowling_team}")


# Predict button
if st.sidebar.button("🔮 Predict"):
    runs_left = int(target - score)
    balls_left = int(120 - (overs * 6))
    wickets_left = int(10 - wickets)
    crr = round(score / overs, 2) if overs > 0 else 0
    rrr = round((runs_left * 6) / balls_left, 2) if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'Batting Team': [batting_team],
        'Bowling Team': [bowling_team],
        'City': [city],
        'Runs Left': [runs_left],
        'Balls Left': [balls_left],
        'Wickets Left': [wickets_left],
        'Target': [target],
        'CRR': [crr],
        'RRR': [rrr]
    })

    st.markdown("## 📋 Match Summary")
    st.table(input_df)

    try:
        prediction = pipe.predict_proba(input_df)
        win_prob = prediction[0][1]
        lose_prob = prediction[0][0]

        st.markdown("## 📈 Predicted Winning Probability")

        # Visual progress bar
        st.progress(win_prob)
        st.success(f"🏆 Win Probability: **{win_prob * 100:.2f}%**")
        st.warning(f"❌ Lose Probability: **{lose_prob * 100:.2f}%**")

    except Exception as e:
        st.error(f"⚠️ An error occurred during prediction: {e}")
