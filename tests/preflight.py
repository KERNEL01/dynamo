import logging


def preflight():
    print('Good luck on all the projects you guys are working on, you do some amazing work. with love, from Rich.')
    test_len_discord_token()
    test_steam_discord_integration()
    
    
def test_len_discord_token():
    from persistence.constants import DISCORD_TOKEN
    if not len(DISCORD_TOKEN) == 72:
        raise RuntimeError("Oops, your discord token doesn't look right.")


def test_steam_discord_integration():
    from util.steam import discordid_by_steamid
    if discordid_by_steamid(76561197984095565) == -1:
        logging.warning("Please edit the function util.steam.discordid_by_steamid to confirm users match their ids. "
                        "You may continue, but users can provide any steamcommunity link without confirmation.")
