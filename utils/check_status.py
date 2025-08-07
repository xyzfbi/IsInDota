import utils.get_status as get_status
import asyncio

async def check_status_periodically(steam_id):
    while True:
        await get_status.advanced_get_player_status(steam_id)
        await asyncio.sleep(60)