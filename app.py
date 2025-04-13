# import streamlit as st
# import pandas as pd
# import numpy as np
# import glob
# import os

# # Setup
# st.set_page_config(layout="wide")
# st.title("NBA Streamlit App")
# st.subheader("🎯 Player Threshold Probability Calculator")

# # Load latest file from directory
# directory = r"D:\streamlit_ingest\final_merged_df"
# csv_files = glob.glob(os.path.join(directory, "*.csv"))
# latest_file = max(csv_files, key=os.path.getmtime)
# df = pd.read_csv(latest_file)

# # Only keep relevant columns
# df = df[['Player', 'team', 'PTS', 'AST', 'REB', 'recentgames_PTS', 'recentgames_AST', 'recentgames_REB']]
# df = df.sort_values(by=["team", "Player"], ascending=[True, True])

# # Dropdown to select player
# player_name = st.selectbox("Select Player", df['Player'].unique())

# # Create tabs
# tabs = st.tabs(["📊 Points (PTS)",  "💪 Rebounds (REB)", "🎯 Assists (AST)"])

# # Define a function for repeated logic
# def display_stat_tab(stat_label, stat_col, recent_col):
#     threshold = st.number_input(f"Enter Threshold for {stat_label}", value=20)

#     player_row = df[df['Player'] == player_name]
#     if not player_row.empty:
#         prediction_str = player_row[stat_col].values[0]  # Format: "18 - 24 - 30"

#         try:
#             low_str, mean_str, high_str = prediction_str.split(" - ")
#             low = int(low_str)
#             mean = int(mean_str)
#             high = int(high_str)

#             if threshold < 0:
#                 st.warning("Please enter a valid threshold above 0.")
#                 return

#             std_estimate = (high - low) / 2
#             simulated_outcomes = np.random.normal(loc=mean, scale=std_estimate, size=100000)
#             prob_over_threshold = np.mean(simulated_outcomes >= threshold)

#             st.subheader("🎯 Probability Meter")
#             st.metric(
#                 label=f"Probability {player_name} gets ≥ {threshold} {stat_label}",
#                 value=f"{prob_over_threshold:.1%}"
#             )
#             st.progress(prob_over_threshold)

#             st.markdown(f"""
#             **What does this mean?**

#             Out of **100,000 simulations** of what {player_name} might get:

#             > **{int(prob_over_threshold * 100000):,}** were **{threshold} or more**.

#             That means there's about a **{prob_over_threshold:.2%} chance** they hit that number or more.
#             """)

#             st.subheader("📈 Recent Games")
#             recent_games_str = player_row[recent_col].values[0]
#             st.text(f"{player_name} - {player_row['team'].values[0]}: {recent_games_str}")

#         except:
#             st.warning("Prediction format invalid. Must be like '18 - 24 - 30'")
#     else:
#         st.warning("Player not found.")

# # Use each tab
# with tabs[0]:
#     display_stat_tab("PTS", "PTS", "recentgames_PTS")

# with tabs[2]:
#     display_stat_tab("AST", "AST", "recentgames_AST")

# with tabs[1]:
#     display_stat_tab("REB", "REB", "recentgames_REB")


import streamlit as st
import pandas as pd
import numpy as np
import glob
import os

# Setup
st.set_page_config(layout="wide")
st.title("Penfolds Predictions")
st.subheader("🎯 Boost Your Edge with NBA Player Probabilities")

# Load latest file from directory
directory = r"D:\streamlit_ingest\final_merged_df"
csv_files = glob.glob(os.path.join(directory, "*.csv"))
latest_file = max(csv_files, key=os.path.getmtime)
df = pd.read_csv(latest_file)

# Only keep relevant columns
df = df[['Player', 'team', 'PTS', 'AST', 'REB', 'recentgames_PTS', 'recentgames_AST', 'recentgames_REB']]
df = df.sort_values(by=["team", "Player"], ascending=[True, True])

# You control the confidence level here (users can't change it)
confidence_level = 0.95
z_score = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}[confidence_level]

# Dropdown to select player
player_name = st.selectbox("Select Player", df['Player'].unique())

# Create tabs
tabs = st.tabs(["📊 Points (PTS)",  "💪 Rebounds (REB)", "🎯 Assists (AST)"])

# Define a function for repeated logic
def display_stat_tab(stat_label, stat_col, recent_col):
    threshold = st.number_input(f"Enter Threshold for {stat_label}", value=20)

    player_row = df[df['Player'] == player_name]
    if not player_row.empty:
        prediction_str = player_row[stat_col].values[0]  # Format: "18 - 24 - 30"

        try:
            low_str, mean_str, high_str = prediction_str.split(" - ")
            low = int(low_str)
            mean = int(mean_str)
            high = int(high_str)

            if threshold < 0:
                st.warning("Please enter a valid threshold above 0.")
                return

            # Estimate standard deviation using z-score
            std_estimate = (high - low) / (2 * z_score)

            # Simulate outcomes
            simulated_outcomes = np.random.normal(loc=mean, scale=std_estimate, size=100000)
            prob_over_threshold = np.mean(simulated_outcomes >= threshold)

            # Display result
            st.subheader("🎯 Probability Meter")
            st.metric(
                label=f"Probability {player_name} gets ≥ {threshold} {stat_label}",
                value=f"{prob_over_threshold:.1%}"
            )
            st.progress(prob_over_threshold)

            st.markdown(f"""
            **What does this mean?**

            Out of **100,000 simulations** of what {player_name} might get:

            > **{int(prob_over_threshold * 100000):,}** were **{threshold} or more**.

            That means there's about a **{prob_over_threshold:.2%} chance** they hit that number or more.

            _(Confidence level: {int(confidence_level * 100)}%)_
            """)

            # Show recent games
            st.subheader("📈 Recent Games")
            recent_games_str = player_row[recent_col].values[0]
            st.text(f"{player_name} - {player_row['team'].values[0]}: {recent_games_str}")

        except:
            st.warning("Prediction format invalid. Must be like '18 - 24 - 30'")
    else:
        st.warning("Player not found.")

# Use each tab
with tabs[0]:
    display_stat_tab("PTS", "PTS", "recentgames_PTS")

with tabs[2]:
    display_stat_tab("AST", "AST", "recentgames_AST")

with tabs[1]:
    display_stat_tab("REB", "REB", "recentgames_REB")





