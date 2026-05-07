import pandas as pd
import plotly.express as px
from great_tables import GT

# 1. Read the datasets
df_match = pd.read_csv("Match.csv", sep=";")
df_possession = pd.read_csv("Match_Possesion.csv", sep=";")
df_team = pd.read_csv("Teams_Datavs.csv", sep=";")

# 2. Group by match_id to get the average possession per match
df_pos_grouped = df_possession.groupby('match_id', as_index=False)['homepos'].mean()

# 3. Find Barcelona's ID
barca_row = df_team[df_team['team_long_name'].str.contains('Barcelona', case=False, na=False)]
barca_id = barca_row['team_api_id'].values[0]

# 4. Filter matches where Barcelona is the home team
df_barca_matches = df_match[df_match['home_team_api_id'] == barca_id].copy()

# 5. Calculate match outcomes
def get_barca_outcome(row):
    if row['home_team_goal'] > row['away_team_goal']:
        return 'Win'
    elif row['home_team_goal'] < row['away_team_goal']:
        return 'Loss'
    else:
        return 'Draw'

df_barca_matches['Outcome'] = df_barca_matches.apply(get_barca_outcome, axis=1)  

# 6. Merge the dataframes
df_merged = pd.merge(df_barca_matches, df_pos_grouped, left_on='match_api_id', right_on='match_id', how='inner')

# Fallback merge if the first one yields empty results
if len(df_merged) == 0:
    df_merged = pd.merge(df_barca_matches, df_pos_grouped, left_on='id', right_on='match_id', how='inner')

df_final = pd.merge(df_merged, df_team, left_on='home_team_api_id', right_on='team_api_id', how='left')

# 7. Select and rename columns for a clean output and plot
columns = ['team_long_name', 'Outcome', 'homepos']

try:
    # Select specific columns and rename them immediately
    df_plot = df_final[columns].rename(columns={
        'team_long_name': 'Team Name',
        'Outcome': 'Result',
        'homepos': 'Possession Rate'
    })
    
    # Print the table cleanly without the index numbers
    print("\n--- FC Barcelona: Match Results and Possession Rates ---")
    print(df_plot.head(15).to_string(index=False))
    
except KeyError as e:
    print(f"Error: Column couldn't be found {e}. Please write the correct name.")

# 8. Create the interactive Plotly boxplot
fig = px.box(
    df_plot,
    x="Result", # Updated to match renamed column
    y="Possession Rate", # Updated to match renamed column
    color="Result",
    category_orders={"Result": ["Win", "Draw", "Loss"]},
    color_discrete_map={
        "Win": "#2ecc71",   
        "Draw": "#f1c40f",  
        "Loss": "#e74c3c"   
    },
    title="FC Barcelona: Possession Rates by Match Outcome (Home)",
    points="outliers"
)

# 9. Update layout for a cleaner look
fig.update_layout(
    template="plotly_white",
    title_font=dict(size=18, family="Arial", color="black"),
    xaxis_title_font=dict(size=14),
    yaxis_title_font=dict(size=14),
    showlegend=False
)

fig.show()