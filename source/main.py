import threading
import analyze_functions
import gather_functions

if __name__ == "__main__":

    gather_functions.team_stat_pull(2021,2024)

    hitting_data = analyze_functions.read_data('generated_data/team_hitting_stats_2024.csv')
    pitching_data = analyze_functions.read_data('generated_data/team_pitching_stats_2024.csv')

    hitting_averages = analyze_functions.calculate_averages(hitting_data)
    pitching_averages = analyze_functions.calculate_averages(pitching_data)

    hitting_team_averages = analyze_functions.calculate_team_averages(hitting_data)
    pitching_team_averages = analyze_functions.calculate_team_averages(pitching_data)

    hitting_ratios = analyze_functions.calculate_ratios(hitting_team_averages, hitting_averages, multiplier=1)
    pitching_ratios = analyze_functions.calculate_ratios(pitching_team_averages, pitching_averages, multiplier=-1)

    total_ratios = analyze_functions.calculate_total_ratios(hitting_ratios, pitching_ratios)

    predictions = analyze_functions.predict_win_loss(total_ratios)
    analyze_functions.write_predictions_to_csv(predictions, 'predicted_win_loss.csv')




