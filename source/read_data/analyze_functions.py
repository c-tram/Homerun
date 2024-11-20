import csv
import statistics

def read_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def calculate_averages(data):
    averages = {}
    for key in data[0].keys():
        if key != 'Team':
            values = [float(str(row[key]).replace(',', '').replace('"', '').replace("'", '').strip('[]')) for row in data]
            averages[key] = statistics.mean(values)
    return averages

def calculate_team_averages(data):
    team_averages = {}
    for row in data:
        team = row['Team']
        if team not in team_averages:
            team_averages[team] = {}
        for key in row.keys():
            if key != 'Team':
                team_averages[team][key] = float(str(row[key]).replace(',', '').replace('"', '').replace("'", '').strip('[]'))
    return team_averages

def calculate_ratios(team_averages, league_averages, multiplier=1):
    ratios = {}
    for team, stats in team_averages.items():
        ratios[team] = {}
        for stat, value in stats.items():
            ratios[team][stat] = multiplier * (value / league_averages[stat])
    return ratios

def calculate_total_ratios(hitting_ratios, pitching_ratios):
    total_ratios = {}
    for team in hitting_ratios.keys():
        total_ratios[team] = (sum(hitting_ratios[team].values()) + sum(pitching_ratios[team].values())) / (len(hitting_ratios[team]) + len(pitching_ratios[team]))
    return total_ratios

def predict_win_loss(total_ratios):
    mean_ratio = statistics.mean(total_ratios.values())

    predictions = []
    for team, ratio in total_ratios.items():
        win_loss_ratio = ratio / mean_ratio
        wins = 162 * win_loss_ratio / (1 + win_loss_ratio)
        losses = 162 - wins
        predictions.append({'Team': team, 'Win-Loss Ratio': win_loss_ratio, 'Wins': round(wins), 'Losses': round(losses)})
        predictions.sort(key=lambda x: x['Wins'], reverse=True)
    return predictions

def write_predictions_to_csv(predictions, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Team', 'Win-Loss Ratio', 'Wins', 'Losses'])
        writer.writeheader()
        writer.writerows(predictions)

if __name__ == "__main__":
    hitting_data = read_data('../gather_data/generated_data/team_hitting_stats_2024.csv')
    pitching_data = read_data('../gather_data/generated_data/team_pitching_stats_2024.csv')

    hitting_averages = calculate_averages(hitting_data)
    pitching_averages = calculate_averages(pitching_data)

    hitting_team_averages = calculate_team_averages(hitting_data)
    pitching_team_averages = calculate_team_averages(pitching_data)

    hitting_ratios = calculate_ratios(hitting_team_averages, hitting_averages, multiplier=1)
    pitching_ratios = calculate_ratios(pitching_team_averages, pitching_averages, multiplier=-1)

    total_ratios = calculate_total_ratios(hitting_ratios, pitching_ratios)

    predictions = predict_win_loss(total_ratios)
    write_predictions_to_csv(predictions, 'predicted_win_loss.csv')
