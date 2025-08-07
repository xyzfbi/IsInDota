from aiogram import types
from aiogram.filters import Command
from utils.player_status_manager import PlayerStatusManager
import logging

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self, status_manager: PlayerStatusManager):
        self.status_manager = status_manager
    
    def register_handlers(self, dp):
        dp.message.register(self.handle_status_request, Command(commands=["дима"]))
        dp.message.register(self.handle_help, Command(commands=["help", "помощь"]))
        dp.message.register(self.handle_stats, Command(commands=["stats", "статистика"]))
    

    
    async def handle_status_request(self, message: types.Message):
        try:
            from config.cfg import STEAM_ID
            status = await self.status_manager.get_player_status(STEAM_ID)
            await message.reply(status)
        except Exception as e:
            logger.error(f"Ошибка при обработке запроса статуса: {e}")
            await message.reply("Произошла ошибка при получении статуса игрока.")
    
    async def handle_help(self, message: types.Message):
        help_text = """
🤖 **Справка по командам бота:**

🎮 `/дима`, `/дота`, `/доте` - показать статус игрока в Dota 2
📊 `/stats` или `/статистика` - показать подробную статистику игрока
❓ `/help` или `/помощь` - показать эту справку

💬 **Как использовать:**
Просто напишите `/дима` в чате, и бот покажет текущий статус игрока.

🎮 **Что отслеживается:**
• Текущий статус в Dota 2
• Время, проведенное в игре
• История игровых сессий
        """
        await message.reply(help_text, parse_mode="Markdown")
    
    async def handle_stats(self, message: types.Message):
        try:
            from config.cfg import STEAM_ID
            status = await self.status_manager.get_player_status(STEAM_ID)
            
            stats_text = f"""
📊 **Статистика игрока:**

{status}

🕐 **Дополнительная информация:**
• Сейчас играет: {'Да' if self.status_manager.is_currently_playing() else 'Нет'}
• Последнее обновление: {self.status_manager.last_known_status or 'Нет данных'}
            """
            await message.reply(stats_text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Ошибка при получении статистики: {e}")
            await message.reply("Произошла ошибка при получении статистики.") 