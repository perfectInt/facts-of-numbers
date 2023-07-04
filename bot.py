import os
import telebot
import requests
import datetime
from telebot import types
from telebot.types import InlineKeyboardButton

BOT_TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am a bot which can tell you a random fact of random number in different "
                          "categories\n" +
                 "Just say me any number.")


@bot.message_handler(func=lambda message: True)
def get_number(message):
    try:
        num = int(message.text)
        choose_type_of_fact(message, num)
    except ValueError:
        bot.send_message(message.from_user.id, "Sorry, I can work only with numbers")


def choose_type_of_fact(message, num):
    markup = types.InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Math", callback_data="math " + str(num) + " " + str(message.from_user.id)),
               InlineKeyboardButton("Date", callback_data="date " + str(num) + " " + str(message.from_user.id)),
               InlineKeyboardButton("Trivia", callback_data="trivia " + str(num) + " " + str(message.from_user.id)))
    bot.send_message(message.from_user.id, 'Choose a type of fact', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    category, num, chat_id = call.data.split(" ")
    if category == "date" and num > datetime.date.today().year:
        bot.answer_callback_query(chat_id, "No data")
    else:
        r = requests.get(f"http://numbersapi.com/{num}/{category}")
        bot.send_message(chat_id, r.text)


bot.infinity_polling()
