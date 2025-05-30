from telegram_bot import start_bot
from scheduler import start_scheduled_tasks

if __name__ == "__main__":
    start_scheduled_tasks()
    start_bot()
