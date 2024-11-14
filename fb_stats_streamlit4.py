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
SPREADSHEET_ID = '1c6zyNC7aii8osjSWPjHbOh0bc7b-EsWJKPKH5lqjXPc'  # Replace with your actual spreadsheet ID

# Specify the range of data you want to access
RANGE_NAME = 'Sheet1!A1:T5000'  # Adjust based on your actual sheet name and range


def get_sheet_data(sheet_name):
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

def adjust_color_hue(color, factor=0.5):
    color = color.lstrip('#')
    r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    r, g, b = [min(255, max(0, x)) for x in (r, g, b)]
    return f'#{r:02x}{g:02x}{b:02x}'

def create_heatmap(conference, nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab):
    if conference == 'NFC':
        data = nfc_vs_nfc_win_crosstab
        title = "NFC Wins by Each Team Against NFC Opponents 2017-2024"
        cmap = "Blues"
    else:  # AFC
        data = afc_vs_afc_win_crosstab
        title = "AFC Wins by Each Team Against AFC Opponents 2017-2024"
        cmap = "Reds"
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(data, annot=True, fmt="d", cmap=cmap, linewidths=0.5, ax=ax)
    
    ax.set_title(title)
    ax.set_xlabel("Opponent")
    ax.set_ylabel("Winner")
    return fig

#Heatmap
def plot_area_map(data):
    plt.figure(figsize=(12, 6))
    
    # Assuming 'Week' and 'Win %' columns exist in your area map data
    plt.fill_between(data['Week'], data['Win %'], color='skyblue', alpha=0.4)
    plt.plot(data['Week'], data['Win %'], color='navy', linewidth=2)
    
    plt.title(f'{team_name} Win % Trend', fontsize=16)
    plt.xlabel('Week', fontsize=12)
    plt.ylabel('Win %', fontsize=12)
    plt.ylim(0, 100)
    plt.xlim(1, max(data['Week']))
    plt.xticks(range(1, max(data['Week']) + 1))  # Set x-axis ticks to week numbers
    plt.grid(True, linestyle='--', alpha=0.7)

    return plt# 

#Load the heatmap data from your JSON file
def load_heatmap_data():
    with open('football_team_stats.json', 'r') as f:
        data = json.load(f)
    nfc_vs_nfc_win_crosstab = pd.DataFrame(data['nfc_heatmap_data'])
    afc_vs_afc_win_crosstab = pd.DataFrame(data['afc_heatmap_data'])
    return nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab

def load_areamap_data():
    with open('football_team_stats.json', 'r') as f:
        return json.load(f)

    all_team_stats = load_data()

def main():
    global all_team_stats
    
    st.set_page_config(layout="wide")  # Set layout to wide for better visibility

    # Load data from JSON file for team stats at the start of main()
    with open('football_team_stats.json', 'r') as f:
        all_team_stats = json.load(f)

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

    # New section for heatmap
    st.header("Conference Heatmap")
    conference = st.radio("Select a conference:", ("AFC", "NFC"))
    
    nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab = load_heatmap_data()
    
    heatmap_fig = create_heatmap(conference, nfc_vs_nfc_win_crosstab, afc_vs_afc_win_crosstab)
    st.pyplot(heatmap_fig)

    # Extract area map data for the selected team
    area_map_data = pd.DataFrame(all_team_stats['all_team_games'])  # Ensure this key exists
    if 'Team' in area_map_data.columns:  # Check if 'Team' column exists
    team_area_map_data = area_map_data[area_map_data['Team'] == team_name]
    st.write(f"Area Map Data for {team_name}")
    st.dataframe(team_area_map_data)  # Display the DataFrame

    # Generate and display the area map
    area_map_fig = plot_area_map(team_area_map_data)
    st.pyplot(area_map_fig)
    else:
    st.error("The expected data for area map is not available.")



# Generate and display the area map
area_map_fig = plot_area_map(team_area_map_data)
st.pyplot(area_map_fig)

if __name__ == "__main__":
    main()