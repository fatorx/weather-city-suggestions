from datetime import datetime
import pytz

def get_current_time():
    timezone = pytz.timezone('America/Sao_Paulo')

    now = datetime.now(timezone)

    current = now.strftime("%Y-%m-%d %H:%M:%S")
    current = current + " " + str(now.tzinfo)

    return current