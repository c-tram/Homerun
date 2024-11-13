from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

# Dictionary mapping team IDs to team names
team_dict = {
    133: "Oakland Athletics",
    147: "New York Yankees",
    145: "Chicago White Sox",
    118: "Kansas City Royals",
    146: "Miami Marlins",
    115: "Colorado Rockies",
    121: "New York Mets",
    116: "Detroit Tigers",
    158: "Milwaukee Brewers",
    120: "Washington Nationals",
    134: "Pittsburgh Pirates",
    137: "San Francisco Giants",
    114: "Cleveland Guardians",
    110: "Baltimore Orioles",
    109: "Arizona Diamondbacks",
    108: "Los Angeles Angels",
    139: "Tampa Bay Rays",
    111: "Boston Red Sox",
    135: "San Diego Padres",
    113: "Cincinnati Reds",
    136: "Seattle Mariners",
    138: "St. Louis Cardinals",
    143: "Philadelphia Phillies",
    142: "Minnesota Twins",
    112: "Chicago Cubs",
    141: "Toronto Blue Jays",
    144: "Atlanta Braves",
    117: "Houston Astros",
    140: "Texas Rangers",
    119: "Los Angeles Dodgers"
}

def get_team_name(svg_url):
    # Extract the team ID from the SVG URL
    team_id = int(svg_url.split('/')[-1].split('.')[0])
    # Return the team name from the dictionary
    return team_dict.get(team_id, "Unknown Team")
