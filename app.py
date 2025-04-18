import streamlit as st
import pandas as pd
import numpy as np
import glob
import os
from datetime import date

# Setup
st.set_page_config(layout="wide")
st.title("Penfolds Predictions")

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🎯 Boost Your Edge with NBA Player Probabilities")

with col2:
    st.markdown("Last update: Apr 14, 2025")

# Load latest file from directory
directory = r"D:\streamlit_ingest\final_merged_df"
csv_files = glob.glob(os.path.join(directory, "*.csv"))
latest_file = max(csv_files, key=os.path.getmtime)
df = pd.read_csv(latest_file)

# Only keep relevant columns
df = df[['Player', 'team', 'PTS', 'AST', 'REB', 'recentgames_PTS', 'recentgames_AST', 'recentgames_REB']]
df = df.sort_values(by=["team", "Player"], ascending=[True, True])

# Confidence level
confidence_level = 0.95
z_score = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}[confidence_level]

# Player selectbox
player_name = st.selectbox("Search or Select a Player", df['Player'].unique())

# Create tabs
tabs = st.tabs(["📊 Points (PTS)",  "💪 Rebounds (REB)", "🎯 Assists (AST)"])

# Load matchup data
directory_matchup = r"D:\streamlit_ingest\matchup_PTS"
csv_files_matchup = glob.glob(os.path.join(directory_matchup, "*.csv"))
latest_file_matchup = max(csv_files_matchup, key=os.path.getmtime)
df_matchup = pd.read_csv(latest_file_matchup)

split_columns = df_matchup['Matchup'].str.split(' vs ', expand=True)
split_columns = split_columns.fillna('Missing')
df_matchup[['Team_name_1', 'Team_name_2']] = split_columns

# Get player's team
player_team = df[df['Player'] == player_name]['team'].values[0]
matchup_row = df_matchup[(df_matchup['Team_name_1'] == player_team) | (df_matchup['Team_name_2'] == player_team)]
other_team = (
    matchup_row.iloc[0]['Team_name_2'] if matchup_row.iloc[0]['Team_name_1'] == player_team 
    else matchup_row.iloc[0]['Team_name_1']
) if not matchup_row.empty else "Unknown"

# Define a function to display each stat tab
def display_stat_tab(stat_label, stat_col, recent_col):
    threshold = st.number_input(f"Enter Threshold for {stat_label}", value=20)

    player_row = df[df['Player'] == player_name]
    if not player_row.empty:
        prediction_str = player_row[stat_col].values[0]  # Format: "18 - 24 - 30"

        try:
            low_str, mean_str, high_str = prediction_str.split(" - ")
            low = float(low_str)
            mean = float(mean_str)
            high = float(high_str)

            # Check for NaNs
            if np.isnan(low) or np.isnan(mean) or np.isnan(high):
                st.warning("⚠️ Not enough data for this player.")
                return

            if threshold < 0:
                st.warning("Please enter a valid threshold above 0.")
                return

            std_estimate = (high - low) / (2 * z_score)
            simulated_outcomes = np.random.normal(loc=mean, scale=std_estimate, size=100000)
            prob_over_threshold = np.mean(simulated_outcomes >= threshold)

            # Display results
            st.subheader("🎯 Probability Meter")
            st.metric(
                label=f"Probability {player_name} gets ≥ {threshold} {stat_label} against {other_team}",
                value=f"{prob_over_threshold:.1%}"
            )
            st.progress(prob_over_threshold)

            st.markdown(f"""
            **What does this mean?**

            Out of **100,000 simulations** of what {player_name} might get:

            > **{int(prob_over_threshold * 100000):,}** were **{threshold} or more**.

            That means there's about a **{prob_over_threshold:.2%} chance** they hit that number and more.

            _(Confidence level: {int(confidence_level * 100)}%)_
            """)

            # Show recent games
            st.subheader("📈 Recent Games")
            recent_games_str = player_row[recent_col].values[0]
            st.text(f"{player_name} - {player_row['team'].values[0]}: {recent_games_str}")

        except Exception as e:
            st.warning("Prediction format invalid. Must be like '18 - 24 - 30 if it is not enough data for prediction'")
    else:
        st.warning("Player not found.")

# Render each tab
with tabs[0]:
    display_stat_tab("PTS", "PTS", "recentgames_PTS")

with tabs[2]:
    display_stat_tab("AST", "AST", "recentgames_AST")

with tabs[1]:
    display_stat_tab("REB", "REB", "recentgames_REB")
