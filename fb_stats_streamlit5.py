import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import json
import requests
from io import BytesIO
from streamlit_extras.row import row
import seaborn as sns

# Load the service account credentials from Streamlit secrets
service_account_info = st.secrets["SERVICE_ACCOUNT_JSON"]
creds = service_account.Credentials.from_service_account_info(service_account_info)

# Create a service to access the Google Sheets API
service = build('sheets', 'v4', credentials=creds)

# The ID of your Google Sheet
SPREADSHEET_ID = '1c6zyNC7aii8osjSWPjHbOh0bc7b-EsWJKPKH5lqjXPc'

# Specify the range of data you want to access
RANGE_NAME = 'Sheet1!A1:T5000'


def get_sheet_data():
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        st.error('No data found in the Google Sheet.')
        return None

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

# Team logos dictionary (replace with actual URLs)
team_logos = {
    'Packers': 'https://drive.google.com/uc?export=view&id=144CQLI5f-_azRj2UccO_BBU972I6VRwG',
    'Texans': 'https://drive.google.com/uc?export=view&id=1468FtlvR4PUyewCfSDY97bC-jueSejsL',
    'Cardinals': 'https://drive.google.com/uc?export=view&id=133uW9bsKHkbU5loaCm1R_zB2IIJ4KGFa',
    'Falcons': 'https://drive.google.com/uc?export=view&id=137tl66qr7eewXctdJE03R0LNr2BfnquC',
    'Ravens': 'https://drive.google.com/uc?export=view&id=1346XrdRjnkqFt1JmUIcXxpgzH75iP1VN',
    'Bills': 'https://drive.google.com/uc?export=view&id=139aFrQMSIiyUY7eocoUlORMJwfds6Yz3',
    'Panthers': 'https://drive.google.com/uc?export=view&id=13GIjfXJDcqPePr0wzhbuR-hJzFgWsSS-',
    'Bears': 'https://drive.google.com/uc?export=view&id=13PLoUkagumSvfr5XJ8GAlyJVxe9KtjMF',
    'Bengals': 'https://drive.google.com/uc?export=view&id=13WYs_NPrV4P7p9-bY-9GD3WbrRWhKwUA',
    'Browns': 'https://drive.google.com/uc?export=view&id=13XszekawObLvEaCWMMKzVox_yErRLhlk',
    'Cowboys': 'https://drive.google.com/uc?export=view&id=13f3JuAq4z8nKgqNEbSrdf0Sz-0j4WOBX',
    'Broncos': 'https://drive.google.com/uc?export=view&id=13hX1O6qA4wG4zeBVBYiW7T3WGYogoqgm',
    'Lions': 'https://drive.google.com/uc?export=view&id=13pW4M0IJqapOe0Ih7YQt4hLSHzsfg5o9',
    'Colts': 'https://drive.google.com/uc?export=view&id=1486Ctp73cUDwoPntDarMfDEB8oLtqeMM',
    'Jaguars': 'https://drive.google.com/uc?export=view&id=148pszC6x1-Ekb_E9G6jsxlsa4CpDtRlZ',
    'Chiefs': 'https://drive.google.com/uc?export=view&id=14MQFysDCMutrI2SyRRWxWVdCqTVnPGe2',
    'Chargers': 'https://drive.google.com/uc?export=view&id=14ftMjvMxmBNEif38l3gFFLBl-6ehBZ76',
    'Rams': 'https://drive.google.com/uc?export=view&id=14ix9KAaQQc429PkakqEhwvs5snKyfnaH',
    'Dolphins': 'https://drive.google.com/uc?export=view&id=14mvHgq6_T88MqIDJOZL50SvGNfTXuUZW',
    'Vikings': 'https://drive.google.com/uc?export=view&id=14sbFLPVxWutXQJXpLufGwWQ-K1R-b5Ei',
    'Patriots': 'https://drive.google.com/uc?export=view&id=152iKOC3H7lhM8-L7spObiGVJBUV7E9_r',
    'Saints': 'https://drive.google.com/uc?export=view&id=155_94kH8wZSpwVwI1PY5gPS0yvtHXIQE',
    'Giants': 'https://drive.google.com/uc?export=view&id=15CeuLekrBvnXeIV5Xkw1jShWwgYg5FTH',
    'Jets': 'https://drive.google.com/uc?export=view&id=15LvXkKR4o_LkwJtcMjYZN_Nc0kfPvUkC',
    'Raiders': 'https://drive.google.com/uc?export=view&id=150bOHDdftBYei7fax7ZOStkO73VyefJF',
    'Eagles': 'https://drive.google.com/uc?export=view&id=15Psj8QTYv3LT2SKWyhzZ-a8-uxLiY6m0',
    'Steelers': 'https://drive.google.com/uc?export=view&id=15UWMiayQloiT4Vw0iqvlXywAj8jmSlN7',
    '49ers': 'https://drive.google.com/uc?export=view&id=15WCnRVXyqfn4pt5n-zi0njxS_X_2ekgd',
    'Seahawks': 'https://drive.google.com/uc?export=view&id=15jUl7AJUPFQ6DuLqBlzJjoqivwB5ExyK',
    'Buccaneers': 'https://drive.google.com/uc?export=view&id=15o9HzFkgVw-4mg_oqV8LoI7Rg9n5ZHPa',
    'Titans': 'https://drive.google.com/uc?export=view&id=15r-k-eIAomuWH_dpXLuh5UYG9mMcMnQ2',
    'Commanders': 'https://drive.google.com/uc?export=view&id=15zChouLg0YRlZQtHC9RQI4NSrB-YjWOq',
}

# Define base colors for teams
base_colors = {
    'Cardinals': '#97233F', 'Falcons': '#A71930', 'Ravens': '#241773',
    'Bills': '#00338D', 'Panthers': '#0085CA', 'Bears': '#0B162A',
    'Bengals': '#FB4F14', 'Browns': '#311D00', 'Cowboys': '#003594',
    'Broncos': '#FB4F14', 'Lions': '#0076B6', 'Packers': '#203731',
    'Texans': '#03202F', 'Colts': '#002C5F', 'Jaguars': '#006778',
    'Chiefs': '#E31837', 'Raiders': '#A5ACAF', 'Chargers': '#0080C6',
    'Rams': '#003594', 'Dolphins': '#008E97', 'Vikings': '#4F2683',
    'Patriots': '#002244', 'Saints': '#D3BC8D', 'Giants': '#0B2265',
    'Jets': '#125740', 'Eagles': '#004C54', 'Steelers': '#FFB612',
    '49ers': '#AA0000', 'Seahawks': '#002244', 'Buccaneers': '#D50A0A',
    'Titans': '#0C2340', 'Commanders': '#5A1414'
}
#load area map
def load_area_map_data():
    try:
        with open('team_season_stats.json', 'r') as f:
            data2 = json.load(f)
        return data2
    except Exception as e:
        print("Error loading data2:", e)
        return None

###this is in the workingversion for just the heatmap though
# Define function to load JSON data for heatmap and area map
def load_heatmap_data():
    with open('football_team_stats.json', 'r') as f:
        data1 = json.load(f)
    nfc_vs_nfc_win_crosstab = pd.DataFrame(data['nfc_heatmap_data'])
    afc_vs_afc_win_crosstab = pd.DataFrame(data['afc_heatmap_data'])
    return nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab

def create_heatmap(conference, nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab):
  
    if conference == 'NFC':
        data1 = nfc_vs_nfc_win_crosstab
        title = "NFC Wins by Each Team Against NFC Opponents 2017-2024"
        cmap = "Blues"
    else:
        data1 = afc_vs_afc_win_crosstab
        title = "AFC Wins by Each Team Against AFC Opponents 2017-2024"
        cmap = "Reds"
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(data1, annot=True, fmt="d", cmap=cmap, linewidths=0.5, ax=ax)
    
    ax.set_title(title)
    ax.set_xlabel("Opponent")
    ax.set_ylabel("Winner")
    return fig

# Area heat map plotting function
# #def plot_area_map(data2):
#    plt.figure(figsize=(12, 6))
    
#    plt.fill_between(data['Week'], data2['Win %'], color='skyblue', alpha=0.4)
#    plt.plot(data2['Week'], data2['Win %'], color='navy', linewidth=2)
    
#    plt.title(f'{data2.iloc[0]["Team"]} Win % Trend', fontsize=16)
#    plt.xlabel('Week', fontsize=12)
#    plt.ylabel('Win %', fontsize=12)
#    plt.ylim(0, 100)
#    plt.grid(True, linestyle='--', alpha=0.7)

#    return plt


def main():
    #added global all_team_stats - was not in other version
    global all_team_stats
    global data2
    data2 = load_area_map_data()  # Load data2 separately for area map

 # Confirm data2 was loaded correctly
    if data2 is not None:
        print("data2 loaded successfully:", data2)  # Display the content of data2
    else:
        print("Failed to load data2.")  # Error message if data2 is None

    st.set_page_config(layout="wide")

    # Load data from JSON file for team stats at the start of main()
    # with open('football_team_stats.json', 'r') as f:
    # all_team_stats = json.load(f)

    # Load data for heatmap and area map
    nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab = load_heatmap_data()
  
    # Create a layout with spacer columns for simulated left alignment
    spacer1, col1, spacer2, col2, col3, spacer3 = st.columns([0.5, 1, 0.4, 2, 1, 0.1], vertical_alignment="bottom")

    # First column: Title
    with col1:
        st.title("Football Team Dashboard")

    # Second column: Selectbox for choosing the team
    with col2:
        team_name = st.selectbox("Select a team:", sorted(all_team_stats.keys()))

    # Third column: Team logo display
    with col3:
        if team_name in team_logos:
            try:
                response = requests.get(team_logos[team_name])
                img = BytesIO(response.content)
                st.image(img, width=100)  # Adjust width as needed
            except Exception as e:
                st.error(f"Error loading team logo: {e}")

    # Spacer columns ensure content is positioned as needed
    spacer3, col4, col5, spacer4 = st.columns([0.5, 3, 5, 0.5])


   # First column of the second row: Display team data
    with col4:
        team_data = all_team_stats[team_name]
        df = pd.DataFrame(team_data)
        st.write(f"Wins, Losses, and Win Percentage by year for {team_name}")
    
        # Display the DataFrame without the index column
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Second column of the second row: Prepare and display the chart
    with col5:
        plot_data = df[df['Season'] != 'Total']
        fig, ax = plt.subplots(figsize=(10, 5))

        team_color = base_colors.get(team_name, '#000000')
        ax.bar(plot_data['Season'], plot_data['Win_Percentage'].str.rstrip('%').astype(int),
               color=team_color, label='Win Percentage')
        ax.plot(plot_data['Season'], plot_data['Total_Wins'],
                color='r', marker='o', label='Team Wins')

        for i, row in plot_data.iterrows():
            ax.text(row['Season'], row['Total_Wins'] + 1, str(row['Total_Wins']),
                    color='black', ha='center', va='bottom')

        ax.set_title(f"{team_name} Performance by Season")
        ax.set_xlabel('Season')
        ax.set_ylabel('Performance Metrics')
        plt.xticks(rotation=45)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

   # Display conference heatmap
    st.header("Conference Heatmap")
    conference = st.radio("Select a conference:", ("AFC", "NFC"))
    nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab = load_heatmap_data()
    heatmap_fig = create_heatmap(conference, nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab)
    st.pyplot(heatmap_fig)

    print(area_map_data.columns)

    # Plot area map for team performance
    # Title of the app
st.title("NFL Team Statistics")

# Dropdown for selecting team
teams = list(data2.keys())
selected_team = st.selectbox("Select Team", teams)

# Dropdown for selecting seasons
seasons = list(data2[selected_team].keys())
selected_season_1 = st.selectbox("Select Season 1", seasons)
selected_season_2 = st.selectbox("Select Season 2", seasons)

# Fetch and display stats for the selected team and seasons
season_data_1 = data2[selected_team][selected_season_1]
season_data_2 = data2[selected_team][selected_season_2]

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

#if isinstance(data2, dict):
#    teams = list(data2.keys())
#else:
#    print("data2 is not a dictionary")

#print(data2)
# Dropdown for selecting team
#teams = list(data2.keys())
#selected_team = st.selectbox("Select Team", teams)

# Dropdown for selecting seasons
#seasons = list(data2[selected_team].keys())
#selected_season_1 = st.selectbox("Select Season 1", seasons)
#selected_season_2 = st.selectbox("Select Season 2", seasons)

# Fetch and display stats for the selected team and seasons
#season_data_1 = data2[selected_team][selected_season_1]
#season_data_2 = data2[selected_team][selected_season_2]

# Create a combined chart for both seasons
#def plot_combined_win_percentage(season_data_1, season_data_2):
#    weeks_1 = [item['Week'] for item in season_data_1]
#    win_percentage_1 = [item['Win %'] for item in season_data_1]
    
#    weeks_2 = [item['Week'] for item in season_data_2]
#    win_percentage_2 = [item['Win %'] for item in season_data_2]

    # Create a new figure object
 #   fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plotting the first season's data
#    ax.fill_between(weeks_1, win_percentage_1, color='skyblue', alpha=0.4, label=f'{selected_season_1} Win %')
#    ax.plot(weeks_1, win_percentage_1, marker='o', color='navy', linewidth=2)

    # Plotting the second season's data
#    ax.fill_between(weeks_2, win_percentage_2, color='lightgreen', alpha=0.4, label=f'{selected_season_2} Win %')
#    ax.plot(weeks_2, win_percentage_2, marker='o', color='darkgreen', linewidth=2)

    # Customize the chart
#    ax.set_title(f'{selected_team} Win % Trend Comparison: {selected_season_1} vs {selected_season_2}', fontsize=16)
#    ax.set_xlabel('Week', fontsize=12)
 #   ax.set_ylabel('Win %', fontsize=12)
 #   ax.set_ylim(0, 100)
 #   ax.set_xlim(1, max(max(weeks_1), max(weeks_2)))  # Set x-axis limits based on weeks
 #   ax.set_xticks(range(1, max(max(weeks_1), max(weeks_2)) + 1))  # Set x-axis ticks to week numbers
 #   ax.grid(True, linestyle='--', alpha=0.7)
 #   ax.legend()

#    return fig  # Return the figure object

# Plot and display the combined chart for both selected seasons
#if season_data_1 and season_data_2:
#    fig = plot_combined_win_percentage(season_data_1, season_data_2)
#    st.pyplot(fig)  # Pass the figure object to st.pyplot()

    # Displaying the stats in a table format
#if season_data_1:
#    st.write(f"Statistics for {selected_team} in {selected_season_1}:")
#    st.dataframe(pd.DataFrame(season_data_1))

#if season_data_2:
#    st.write(f"Statistics for {selected_team} in {selected_season_2}:")
#    st.dataframe(pd.DataFrame(season_data_2))

 
if __name__ == "__main__":
    main()

