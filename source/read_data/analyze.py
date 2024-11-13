rewrite this code to account for pitching stats as well.

Weight stats in this order. All of these stats are negative. with > being worst stat to have against a pitcher

H > 




import csv

# Read the CSV file
with open('/Users/coletrammell/Documents/GitHub/Homerun/source/gather_data/generated_data/team_stats_2024.csv', mode='r') as file:
    reader = csv.DictReader(file)
    teams_data = list(reader)

# Function to calculate a score based on the given priorities
def calculate_score(team):
    return (int(team['Hits'].replace(',', '')) * 1.5 +
            int(team['BB'].replace(',', '')) * 1.4 +
            float(team['SLG']) * 1.3 +
            float(team['xSLG']) * 1.2 +
            float(team['BA']) * 1.1 +
            int(team['HR']) * 1.0 -
            int(team['SO'].replace(',', '')) * 0.5)

# Calculate scores for each team
for team in teams_data:
    team['Score'] = calculate_score(team)

# Sort teams by score
teams_data.sort(key=lambda x: x['Score'], reverse=True)

# Predict wins and losses
total_games = 162
for i, team in enumerate(teams_data):
    # Assuming the top team wins more games and the bottom team wins fewer games
    wins = total_games * (1 - (i / len(teams_data)))
    losses = total_games - wins
    team['Wins'] = round(wins)
    team['Losses'] = round(losses)

# Write the predictions to a new CSV file
with open('/Users/coletrammell/Documents/GitHub/Homerun/source/gather_data/generated_data/team_stats_2025_predictions.csv', mode='w', newline='') as file:
    fieldnames = ['Team', 'Wins', 'Losses']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    for team in teams_data:
        writer.writerow({'Team': team['Team'], 'Wins': team['Wins'], 'Losses': team['Losses']})