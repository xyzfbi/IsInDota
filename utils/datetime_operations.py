def format_duration(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{int(hours)} ч {int(minutes)} мин {int(seconds)} сек"
    elif minutes > 0:
        return f"{int(minutes)} мин {int(seconds)} сек"
    else:
        return f"{int(seconds)} сек"