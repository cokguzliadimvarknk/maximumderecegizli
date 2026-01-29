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

bot.polling()
