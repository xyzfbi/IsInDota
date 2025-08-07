import re
from aiogram import types
from aiogram.filters import Command
from typing import List, Optional
from utils.player_status_manager import PlayerStatusManager
import logging

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self, status_manager: PlayerStatusManager):
        self.status_manager = status_manager
        self.trigger_words = [r'\b(дима|дота|доте)\b']
        self.allowed_chat_types = ['group', 'supergroup']
    
    def register_handlers(self, dp):
        """Регистрирует все обработчики команд"""
        dp.message.register(self.handle_status_request, self.is_status_trigger)
        dp.message.register(self.handle_help, Command(commands=["help", "помощь"]))
        dp.message.register(self.handle_stats, Command(commands=["stats", "статистика"]))
    
    def is_status_trigger(self, message: types.Message) -> bool:
        """Проверяет, является ли сообщение триггером для запроса статуса"""
        if message.chat.type not in self.allowed_chat_types:
            return False
        
        if not message.text:
            return False
        
        return any(re.search(pattern, message.text, re.IGNORECASE) 
                  for pattern in self.trigger_words)
    
    async def handle_status_request(self, message: types.Message):
        """Обрабатывает запрос статуса игрока"""
        try:
            from config.cfg import STEAM_ID
            status = await self.status_manager.get_player_status(STEAM_ID)
            await message.reply(status)
        except Exception as e:
            logger.error(f"Ошибка при обработке запроса статуса: {e}")
            await message.reply("Произошла ошибка при получении статуса игрока.")
    
    async def handle_help(self, message: types.Message):
        """Показывает справку по командам"""
        help_text = """
🤖 **Справка по командам бота:**

📊 `/stats` или `/статистика` - показать статистику игрока
❓ `/help` или `/помощь` - показать эту справку

💬 **Автоматические триггеры:**
Просто упомяните "дима", "дота" или "доте" в сообщении, и бот покажет текущий статус игрока.

🎮 **Что отслеживается:**
• Текущий статус в Dota 2
• Время, проведенное в игре
• История игровых сессий
        """
        await message.reply(help_text, parse_mode="Markdown")
    
    async def handle_stats(self, message: types.Message):
        """Показывает статистику игрока"""
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