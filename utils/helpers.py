import re
from typing import List, Optional
from datetime import datetime, timedelta

def validate_steam_id(steam_id: str) -> bool:
    """Проверяет корректность Steam ID"""
    # Steam ID должен быть числом длиной 17 символов
    return steam_id.isdigit() and len(steam_id) == 17

def extract_steam_id_from_url(url: str) -> Optional[str]:
    """Извлекает Steam ID из URL профиля Steam"""
    patterns = [
        r'steamcommunity\.com/profiles/(\d{17})',
        r'steamcommunity\.com/id/([^/]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def format_time_ago(dt: datetime) -> str:
    """Форматирует время в формате 'X минут назад'"""
    now = datetime.now()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days} дней назад"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} часов назад"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} минут назад"
    else:
        return "только что"

def parse_duration_string(duration_str: str) -> Optional[timedelta]:
    """Парсит строку длительности в timedelta"""
    # Пример: "2 ч 30 мин 45 сек"
    pattern = r'(\d+)\s*ч\s*(\d+)\s*мин\s*(\d+)\s*сек'
    match = re.match(pattern, duration_str)
    
    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    return None

def sanitize_username(username: str) -> str:
    """Очищает имя пользователя от потенциально опасных символов"""
    # Удаляем HTML теги и специальные символы
    cleaned = re.sub(r'<[^>]+>', '', username)
    cleaned = re.sub(r'[<>"\']', '', cleaned)
    return cleaned.strip()

def is_valid_telegram_username(username: str) -> bool:
    """Проверяет корректность Telegram username"""
    # Telegram username: 5-32 символа, буквы, цифры, подчеркивания
    pattern = r'^[a-zA-Z0-9_]{5,32}$'
    return bool(re.match(pattern, username)) 