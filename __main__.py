from __future__ import print_function, division
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os
import time

from pprint import pprint
import apiai, json
TOKEN = os.environ["TOKEN"]


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='эТо ДнЕвНиКрУ BOOOT! \nОзнакомиться с доступными функциями ты сможешь, отправив /functions')

def functionCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Список функций: \n/gif - Команда, которая поднимет тебе настроение!")

def textMessage(bot, update):
    update.message.reply_text(update.message.text)

    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Что ты сказал?')



function_Command_handler = CommandHandler('functions', functionCommand)
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)


dispatcher.add_handler(function_Command_handler)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)

updater.idle()

