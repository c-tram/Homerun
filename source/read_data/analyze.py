import pandas as pd
import numpy as np

#purpose of this file will be to analyze the data that we have gathered from the gather_data folder and to create visualizations of the data
#we will use pandas to read the data and matplotlib to create visualizations
#from this data, we will be able to see trends and patterns in the data that we have gathered and predict who should have won the WS based on the data and overall percentages for each tim to have won the world series

# Load the data
data = pd.read_csv('/Users/coletrammell/Documents/GitHub/Homerun/source/gather_data/combined_data.csv')

# Define the columns in the order of their weights
columns = ['Wins','Losses', 'RS', 'RA', 'PCT', 'DIF', 'OBP', 'xSLG', 'HR']

# Check if all columns exist in the DataFrame
missing_columns = [col for col in columns if col not in data.columns]
if missing_columns:
    raise KeyError(f"Missing columns in data: {missing_columns}")

# Initialize a dictionary to store the rankings
rankings = {team: 0 for team in data['Team'].unique()}

# Run the test 100 times
for _ in range(100):
    # Generate base weights in the order of columns
    base_weights = np.array([0.2, 0.3, 0.15, 0.15, 0.05, 0.05, 0.05, 0.025, 0.025])
    # Adjust weights by ±20%
    weights = base_weights + (np.random.rand(len(columns)) - 0.5) * 0.4
    weights = np.clip(weights, 0, 1)  # Ensure weights are within [0, 1]

    # Calculate the weighted score for each team
    data['Score'] = data[columns].dot(weights)

    # Rank the teams based on their scores
    data['Rank'] = data['Score'].rank(ascending=False)

    # Update the rankings
    for team in data['Team'].unique():
        rankings[team] += data.loc[data['Team'] == team, 'Rank'].values[0]

# Calculate the average ranking
for team in rankings:
    rankings[team] /= 100

# Sort the teams by their average ranking
sorted_rankings = sorted(rankings.items(), key=lambda x: x[1])

    # Save the rankings to a new CSV file
rankings_df = pd.DataFrame(sorted_rankings, columns=['Team', 'Average Rank'])
rankings_df.to_csv('/Users/coletrammell/Documents/GitHub/Homerun/source/read_data/rankings.csv', index=False)