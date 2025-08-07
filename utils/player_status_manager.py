from datetime import datetime
from typing import Optional
from utils.steam_client import SteamClient
import logging

logger = logging.getLogger(__name__)

class PlayerStatusManager:
    def __init__(self, steam_client: SteamClient):
        self.steam_client = steam_client
        self.player_game_start_time: Optional[datetime] = None
        self.last_known_status: Optional[str] = None
        self.last_player_name: Optional[str] = None
    
    def format_duration(self, seconds: float) -> str:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours} ч {minutes} мин {secs} сек"
        elif minutes > 0:
            return f"{minutes} мин {secs} сек"
        else:
            return f"{secs} сек"
    
    async def get_player_status(self, steam_id: str) -> str:
        player_data = await self.steam_client.get_player_summary(steam_id)
        
        if not player_data:
            self.player_game_start_time = None
            self.last_known_status = "Пользователь не найден."
            return self.last_known_status
        
        player_name = player_data.get('personaname', 'Неизвестный игрок')
        current_status = self.steam_client.is_playing_dota2(player_data)
        
        if current_status:
            if self.player_game_start_time is None:
                self.player_game_start_time = datetime.now()
                logger.info(f"Игрок {player_name} начал играть в Dota 2")
            
            playtime = (datetime.now() - self.player_game_start_time).total_seconds()
            self.last_known_status = f"{player_name} сейчас играет в Dota 2! Время в игре: {self.format_duration(playtime)}."
        else:
            if self.player_game_start_time is not None:
                total_playtime = (datetime.now() - self.player_game_start_time).total_seconds()
                logger.info(f"Игрок {player_name} закончил играть. Общее время: {self.format_duration(total_playtime)}")
            
            self.player_game_start_time = None
            self.last_known_status = f"{player_name} не в Dota 2."
        
        self.last_player_name = player_name
        return self.last_known_status
    
    def get_last_status(self) -> Optional[str]:
        return self.last_known_status
    
    def is_currently_playing(self) -> bool:
        return self.player_game_start_time is not None 