
import requests
import logging
from persistence.constants import STEAM_COMMUNITY_APIKEY
import re

"""
    Steam community API related stuff.
    Psst - You guys should publish an official python binding ;)
"""


def steamid_by_community_url(steam_community_url: str) -> str | None:
    """ Given a community url, we convert it to a vanityurl and then query the API for the players SteamID. """
    
    # remove the erroneous parts of the steam_community_url
    match = re.search(r'^https:\/\/steamcommunity\.com\/id\/([a-zA-Z0-9_-]+)\/?$', steam_community_url)
    vanity_url = match.group(1) if match else None
    
    if not vanity_url:
        return None

    params = {
        'key': STEAM_COMMUNITY_APIKEY,
        "vanityurl": vanity_url
    }

    resp = requests.get('https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/', params=params)

    if resp.status_code == 200:
        return resp.json()['response']['steamid']


def player_has_bans(steamid: str | int) -> bool | None:
    """ Return whether the given user has any Bans or not. """
    params = {
        "key": STEAM_COMMUNITY_APIKEY,
        "steamids": steamid
    }
    
    resp = requests.get("https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/", params=params)
    try:
        player_data = resp.json()['players'][0]
        
        if player_data['CommunityBanned']:
            return True
        
        if player_data['VACBanned'] or player_data['NumberOfVACBans'] > 0:
            return True
        
        if player_data["DaysSinceLastBan"] > 0 or player_data["DaysSinceLastBan"] > 0:
            return True
            
        if player_data['EconomyBan'] != "none":
            return True
        
        return False
    except Exception as e:
        logging.error(f'Error checking {steamid} for player bans: Failed with {e}.')
        return None


def discordid_by_steamid(steamid: str | int) -> int:
    logging.error("Sorry, I can't implement this part for you guys, "
                  "as I don't have access to the DB/API that contains SteamID to Discord ID conversions.")
    return -1
