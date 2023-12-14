import requests
from fpl import FPL
from bs4 import BeautifulSoup
import tweepy 
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def connect_to_twitter_account():
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
)
    
    return client

def send_tweet(client, message: str):
    # Post a tweet with the given client 
    response = client.create_tweet(text=message)

def create_tweet(transfer, gameweek):
    date = datetime.today().strftime('%Y-%m-%d')
    gameweek = gameweek
    if transfer['transfer_type'] == 'sell':
        emoji = '🔻' 
        core_message = f"⚠️ {emoji} [{date}] [{transfer['team']}] {transfer['user']} has transferred OUT their own teammate {transfer['transfer_out']}! (🔄 {transfer['transfer_in']}) #FPL #GW{gameweek}"
    elif transfer['transfer_type'] == 'buy':
        emoji = '✅'
        core_message = f"⚠️ {emoji} [{date}] [{transfer['team']}] {transfer['user']} has transferred IN their own teammate {transfer['transfer_in']}! (🔄 {transfer['transfer_out']}) #FPL #GW{gameweek}"

    return core_message


def get_player_gameweek_squad(
        player_id: int, 
        gameweek: int ):
    """Get the 15 man squad for the players in """

    # Contact the FPL API


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


# site_data = pull_data_from_fplbot_site()
# print(site_data)


#  