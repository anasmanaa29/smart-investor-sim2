import telebot
from config import TELEGRAM_TOKEN, TELEGRAM_USER_ID
from advisor import get_smart_advice
from analyzer import analyze_stocks
from capital_manager import update_balance, get_available_balance
from reports import generate_performance_report
from evening_report_scheduler import schedule_evening_summary
from flask import Flask
import threading

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    analyze_button = telebot.types.KeyboardButton('📊 تحليل الآن')
    advisor_button = telebot.types.KeyboardButton('🧠 المستشار الذكي')
    portfolio_button = telebot.types.KeyboardButton('📈 أداء المحفظة')
    balance_button = telebot.types.KeyboardButton('💰 الرصيد المتاح')
    markup.add(analyze_button, advisor_button, portfolio_button, balance_button)
    
    bot.send_message(message.chat.id, "أهلًا! 👋\nأنا البوت الاستثماري الذكي الخاص بك.\nاستخدم الأزرار أدناه للتفاعل معي.", reply_markup=markup)
    # جدولة التقرير المسائي للمستخدم الحالي
    schedule_evening_summary(bot, message.chat.id)

@bot.message_handler(commands=['advice'])
def send_advice(message):
    advice = get_smart_advice()
    bot.send_message(message.chat.id, advice)

@bot.message_handler(func=lambda message: message.text == '🧠 المستشار الذكي')
def advisor_button_handler(message):
    send_advice(message)

@bot.message_handler(commands=['analyze_now'])
def analyze_now(message):
    results = analyze_stocks()
    response = "📊 نتائج التحليل:\n\n"
    for stock in results:
        response += f"{stock['symbol']} | التغير: {stock['change']}% | {stock['decision']}\n"
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == '📊 تحليل الآن')
def analyze_button_handler(message):
    analyze_now(message)

@bot.message_handler(commands=['balance'])
def show_balance(message):
    balance = get_available_balance()
    bot.send_message(message.chat.id, f"💰 الرصيد المتاح: ${balance:.2f}")

@bot.message_handler(func=lambda message: message.text == '💰 الرصيد المتاح')
def balance_button_handler(message):
    show_balance(message)

@bot.message_handler(commands=['report'])
def send_report(message):
    report = generate_performance_report()
    bot.send_message(message.chat.id, "📈 تقرير الأداء:\n\n" + report)

@bot.message_handler(func=lambda message: message.text == '📈 أداء المحفظة')
def portfolio_button_handler(message):
    send_report(message)

def send_telegram_message(msg):
    bot.send_message(TELEGRAM_USER_ID, msg)

def run_bot():
    bot.infinity_polling()

app = Flask(__name__)

@app.route('/')
def home():
    return "Smart Investor Bot is running!"

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)
else:
    # للاستخدام عند استيراد الملف كوحدة
    def start_bot():
        bot.polling()
