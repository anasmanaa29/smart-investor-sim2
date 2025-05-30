from reports import generate_daily_summary_report
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

def schedule_evening_summary(bot, chat_id):
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Gaza"))
    scheduler.add_job(lambda: bot.send_message(chat_id, generate_daily_summary_report()),
                      'cron', hour=22, minute=0)
    scheduler.start()
    print(f"[{datetime.now()}] ✅ تم جدولة التقرير المسائي للمستخدم {chat_id}.")
