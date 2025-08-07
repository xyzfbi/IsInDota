# 🎮 Dota 2 Status Bot

Telegram бот для отслеживания статуса игрока в Dota 2 через Steam API.

## ✨ Возможности

- 🔍 **Отслеживание статуса** - проверка, играет ли игрок в Dota 2
- ⏱️ **Время в игре** - подсчет времени, проведенного в игре
- 🔄 **Фоновый мониторинг** - автоматическое обновление статуса каждые 60 секунд
- 💬 **Автоматические триггеры** - реакция на ключевые слова в чате
- 📊 **Статистика** - команды для получения подробной информации
- 🛡️ **Обработка ошибок** - надежная работа с API и сетью

## 🏗️ Архитектура

Проект построен с использованием объектно-ориентированного подхода:

```
├── main.py                 # Главный файл приложения
├── config/
│   └── cfg.py             # Конфигурация и переменные окружения
├── utils/
│   ├── steam_client.py    # Клиент для работы с Steam API
│   ├── player_status_manager.py  # Управление статусом игрока
│   ├── bot_handlers.py    # Обработчики команд бота
│   ├── background_monitor.py     # Фоновый мониторинг
│   └── helpers.py         # Вспомогательные функции
└── requirements.txt       # Зависимости проекта
```

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd IsInDota_BOTR
```

### 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
Создайте файл `.env` в корне проекта:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
STEAM_API_KEY=your_steam_api_key
STEAM_ID=target_player_steam_id
DOTA2_APP_ID=570
TARGET_PLAYER_NAME=PlayerName
YOUR_STEAM_ID=your_steam_id
```

### 5. Запуск бота
```bash
python main.py
```

## 📋 Команды бота

### Команды для получения статуса
- `/дима`, `/дота`, `/доте` - показать статус игрока в Dota 2

### Дополнительные команды
- `/help` или `/помощь` - показать справку
- `/stats` или `/статистика` - показать статистику игрока

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|---------|
| `TELEGRAM_TOKEN` | Токен Telegram бота | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `STEAM_API_KEY` | Ключ Steam API | `ABCDEF1234567890ABCDEF1234567890` |
| `STEAM_ID` | Steam ID отслеживаемого игрока | `76561198012345678` |
| `DOTA2_APP_ID` | ID приложения Dota 2 | `570` |

### Настройка интервалов
В файле `main.py` можно изменить интервал проверки статуса:
```python
self.background_monitor = BackgroundMonitor(self.status_manager, check_interval=60)
```

## 🛠️ Разработка

### Добавление новых команд
1. Создайте новый метод в классе `BotHandlers`
2. Зарегистрируйте обработчик в методе `register_handlers`

### Расширение функционала Steam API
1. Добавьте новые методы в класс `SteamClient`
2. Обновите `PlayerStatusManager` для использования новых данных

### Логирование
Проект использует стандартный модуль `logging` Python. Логи записываются в консоль с уровнем INFO.

## 📝 Примеры использования

### Получение статуса игрока
```python
from utils.steam_client import SteamClient
from utils.player_status_manager import PlayerStatusManager

steam_client = SteamClient(api_key, dota2_app_id)
status_manager = PlayerStatusManager(steam_client)

status = await status_manager.get_player_status(steam_id)
print(status)
```

### Фоновый мониторинг
```python
from utils.background_monitor import BackgroundMonitor

monitor = BackgroundMonitor(status_manager, check_interval=30)
await monitor.start_monitoring(steam_id)
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи в консоли
2. Убедитесь в корректности переменных окружения
3. Проверьте доступность Steam API
4. Создайте Issue в репозитории 