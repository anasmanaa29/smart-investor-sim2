from apscheduler.schedulers.background import BackgroundScheduler
from telegram_bot import send_telegram_message
from reports import generate_performance_report, generate_daily_summary_report
from analyzer import analyze_stocks
from datetime import datetime
import pytz

GAZA_TIMEZONE = pytz.timezone("Asia/Gaza")
scheduler = BackgroundScheduler(timezone=GAZA_TIMEZONE)

def send_daily_analysis():
    results = analyze_stocks()
    message = "📊 تحليل يومي للأسهم:\n\n"
    for stock in results:
        message += f"{stock['symbol']} | التغير: {stock['change']:.2f}% | {stock['decision']}\n"
    send_telegram_message(message)

def send_weekly_report():
    report = generate_performance_report()
    send_telegram_message("📈 تقرير أسبوعي للمحفظة:\n\n" + report)

def start_scheduled_tasks():
    scheduler.add_job(send_daily_analysis, trigger='cron', hour=9, minute=30)
    scheduler.add_job(send_weekly_report, trigger='cron', day_of_week='fri', hour=17, minute=0)
    scheduler.start()
    print(f"[{datetime.now(GAZA_TIMEZONE)}] ✅ تم تشغيل الجدولة الذكية.")
