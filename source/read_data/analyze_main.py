import analyze_functions
import csv

if __name__ == "__main__":

    data = analyze_functions.load_team_data('../gather_data/generated_data')
    team_averages = analyze_functions.calculate_team_averages(data)
    league_averages = analyze_functions.calculate_league_averages(team_averages)
    comparisons = analyze_functions.compare_team_to_league(team_averages, league_averages)
    predictions = analyze_functions.predict_win_loss(comparisons)

    with open('output.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Team', 'Average', 'League Average', 'Comparison', 'Prediction'])
        for team, avg in team_averages.items():
            league_avg = league_averages.get(team, 'N/A')
            comparison = comparisons.get(team, 'N/A')
            prediction = predictions.get(team, 'N/A')
            writer.writerow([team, avg, league_avg, comparison, prediction])