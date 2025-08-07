import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
DOTA2_APP_ID = os.getenv('DOTA2_APP_ID')
STEAM_ID = os.getenv('STEAM_ID')
TARGET_PLAYER_NAME=os.getenv('TARGET_PLAYER_NAME')
YOUR_STEAM_ID=os.getenv('YOUR_STEAM_ID')