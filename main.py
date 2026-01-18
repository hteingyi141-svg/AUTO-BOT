import telebot
from telebot import types
import os
from datetime import datetime

# ✅ Token from GitHub Actions Secret
BOT_TOKEN = os.getenv("7995464995:AAEdv6xN4YTsBuplrfNaxOvNLoc1uDP2K04")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

bot = telebot.TeleBot(BOT_TOKEN)

# folder for photos
PHOTO_DIR = "profile_photos"
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

def log(text):
    print(f"[{datetime.now()}] {text}")

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    chat_id = message.chat.id

    log("========== USER PROFILE LOG ==========")
    log(f"User ID    : {user.id}")
    log(f"Username   : {user.username}")
    log(f"First Name : {user.first_name}")
    log(f"Last Name  : {user.last_name}")

    bot.send_message(
        chat_id,
        f"👤 PROFILE\n"
        f"USER ID   : {user.id}\n"
        f"USERNAME  : @{user.username if user.username else 'မရှိပါ'}\n"
        f"NAME      : {user.first_name} {user.last_name or ''}"
    )

    photos = bot.get_user_profile_photos(user.id, limit=1)

    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)

        filename = f"{PHOTO_DIR}/{user.id}.jpg"
        with open(filename, "wb") as f:
            f.write(downloaded)

        log(f"Profile Photo Saved: {filename}")
        bot.send_photo(chat_id, file_id, caption="📸 Profile Photo")
    else:
        log("Profile Photo: NONE")
        bot.send_message(chat_id, "📸 Profile Photo မရှိပါ")

    log("=====================================")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_btn = types.KeyboardButton(
        text="ဆက်သွယ်ရန်နှိပ်ပါ",
        request_contact=True
    )
    markup.add(phone_btn)

    bot.send_message(chat_id, "📞 ဖုန်းနံပါတ် မျှဝေရန်", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def get_phone(message):
    user = message.from_user
    phone = message.contact.phone_number

    log("========== PHONE LOG ==========")
    log(f"User ID  : {user.id}")
    log(f"Username : {user.username}")
    log(f"Phone No : {phone}")
    log("==============================")

    bot.send_message(message.chat.id, "✅ ဖုန်းနံပါတ် လက်ခံရရှိပါပြီ")

log("AUTO-BOT started")
bot.polling(none_stop=True)
