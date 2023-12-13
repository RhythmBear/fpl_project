import requests
from bs4 import BeautifulSoup

def get_team_and_fpl_link(player_link):
    """Get the link to the player's FPL page from the fplbot page using the link supplied and return the link plus the plauyer's team"""
    response = requests.get(player_link)
    response.encoding = 'utf-8'  # Set the encoding to UTF-8
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the team name
    team = soup.find('img', class_='shirt').parent.text
    fpl_team_div = soup.find('dt', string='FPL Team').parent
    fpl_link = fpl_team_div.find('a')['href']

    return {"team": team, "fpl_link": fpl_link}
    

def pull_data_from_fplbot_site():
    url = "https://www.fplbot.app/virtual-leagues/pl"

    response = requests.get(url)
    response.encoding = 'utf-8'  # Set the encoding to UTF-8
    soup = BeautifulSoup(response.content, "html.parser")

    # FInd Player divs
    player_divs = soup.find_all("div", {"class": "verified-table__player_inner"})

    # Get the player name and the link from the divs in the website.
    result_dict = []
    for div in player_divs:
        player_name = div.find('a').text
        player_link = f"https://www.fplbot.app{div.find('a')['href']}"

        # Get details from the player's page
        player_data = get_team_and_fpl_link(player_link)
        result_dict.append({
            "player_name": player_name,
            "player_link": player_link,
            "player_team": player_data['team'],
            "player_fpl_link": player_data['fpl_link']
        })
        
    return result_dict


site_data = pull_data_from_fplbot_site()
print(site_data)


