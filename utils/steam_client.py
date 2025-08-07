from aiohttp import ClientSession
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SteamClient:
    def __init__(self, api_key: str, dota2_app_id: str):
        self.api_key = api_key
        self.dota2_app_id = dota2_app_id
        self.base_url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    
    async def get_player_summary(self, steam_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}?key={self.api_key}&steamids={steam_id}"
        
        async with ClientSession() as session:
            try:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if data['response']['players']:
                        return data['response']['players'][0]
                    return None
            except Exception as e:
                logger.error(f"Ошибка при запросе к Steam API: {e}")
                return None
    
    def is_playing_dota2(self, player_data: Dict[str, Any]) -> bool:
        return 'gameid' in player_data and player_data['gameid'] == self.dota2_app_id 