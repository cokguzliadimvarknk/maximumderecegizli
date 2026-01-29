import telebot
import requests
from flask import Flask
import threading

# --- AYARLAR ---
API_TOKEN = '8468128322:AAHtXjuQrE5_PUhaRXfyon-zozLpySnsnaw'
bot = telebot.TeleBot(API_TOKEN)

def get_proxies():
    # İnternetten taze ve bedava proxyleri çeker
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        r = requests.get(url)
        return r.text.splitlines()
    except:
        return []

def view_engine(post_url):
    proxies = get_proxies()
    for ip in proxies:
        try:
            # Görüntülenme işlemini simüle eder
            requests.get(post_url, proxies={"http": ip, "https": ip}, timeout=5)
        except:
            continue

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Link gönder, beleş görüntülenme basayım!")

@bot.message_handler(func=lambda m: "t.me/" in m.text)
def handle(message):
    bot.reply_to(message, "🚀 Başlatıldı!")
    threading.Thread(target=view_engine, args=(message.text,)).start()

import telebot
import requests
import threading

# --- AYARLAR ---
API_TOKEN = '8468128322:AAHtXjuQrE5_PUhaRXfyon-zozLpySnsnaw'
bot = telebot.TeleBot(API_TOKEN)

def get_proxies():
    # İnternetten taze ve bedava proxyleri çeker
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        r = requests.get(url)
        return r.text.splitlines()
    except:
        return []

def view_engine(post_url):
    proxies = get_proxies()
    for ip in proxies:
        try:
            # Görüntülenme işlemini simüle eder
            requests.get(post_url, proxies={"http": ip, "https": ip}, timeout=5)
        except:
            continue

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Link gönder, beleş görüntülenme basayım!")

@bot.message_handler(func=lambda m: "t.me/" in m.text)
def handle(message):
    bot.reply_to(message, "🚀 Başlatıldı!")
    threading.Thread(target=view_engine, args=(message.text,)).start()


app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Aktif ve Calisiyor!"

def run_bot():
    try:
        print("Bot dinlemeye basladi...")
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Hata olustu: {e}")

if __name__ == "__main__":
    # Botu arka planda (thread) baslat
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Flask sunucusunu ana kolda baslat (Vercel bunu bekler)
    app.run(host='0.0.0.0', port=5000)
