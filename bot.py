import os
import telebot
import requests
from telebot import types
from telebot.types import InlineKeyboardButton

BOT_TOKEN=os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am a bot which can tell you certain fact of random number in different categories")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, "To get some facts use next commands:\n " +
                     "/get_fact - to start to fill args to get random fact about certain number\n" +
                     "/help - to get help\n")


@bot.message_handler(commands=['get_fact'])
def get_fact(message):
    bot.send_message(message.from_user.id, "Enter a number that you want to check")
    bot.register_next_step_handler(message, get_number)


def get_number(message):
    print(message.text)
    choose_type_of_fact(message, int(message.text))


def choose_type_of_fact(message, num):
    markup = types.InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Math", callback_data="math " + str(num) + " " + str(message.from_user.id)),
               InlineKeyboardButton("Date", callback_data="date " + str(num) + " " + str(message.from_user.id)),
               InlineKeyboardButton("Trivia", callback_data="trivia " + str(num) + " " + str(message.from_user.id)))
    bot.send_message(message.from_user.id, 'Choose a type of fact', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    category, num, chat_id = call.data.split(" ")
    print(num, category, chat_id)
    r = requests.get(f"http://numbersapi.com/{num}/{category}")
    bot.send_message(chat_id, r.text)


bot.infinity_polling()
