from __future__ import print_function, division
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os
import time

from pprint import pprint
import apiai, json
TOKEN = os.environ["TOKEN"]

n = 0

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='эТо ДнЕвНиКрУ BOOOT! \nОзнакомиться с доступными функциями ты сможешь, отправив /functions')


def functionCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Список функций: \n/xxx -")
    update.message(textMessage(bot, update))
    global n
    n = 1
    return n


def textMessage(bot, update):
    global n
    if n != 0:
        update.message.reply_text(update.message.text)
        return update.message.text
        #bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text="lol")






function_Command_handler = CommandHandler('functions', functionCommand)
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)


dispatcher.add_handler(function_Command_handler)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

updater.start_polling(clean=True)

updater.idle()

