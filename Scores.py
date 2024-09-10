from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

def get_match_details(date):
    url = f"https://www.besoccer.com/livescore/{date}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    
    match_details = []
    championships = soup.find("div", {'id': 'tableMatches'}).find_all("div", {'id': 'mod_panel'})
    
    for i in range(len(championships)):
        championship_title = championships[i].contents[1].find("span", {'class': 'va-m'}).text.strip()
        matches = championships[i].contents[1].find_all("a", {'class': 'match-link'})
        
        for match in matches:
            home_team = match.find("div", {'class': 'team_left'}).text.strip()
            away_team = match.find("div", {'class': 'team_right'}).text.strip()
            score = match.find("div", {'class': 'marker'}).text.strip()
            match_detail = OrderedDict({
                "Championship": championship_title,
                "Match": f"{home_team} {score} {away_team}", 
            })
            match_details.append(match_detail)
        if i == 5:  
            break

    return match_details

@app.route('/matches', methods=['GET'])
def matches():
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Please provide a date in the format yyyy-mm-dd"}), 400

    match_data = get_match_details(date)
    return jsonify(match_data)

if __name__ == '__main__':
    app.run(debug=True)
