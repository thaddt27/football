import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load JSON data
with open('football_team_stats.json') as f:
    data = json.load(f)

# Check if data is a list or dict
if isinstance(data, list):
    # Assuming each item in the list is a dictionary representing a team
    teams = [team['team_name'] for team in data]  # Adjust based on actual key for team name
else:
    teams = list(data.keys())

selected_team = st.selectbox("Select Team", teams)

# Find the selected team's data
if isinstance(data, list):
    selected_team_data = next(team for team in data if team['team_name'] == selected_team)
    seasons = list(selected_team_data['seasons'].keys())  # Adjust based on actual key for seasons
else:
    selected_team_data = data[selected_team]
    seasons = list(selected_team_data.keys())

selected_season_1 = st.selectbox("Select Season 1", seasons)
selected_season_2 = st.selectbox("Select Season 2", seasons)

# Fetch and display stats for the selected team and seasons
season_data_1 = selected_team_data['seasons'][selected_season_1]  # Adjust based on actual structure
season_data_2 = selected_team_data['seasons'][selected_season_2]  # Adjust based on actual structure

# Create a combined chart for both seasons
def plot_combined_win_percentage(season_data_1, season_data_2):
    weeks_1 = [item['Week'] for item in season_data_1]
    win_percentage_1 = [item['Win %'] for item in season_data_1]
    
    weeks_2 = [item['Week'] for item in season_data_2]
    win_percentage_2 = [item['Win %'] for item in season_data_2]

    # Create a new figure object
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plotting the first season's data
    ax.fill_between(weeks_1, win_percentage_1, color='skyblue', alpha=0.4, label=f'{selected_season_1} Win %')
    ax.plot(weeks_1, win_percentage_1, marker='o', color='navy', linewidth=2)

    # Plotting the second season's data
    ax.fill_between(weeks_2, win_percentage_2, color='lightgreen', alpha=0.4, label=f'{selected_season_2} Win %')
    ax.plot(weeks_2, win_percentage_2, marker='o', color='darkgreen', linewidth=2)

    # Customize the chart
    ax.set_title(f'{selected_team} Win % Trend Comparison: {selected_season_1} vs {selected_season_2}', fontsize=16)
    ax.set_xlabel('Week', fontsize=12)
    ax.set_ylabel('Win %', fontsize=12)
    ax.set_ylim(0, 100)
    ax.set_xlim(1, max(max(weeks_1), max(weeks_2)))  # Set x-axis limits based on weeks
    ax.set_xticks(range(1, max(max(weeks_1), max(weeks_2)) + 1))  # Set x-axis ticks to week numbers
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()

    return fig  # Return the figure object

# Plot and display the combined chart for both selected seasons
if season_data_1 and season_data_2:
    fig = plot_combined_win_percentage(season_data_1, season_data_2)
    st.pyplot(fig)  # Pass the figure object to st.pyplot()

    # Displaying the stats in a table format
if season_data_1:
    st.write(f"Statistics for {selected_team} in {selected_season_1}:")
    st.dataframe(pd.DataFrame(season_data_1))

if season_data_2:
    st.write(f"Statistics for {selected_team} in {selected_season_2}:")
    st.dataframe(pd.DataFrame(season_data_2))
