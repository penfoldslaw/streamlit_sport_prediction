import os
import glob
import pandas as pd

import streamlit as st





st.set_page_config(layout="wide")
st.title("NBA Streamlit App")

st.subheader("NBA Player Statistics")
st.markdown("This app displays NBA player statistics.")

# Define the directory where your files are stored
directory = r"D:\streamlit_ingest\final_merged_df"

# Use glob to get all CSV files in the directory
csv_files = glob.glob(os.path.join(directory, "*.csv"))

# Sort the files by modification time (most recent first)
latest_file_final = max(csv_files, key=os.path.getmtime)




# Read the latest CSV file
df = pd.read_csv(latest_file_final)

df = df[[
    'Player','team','PTS','PTS_First_Pct','PTS_Second_Pct','PTS_Third_Pct','recentgames_PTS',
    'REB','REB_First_Pct','REB_Second_Pct','REB_Third_Pct','recentgames_REB',
    'AST','AST_First_Pct','AST_Second_Pct','AST_Third_Pct','recentgames_AST',
]]

df = df.sort_values(by=["team", "Player"], ascending=[True, True])



# Custom style to limit max height/width via CSS
st.markdown("""
    <style>
        .fixed-height-table .stDataFrame { 
            max-height: 400px; 
            overflow-y: auto;
        }
    </style>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab_input, tab_match_pts = st.tabs(["PTS Predictions", "REB Predictions", "AST Predictions", "🔍 Search Player", "Matchup First points"])

with tab1:
    st.subheader("Search for Player Stats")

    # Add a search box to filter players by name
    player_name = st.text_input("Enter Player Name", key="search_player_tab1")

    # If there's a player name entered, filter the dataframe by it
    if player_name:
        filtered_df = df[df['Player'].str.contains(player_name, case=False, na=False)]
    else:
        filtered_df = df  # Show the full dataframe if no search term

    # Display the filtered dataframe
    st.markdown('<div class="fixed-height-table">', unsafe_allow_html=True)
    st.dataframe(
        filtered_df[['Player','team' ,'PTS','PTS_First_Pct','PTS_Second_Pct','PTS_Third_Pct']].reset_index(drop=True),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


with tab2:
    st.subheader("Search for Player Stats")

    # Add a search box to filter players by name
    player_name = st.text_input("Enter Player Name", key="search_player_tab2")

    # If there's a player name entered, filter the dataframe by it
    if player_name:
        filtered_df = df[df['Player'].str.contains(player_name, case=False, na=False)]
    else:
        filtered_df = df  # Show the full dataframe if no search term




    st.markdown('<div class="fixed-height-table">', unsafe_allow_html=True)
    st.dataframe(
        df[['Player', 'team' ,'REB','REB_First_Pct','REB_Second_Pct','REB_Third_Pct']].reset_index(drop=True),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Search for Player Stats")

    # Add a search box to filter players by name
    player_name = st.text_input("Enter Player Name", key="search_player_tab3")

    # If there's a player name entered, filter the dataframe by it
    if player_name:
        filtered_df = df[df['Player'].str.contains(player_name, case=False, na=False)]
    else:
        filtered_df = df  # Show the full dataframe if no search term


    st.markdown('<div class="fixed-height-table">', unsafe_allow_html=True)
    st.dataframe(
        df[['Player', 'team' ,'AST','AST_First_Pct','AST_Second_Pct','AST_Third_Pct']].reset_index(drop=True),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# 🔍 Player Search Tab
with tab_input:
    st.subheader("Search Player Stats")
    player_name = st.text_input("Enter Player Name")

    if player_name:
        filtered_df = df[df['Player'].str.contains(player_name, case=False, na=False)]
        if not filtered_df.empty:
            st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)
        else:
            st.warning("Player not found. Try checking the spelling or a different name.")

    with st.expander("📊 Compare Two Players"):
        col1, col2 = st.columns(2)

        with col1:
            player1 = st.selectbox("Select First Player", df['Player'].unique(), key="compare_player_1")

        with col2:
            player2 = st.selectbox("Select Second Player", df['Player'].unique(), key="compare_player_2")

        # Filter data for the selected players
        comparison_df = df[df['Player'].isin([player1, player2])].reset_index(drop=True)

        if player1 != player2 and len(comparison_df) == 2:
            st.markdown('<div class="fixed-height-table">', unsafe_allow_html=True)
            st.dataframe(comparison_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Please select two different players to compare.")

targets = ['PTS', 'REB', 'AST']
for target in targets:
    directory_matchup = rf"D:\streamlit_ingest\matchup_{target}"
    # Use glob to get all CSV files in the directory
    csv_files_matchup = glob.glob(os.path.join(directory_matchup, "*.csv"))
    # Sort the files by modification time (most recent first)
    latest_file_matchup = max(csv_files_matchup, key=os.path.getmtime)

    df_matchup = pd.read_csv(latest_file_matchup)



    with tab_match_pts:
        st.subheader(f"Matchup {target}")
        st.markdown('<div class="fixed-height-table">', unsafe_allow_html=True)
        st.dataframe(
            df_matchup.reset_index(drop=True),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
