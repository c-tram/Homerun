from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os
import threading
import team_identifiers

def setup_driver():
    """Setup the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver_path = '/Users/coletrammell/Downloads/chromedriver-mac-arm64/chromedriver'
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    return driver

def team_hitting_stat_pull_for_year(year):
    url = f'https://baseballsavant.mlb.com/league?view=statcast&nav=hitting&season={year}'
    driver = setup_driver()
    driver.get(url)
    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, '.statcast-generic')
    for row in rows:
        team_logo = row.find_element(By.CSS_SELECTOR, '.team-mug')
        team_id = team_logo.get_attribute('src').split('/')[-1].split('.')[0]
        team_name = team_identifiers.get_team_name(team_id)
        cells = row.find_elements(By.CSS_SELECTOR, '.tr-data.align-right')
        if len(data) >= 30:
            break
        data.append([team_name] + [cell.text for cell in cells[:12]])  # Include team name and take the first 12 columns

    driver.quit()

    # Define the CSV file headers
    headers = ['Team', 'PA', 'AB', 'Hits', '2B', '3B', 'HR', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'xSLG']
    
    # Ensure the directory exists
    os.makedirs('generated_data', exist_ok=True)
    
    # Write data to CSV file
    with open(f'generated_data/team_hitting_stats_{year}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Data has been written to generated_data/team_hitting_stats_{year}.csv")

def team_pitching_stat_pull_for_year(year):
    url = f'https://baseballsavant.mlb.com/league?view=statcast&nav=pitching&season={year}'
    driver = setup_driver()
    driver.get(url)
    
    # Wait for the data to load
    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, '.statcast-generic')
    for row in rows:
        team_logo = row.find_element(By.CSS_SELECTOR, '.team-mug')
        team_id = team_logo.get_attribute('src').split('/')[-1].split('.')[0]
        team_name = team_identifiers.get_team_name(team_id)
        cells = row.find_elements(By.CSS_SELECTOR, '.tr-data.align-right')

        
        if all(cell.text != '' for cell in cells[1:8]):
            data.append([team_name] + [cell.text for cell in cells[:8]])  # Include team name and take the first 8 columns

    driver.quit()

    # Define the CSV file headers
    headers = ['Team', 'H', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'Exit Velocity']
    
    # Ensure the directory exists
    os.makedirs('generated_data', exist_ok=True)
    
    # Write data to CSV file
    with open(f'generated_data/team_pitching_stats_{year}.csv', 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Data has been written to generated_data/team_pitching_stats_{year}.csv")

def team_stat_pull(start_year, end_year):
    threads = []
    for year in range(start_year, end_year + 1):
        hitting_thread = threading.Thread(target=team_hitting_stat_pull_for_year, args=(year,))
        pitching_thread = threading.Thread(target=team_pitching_stat_pull_for_year, args=(year,))
        threads.append(hitting_thread)
        threads.append(pitching_thread)
        hitting_thread.start()
        pitching_thread.start()

    for thread in threads:
        thread.join()

def team_standing_pull_for_year(year):
    url = f'https://www.mlb.com/standings/mlb?season={year}'
    driver = setup_driver()
    driver.get(url)

    data = []
    
    rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, 'td')
        team_name = row.find_element(By.CSS_SELECTOR, 'th').text
        wins = cells[0].text
        losses = cells[1].text
        pct = cells[2].text
        rs = cells[7].text
        ra = cells[8].text
        dif = cells[9].text
        xwl = cells[10].text
        data.append([team_name, wins, losses, pct, rs, ra, dif, xwl])

    driver.quit()

    # Define the CSV file headers
    headers = ['Team', 'Wins', 'Losses', 'PCT', 'RS', 'RA', 'DIF', 'X-W/L']

    # Ensure the directory exists
    os.makedirs('generated_data', exist_ok=True)
    
    # Write data to CSV file
    with open(f'generated_data/team_standings_{year}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Data has been written to generated_data/team_standings_{year}.csv")

def team_standing_pull(start_year, end_year):
    threads = []
    for year in range(start_year, end_year + 1):
        thread = threading.Thread(target=team_standing_pull_for_year, args=(year,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def combine_csv_files():
    # Ensure the directory exists
    os.makedirs('generated_data', exist_ok=True)
    
    # Read the CSV files
    with open('generated_data/team_stats.csv', 'r') as stats_file:
        stats_reader = csv.reader(stats_file)
        stats_data = list(stats_reader)

    with open('generated_data/team_standings.csv', 'r') as standings_file:
        standings_reader = csv.reader(standings_file)
        standings_data = list(standings_reader)

    # Combine the data
    combined_data = []
    for stats_row in stats_data:
        for standings_row in standings_data:
            if standings_row[0].__contains__(stats_row[0]):
                combined_data.append(stats_row + standings_row[1:])

    # Write the combined data to a new CSV file
    with open('generated_data/combined_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(combined_data)

    print("Data has been written to generated_data/combined_data.csv")


