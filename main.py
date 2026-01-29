import telebot
from telebot import types
import requests
import configparser
import threading

# --- AYARLAR ---
TOKEN = "8468128322:AAHtXjuQrE5_PUhaRXfyon-zozLpySnsnaw"
bot = telebot.TeleBot(TOKEN)
KANAL_ID = "@izsizim"
SAHIBIM = "@yikmaz"

# Config'den Proxy Çekme
def get_proxies():
    config = configparser.ConfigParser()
    config.read('config.ini')
    all_proxies = []
    if not config.sections():
        return []
    for section in config.sections():
        if 'Sources' in config[section]:
            sources = config.get(section, 'Sources').strip().split('\n')
            for url in sources:
                try:
                    r = requests.get(url.strip(), timeout=5)
                    if r.status_code == 200:
                        all_proxies.extend(r.text.splitlines())
                except: continue
    return list(set(all_proxies))

# Kanal Kontrolü
def kanal_kontrol(user_id):
    try:
        durum = bot.get_chat_member(KANAL_ID, user_id).status
        return durum in ['member', 'administrator', 'creator']
    except:
        return False

# Butonlu Menü
def ana_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_sahibi = types.InlineKeyboardButton("👤 Sahibim", url=f"https://t.me/yikmaz")
    btn_kanal = types.InlineKeyboardButton("📢 Kanal", url="https://t.me/izsizim")
    btn_post = types.InlineKeyboardButton("🚀 Post Bot", callback_data="post_islem")
    markup.add(btn_post)
    markup.add(btn_sahibi, btn_kanal)
    return markup

@bot.message_handler(commands=['start', 'post'])
def handle_start_post(message):
    if not kanal_kontrol(message.from_user.id):
        bot.send_message(message.chat.id, f"⚠️ Botu kullanmak için önce {KANAL_ID} kanalına katılmalısın!")
        return
    bot.send_message(message.chat.id, "🌟 Hoş geldin! İşlem seçmek için butonları kullan:", reply_markup=ana_menu())

@bot.callback_query_handler(func=lambda call: call.data == "post_islem")
def ask_for_link(call):
    msg = bot.send_message(call.message.chat.id, "🔗 Lütfen görüntülenme gönderilecek post linkini gönderin:")
    bot.register_next_step_handler(msg, process_view_request)

def process_view_request(message):
    link = message.text
    if "t.me/" in link:
        bot.send_message(message.chat.id, "✅ Gönderiliyor... Eğer görüntülenme gelmezse @yikmaz hesabına ulaşın.")
        # Buraya mevcut görüntülenme basma döngünü/fonksiyonunu entegre edebilirsin.
    else:
        bot.send_message(message.chat.id, "❌ Hatalı link! Lütfen geçerli bir Telegram post linki atın.")

bot.infinity_polling()
