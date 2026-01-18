import telebot
from telebot import types
import os
from datetime import datetime

BOT_TOKEN = "7995464995:AAEdv6xN4YTsBuplrfNaxOvNLoc1uDP2K04"
bot = telebot.TeleBot(BOT_TOKEN)

# folder for photos
if not os.path.exists("profile_photos"):
    os.makedirs("profile_photos")

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    chat_id = message.chat.id

    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    # ===== TEXT LOG =====
    print("========== USER PROFILE LOG ==========")
    print("User ID    :", user_id)
    print("Username   :", username)
    print("First Name :", first_name)
    print("Last Name  :", last_name)

    # Send profile text to user
    bot.send_message(
        chat_id,
        f"👤 PROFILE\n"
        f"USER ID   : {user_id}\n"
        f"USERNAME  : @{username if username else 'မရှိပါ'}\n"
        f"NAME      : {first_name} {last_name if last_name else ''}"
    )

    # ===== PROFILE PHOTO =====
    photos = bot.get_user_profile_photos(user_id, limit=1)

    if photos.total_count > 0:
        file_id = photos.photos[0][-1].file_id
        file_info = bot.get_file(file_id)
        downloaded = bot.download_file(file_info.file_path)

        filename = f"profile_photos/{user_id}.jpg"
        with open(filename, "wb") as f:
            f.write(downloaded)

        print("Profile Photo Saved:", filename)

        bot.send_photo(chat_id, file_id, caption="📸 Profile Photo")
    else:
        print("Profile Photo: NONE")
        bot.send_message(chat_id, "📸 Profile Photo မရှိပါ")

    print("=====================================")

    # ===== SHARE PHONE NUMBER BUTTON =====
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True
    )
    phone_btn = types.KeyboardButton(
        text="ဆက်သွယ်ရန်နှိပ်ပါ",
        request_contact=True
    )
    markup.add(phone_btn)

    bot.send_message(
        chat_id,
        "Thank",
        reply_markup=markup
    )

# ===== RECEIVE PHONE NUMBER =====
@bot.message_handler(content_types=['contact'])
def get_phone(message):
    user = message.from_user
    phone = message.contact.phone_number

    print("========== PHONE LOG ==========")
    print("User ID    :", user.id)
    print("Username   :", user.username)
    print("Phone No   :", phone)
    print("===============================")

    bot.send_message(
        message.chat.id,
        "✅ ဖုန်းနံပါတ် လက်ခံရရှိပါပြီ"
    )

bot.polling(none_stop=True)
