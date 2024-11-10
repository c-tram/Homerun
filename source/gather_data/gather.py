from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import os
import threading

def setup_driver():
    """Setup the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def get_element_text(url, element_id):
    """Get the text of a specific element by its ID."""
    driver = setup_driver()
    driver.get(url)
    element = driver.find_element(By.ID, element_id)
    text = element.text
    driver.quit()
    return text

def get_all_links(url):
    """Get all the links from the webpage."""
    driver = setup_driver()
    driver.get(url)
    links = [a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a')]
    driver.quit()
    return links

# Example function to show a pull
def example_pull():
    url = 'https://example.com'
    title = get_page_title(url)
    print(f"Page Title: {title}")

    element_id = 'exampleElementId'
    element_text = get_element_text(url, element_id)
    print(f"Element Text: {element_text}")

    links = get_all_links(url)
    print(f"Links: {links}")

# In this pull, we will be pulling the year, team, pa, ab, hits, 2b, 3b, hr, bb, so, ba, obp, slg, xslg.
# We will return this data as a CSV file for further analysis
def team_stat_pull():
    url = 'https://baseballsavant.mlb.com/league?view=statcast&nav=hitting&season=2024'
    driver = setup_driver()
    driver.get(url)

    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, '.statcast-generic')

    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, '.tr-data.align-right')
        if len(data) >= 30:
            break
        data.append([cell.text for cell in cells[:12]])  # Only take the first 12 columns

    driver.quit()

    # Define the CSV file headers
    headers = ['Team','PA', 'AB', 'Hits', '2B', '3B', 'HR', 'BB', 'SO', 'BA', 'OBP', 'SLG', 'xSLG']
    teams = [
        'Chicago White Sox', 'Cleveland Guardians', 'Colorado Rockies', 'Washington Nationals', 'Los Angeles Angels',
        'Kansas City Royals', 'Tampa Bay Rays', 'Detroit Tigers', 'Colorado Rockies', 'Oakland Athletics',
        'Miami Marlins', 'Texas Rangers', 'Toronto Blue Jays', 'San Francisco Giants', 'Seattle Mariners',
        'Atlanta Braves', 'Pittsburgh Pirates', 'San Diego Padres', 'Houston Astros', 'St. Louis Cardinals',
        'Cincinnati Reds', 'Minnesota Twins', 'New York Mets', 'Philadelphia Phillies', 'Milwaukee Brewers',
        'Baltimore Orioles', 'Boston Red Sox', 'New York Yankees', 'Los Angeles Dodgers', 'Arizona Diamondbacks'
    ]

    # Add team names to the data
    for i, row in enumerate(data):
        row.insert(0, teams[i])
    # Write data to CSV file
    with open('team_stats.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers[:13])  # Only write the first 12 headers
        writer.writerows(data)

    print("Data has been written to team_stats.csv")

def team_standing_pull():
    url = 'https://www.mlb.com/standings/mlb'
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

    # Write data to CSV file
    with open('team_standings.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    print("Data has been written to team_standings.csv")

def combine_csv_files():
    # Read the CSV files
    with open('team_stats.csv', 'r') as stats_file:
        stats_reader = csv.reader(stats_file)
        stats_data = list(stats_reader)

    with open('team_standings.csv', 'r') as standings_file:
        standings_reader = csv.reader(standings_file)
        standings_data = list(standings_reader)

    # Combine the data
    combined_data = []
    for stats_row in stats_data:
        for standings_row in standings_data:
            if standings_row[0].__contains__(stats_row[0]):
                combined_data.append(stats_row + standings_row[1:])

    # Write the combined data to a new CSV file
    with open('combined_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(combined_data)

    print("Data has been written to combined_data.csv")


if __name__ == "__main__":

    # Create threads for team_stat_pull and team_standing_pull
    stat_thread = threading.Thread(target=team_stat_pull)
    standing_thread = threading.Thread(target=team_standing_pull)

    # Start the threads
    stat_thread.start()
    standing_thread.start()

    # Wait for both threads to complete
    stat_thread.join()
    standing_thread.join()

    # Execute the final function
    combine_csv_files()

    