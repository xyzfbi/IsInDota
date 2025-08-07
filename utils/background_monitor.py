import asyncio
from typing import Optional
from utils.player_status_manager import PlayerStatusManager
import logging

logger = logging.getLogger(__name__)

class BackgroundMonitor:
    def __init__(self, status_manager: PlayerStatusManager, check_interval: int = 60):
        self.status_manager = status_manager
        self.check_interval = check_interval
        self.is_running = False
        self.task: Optional[asyncio.Task] = None
        self.last_status = None
    
    async def start_monitoring(self, steam_id: str):
        if self.is_running:
            logger.warning("Мониторинг уже запущен")
            return
        
        self.is_running = True
        self.task = asyncio.create_task(self._monitor_loop(steam_id))
        logger.info(f"Фоновый мониторинг запущен с интервалом {self.check_interval} секунд")
    
    async def stop_monitoring(self):
        if not self.is_running:
            return
        
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Фоновый мониторинг остановлен")
    
    async def _monitor_loop(self, steam_id: str):
        while self.is_running:
            try:
                current_status = await self.status_manager.get_player_status(steam_id)
                
                if current_status != self.last_status:
                    logger.info(f"Изменение статуса: {current_status}")
                    self.last_status = current_status
                
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Ошибка в цикле мониторинга: {e}")
                await asyncio.sleep(self.check_interval)
    
    def get_monitoring_info(self) -> dict:
        return {
            "is_running": self.is_running,
            "check_interval": self.check_interval,
            "last_status": self.last_status,
            "is_currently_playing": self.status_manager.is_currently_playing()
        } 