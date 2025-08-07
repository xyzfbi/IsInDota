import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.cfg import TELEGRAM_TOKEN, STEAM_API_KEY, DOTA2_APP_ID, STEAM_ID
from utils.steam_client import SteamClient
from utils.player_status_manager import PlayerStatusManager
from utils.bot_handlers import BotHandlers
from utils.background_monitor import BackgroundMonitor

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DotaBot:
    def __init__(self):
        self.steam_client = SteamClient(STEAM_API_KEY, DOTA2_APP_ID)
        self.status_manager = PlayerStatusManager(self.steam_client)
        self.bot_handlers = BotHandlers(self.status_manager)
        self.background_monitor = BackgroundMonitor(self.status_manager, check_interval=60)
        
        self.bot = Bot(token=TELEGRAM_TOKEN)
        self.dp = Dispatcher()
        
        self.bot_handlers.register_handlers(self.dp)
    
    async def start(self):
        """Запускает бота"""
        try:
            logger.info("Запуск Dota 2 Status Bot...")
            
            await self.background_monitor.start_monitoring(STEAM_ID)
            
            await self.dp.start_polling(self.bot)
            
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            raise
    
    async def stop(self):
        """Останавливает бота"""
        try:
            await self.background_monitor.stop_monitoring()
            await self.bot.session.close()
            logger.info("Бот остановлен")
        except Exception as e:
            logger.error(f"Ошибка при остановке бота: {e}")

async def main():
    bot = DotaBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки...")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
    finally:
        await bot.stop()

if __name__ == '__main__':
    asyncio.run(main())