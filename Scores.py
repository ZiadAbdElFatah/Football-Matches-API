import requests
from bs4 import BeautifulSoup
import os
import csv

directory = 'Documents'
file_path = os.path.join(directory, 'matches.csv')

os.makedirs(directory, exist_ok=True)

date = input('Enter date in yyyy-mm-dd format: ')
page = requests.get(f"https://www.besoccer.com/livescore/{date}")

def main(page):
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    match_details = []
    
    championships = soup.find("div", {'id': 'tableMatches'}).find_all("div", {'id': 'mod_panel'})
    
    def get_match_info(championships):
        for i in range(len(championships)):
            championship_title = championships[i].contents[1].find("span", {'class': 'va-m'}).text.strip()
            matches = championships[i].contents[1].find_all("a", {'class': 'match-link'})
            for match in matches:
                home_team = match.find("div", {'class': 'team_left'}).text.strip()
                away_team = match.find("div", {'class': 'team_right'}).text.strip()
                score = match.find("div", {'class': 'marker'}).text.strip()
                match_details.append({"Championship":championship_title, "Home Team":home_team, "Result/Time":score, "Away Team":away_team})
            if i == 5:
                break
    get_match_info(championships)
    
    keys = match_details[0].keys()
    
    with open(file_path, 'w', newline='') as output:
        dict_writer = csv.DictWriter(output, keys)
        dict_writer.writeheader()
        dict_writer.writerows(match_details)
        print("File created")
    
main(page)