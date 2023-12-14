from fpl import FPL
import aiohttp
import time
import asyncio
from utils import *

load_dotenv()

async def get_user_transfers(fpl_session, user_id, gameweek_no)-> dict:    
    user = await fpl_session.get_user(user_id)

    result_dict = {
         "user": str(user),
         "gameweek": gameweek_no,
         "transfer_type": '',
         "transfers_in": [],
         "transfers_out": []}
    # print(user)

    # Retrieve User Transfers
    user_transfers = await user.get_transfers(gameweek=gameweek_no)

    # GEt the Id's for the players that were transfered in and out
    players_in_ids = [transfer['element_in'] for transfer in user_transfers] 
    players_out_ids = [transfer['element_out'] for transfer in user_transfers]
    
    # Retrieve the actual Player details for each transfer
    if players_in_ids:
        players_in = await fpl_session.get_players(players_in_ids)
        result_dict['transfers_in'] = [str(player) for player in players_in]
        result_dict['transfer_type'] = 'buy'
    if players_out_ids:
        players_out = await fpl_session.get_players(players_out_ids)
        result_dict['transfers_out'] = [str(player) for player in players_out]
        result_dict['transfer_type'] = 'sell'

    # Get the actual results and convert them to strings append them to the dictionary.
    
    

    
    # for transfer in user_transfers:
    #         player_in = await fpl_session.get_player(transfer['element_in'], return_json=False)
    #         player_out = await fpl_session.get_player(transfer['element_out'], return_json=False)
    #         result_dict['transfers_in'].append(player_in)
    #         result_dict['transfers_out'].append(player_out)
            
    return result_dict



async def check_and_update_transfer_result(transfer_result, owner_team):
    """
    Get The message results and get the Users that transfered out/in a player in their club
    """
    all_messages_info = []
    
    for index, transfer in enumerate(transfer_result['transfers_in']):
        club = transfer.split(' - ')[-1]
        if club == owner_team:
            new_message = {
                "user": transfer_result['user'].split(' - ')[0],
                "team": owner_team,
                "transfer_type": "buy",
                "transfer_in": transfer.split(' - ')[0],
                "transfer_out": transfer_result['transfers_out'][index].split(' - ')[0]

                }
            all_messages_info.append(new_message)

    for index, transfer in enumerate(transfer_result['transfers_out']):
        club = transfer.split(' - ')[-1]
        if club == owner_team:
            new_message = {
                "user": transfer_result['user'].split(' - ')[0],
                "team": owner_team,
                "transfer_type": "sell",
                "transfer_out": transfer.split(' - ')[0],
                "transfer_in": transfer_result['transfers_in'][index].split(' - ')[0]
                }
            all_messages_info.append(new_message)

    return all_messages_info

            

    

async def main():
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        
        # Get Start Time
        start_time = time.time()
        gameweek_no = 10
        # Get the Transfer Data for the specified user
        transfer_result = await get_user_transfers(fpl, 8991835, gameweek_no
        
                                                   )
        print(transfer_result)

        all_messages = await check_and_update_transfer_result(transfer_result, "Chelsea")
        print(all_messages)

        for message in all_messages:
            twitter_client = connect_to_twitter_account()
            tweet = create_tweet(message, gameweek_no)
            print(tweet)
            send_tweet(twitter_client, tweet)
            
        print(f"Total Run time is {time.time() - start_time}")

            

    await session.close()

# Python 3.7+
asyncio.run(main())