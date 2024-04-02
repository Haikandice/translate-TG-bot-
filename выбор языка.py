from googletrans import Translator
from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import InlineQuery, InputTextMessageContent
from telebot import types

bot = AsyncTeleBot("6970562675:AAFpVGVWzh0c5tZEJM1RXAJ6ka6I2f_E0Kw", parse_mode=None)


# Dictionary to map language codes to human-readable names
language_names = {
    'en': 'English',
    'ru': 'Russian',
    'kk': 'Kazakh',
}

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message,'------\n'
                 + 'Здравствуй, '
                 + message.from_user.first_name
                 + ' \nПереведу с русского на английский \nИ с других языков на русский '
                 +'\n------')

# Command to set the translation language
@bot.message_handler(commands=['setlang'])
async def set_language(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for lang_code, lang_name in language_names.items():
        markup.add(types.InlineKeyboardButton(text=lang_name, callback_data=lang_code))
    await bot.send_message(message.chat.id, "Choose your language \nТіліңізді таңдаңыз \nВыберите ваш язык:", reply_markup=markup)

# Callback to handle language selection
@bot.callback_query_handler(func=lambda call: True)
async def callback_handler(call):
    user_id = call.from_user.id
    selected_lang = call.data
    # Store the selected language for the user
    # You can use a database or any other storage mechanism here
    # For demonstration purposes, I'm storing it in a dictionary
    # Replace this with your actual storage mechanism
    user_selected_languages[user_id] = selected_lang
    await bot.answer_callback_query(call.id, f"Language set to {language_names[selected_lang]}")

# Handle text messages for translation
@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    # Get the user's selected language, default to English if not set
    selected_lang = user_selected_languages.get(message.from_user.id, 'en')

    translator = Translator()

    if message.text:
        # Translate the message to the selected language
        translation = translator.translate(message.text, dest=selected_lang)
        await bot.send_message(message.chat.id, translation.text)

# Initialize the dictionary to store user-selected languages
user_selected_languages = {}

# Run the bot
asyncio.run(bot.infinity_polling())
