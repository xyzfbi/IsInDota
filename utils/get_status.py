from aiohttp import ClientSession
from datetime import datetime
from config.cfg import STEAM_API_KEY, DOTA2_APP_ID

async def get_player_status(steam_id):
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}'
    async with ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

                if data['response']['players']:
                    player = data['response']['players'][0]
                    if 'gameid' in player and player['gameid'] == DOTA2_APP_ID:
                        return f"{player['personaname']} сейчас играет в Dota 2!"
                    else:
                        return f"{player['personaname']} не в Dota 2."
                else:
                    return "Пользователь не найден."
        except Exception as e:
            return f"Ошибка при запросе к Steam API: {e}"

# Global variables for tracking game status
player_game_start_time = None
last_known_status = None

async def advanced_get_player_status(steam_id):
    global player_game_start_time, last_known_status
    url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}'
    async with ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

                if data['response']['players']:
                    player = data['response']['players'][0]
                    current_status = 'gameid' in player and player['gameid'] == DOTA2_APP_ID
                    if current_status:
                        if player_game_start_time is None:
                            player_game_start_time = datetime.now()
                        playtime = (datetime.now() - player_game_start_time).total_seconds()
                        last_known_status = f"{player['personaname']} сейчас играет в Dota 2! Время в игре: {format_duration(playtime)}."
                    else:
                        player_game_start_time = None
                        last_known_status = f"{player['personaname']} не в Dota 2."
                    return last_known_status
                else:
                    player_game_start_time = None
                    last_known_status = "Пользователь не найден."
                    return last_known_status
        except Exception as e:
            last_known_status = f"Ошибка при запросе к Steam API: {e}"
            return last_known_status

def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)} ч {int(minutes)} мин {int(seconds)} сек"
    elif minutes > 0:
        return f"{int(minutes)} мин {int(seconds)} сек"
    else:
        return f"{int(seconds)} сек"