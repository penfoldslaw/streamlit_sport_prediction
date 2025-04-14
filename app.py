
# import streamlit as st
# import pandas as pd
# import numpy as np
# import glob
# import os

# # Setup
# st.set_page_config(layout="wide")
# st.title("Penfolds Predictions")
# st.subheader("🎯 Boost Your Edge with NBA Player Probabilities")

# # Load latest file from directory
# # directory = r"D:\streamlit_ingest\final_merged_df"
# directory = "/home/ubuntu/aws_streamlit_ingest/streamlit_ingest/final_merged_df"
# csv_files = glob.glob(os.path.join(directory, "*.csv"))
# latest_file = max(csv_files, key=os.path.getmtime)
# df = pd.read_csv(latest_file)

# # Only keep relevant columns
# df = df[['Player', 'team', 'PTS', 'AST', 'REB', 'recentgames_PTS', 'recentgames_AST', 'recentgames_REB']]
# df = df.sort_values(by=["team", "Player"], ascending=[True, True])

# # You control the confidence level here (users can't change it)
# confidence_level = 0.95
# z_score = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}[confidence_level]

# # Dropdown to select player
# player_name = st.selectbox("Search or Select a Player", df['Player'].unique())

# # Create tabs
# tabs = st.tabs(["📊 Points (PTS)",  "💪 Rebounds (REB)", "🎯 Assists (AST)"])


# directory_matchup = "/home/ubuntu/aws_streamlit_ingest/streamlit_ingest/matchup_PTS"
# # Use glob to get all CSV files in the directory
# csv_files_matchup = glob.glob(os.path.join(directory_matchup, "*.csv"))
# # Sort the files by modification time (most recent first)
# latest_file_matchup = max(csv_files_matchup, key=os.path.getmtime)

# df_matchup = pd.read_csv(latest_file_matchup)


# split_columns = df_matchup['Matchup'].str.split(' vs ', expand=True)

# # Handle missing or inconsistent data by filling with 'Missing'
# split_columns = split_columns.fillna('Missing')

# # Assign to new columns in DataFrame
# df_matchup[['Team_name_1', 'Team_name_2']] = split_columns



# # Get player's team
# player_team = df[df['Player'] == player_name]['team'].values[0]

# # Find the row where the player's team is in either Team_name_1 or Team_name_2
# matchup_row = df_matchup[(df_matchup['Team_name_1'] == player_team) | (df_matchup['Team_name_2'] == player_team)]

# # Determine the opposing team
# if not matchup_row.empty:
#     row = matchup_row.iloc[0]
#     other_team = row['Team_name_2'] if row['Team_name_1'] == player_team else row['Team_name_1']
# else:
#     other_team = "Unknown"

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

#             # Estimate standard deviation using z-score
#             std_estimate = (high - low) / (2 * z_score)

#             # Simulate outcomes
#             simulated_outcomes = np.random.normal(loc=mean, scale=std_estimate, size=100000)
#             prob_over_threshold = np.mean(simulated_outcomes >= threshold)
            

#             # Display result
#             st.subheader("🎯 Probability Meter")
#             st.metric(
#                 label=f"Probability {player_name} gets ≥ {threshold} {stat_label} against {other_team}",
#                 value=f"{prob_over_threshold:.1%}"
#             )
#             st.progress(prob_over_threshold)

#             st.markdown(f"""
#             **What does this mean?**

#             Out of **100,000 simulations** of what {player_name} might get:

#             > **{int(prob_over_threshold * 100000):,}** were **{threshold} or more**.

#             That means there's about a **{prob_over_threshold:.2%} chance** they hit that number and more.

#             _(Confidence level: {int(confidence_level * 100)}%)_
#             """)

#             # Show recent games
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

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("🎯 Boost Your Edge with NBA Player Probabilities")

with col2:
    st.markdown("Last update: Apr 14, 2025")

# Load latest file from directory
# directory = r"D:\streamlit_ingest\final_merged_df"
directory = "/home/ubuntu/aws_streamlit_ingest/streamlit_ingest/final_merged_df"
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
player_name = st.selectbox("Search or Select a Player", df['Player'].unique())

# Create tabs
tabs = st.tabs(["📊 Points (PTS)",  "💪 Rebounds (REB)", "🎯 Assists (AST)"])


directory_matchup = "/home/ubuntu/aws_streamlit_ingest/streamlit_ingest/matchup_PTS"
# Use glob to get all CSV files in the directory
csv_files_matchup = glob.glob(os.path.join(directory_matchup, "*.csv"))
# Sort the files by modification time (most recent first)
latest_file_matchup = max(csv_files_matchup, key=os.path.getmtime)

df_matchup = pd.read_csv(latest_file_matchup)


split_columns = df_matchup['Matchup'].str.split(' vs ', expand=True)

# Handle missing or inconsistent data by filling with 'Missing'
split_columns = split_columns.fillna('Missing')

# Assign to new columns in DataFrame
df_matchup[['Team_name_1', 'Team_name_2']] = split_columns



# Get player's team
player_team = df[df['Player'] == player_name]['team'].values[0]

# Find the row where the player's team is in either Team_name_1 or Team_name_2
matchup_row = df_matchup[(df_matchup['Team_name_1'] == player_team) | (df_matchup['Team_name_2'] == player_team)]

# Determine the opposing team
if not matchup_row.empty:
    row = matchup_row.iloc[0]
    other_team = row['Team_name_2'] if row['Team_name_1'] == player_team else row['Team_name_1']
else:
    other_team = "Unknown"

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









