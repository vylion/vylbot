#!/usr/bin/env python3

import sys, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import *
from telegram import ParseMode
import logging
import argparse
import diceRoller as dice
import textwrap

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - Vylionbot',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

help_msg = """Reconozco los siguientes comandos:

/start - Saludo
/help - Envío este mensaje
/roll - Tiro dados
/quote [<autor>:] <mensaje> - Cito un <mensaje> con un <autor> opcional
/me <mensaje> - Te describo haciendo <mensaje>"""

idiot_msg = "you idiot. you big dunce. you utter buffoon"

def error(bot, update, error):
    logger.warn('Update "{u}" caused error "{e}"'.format(u=update, e=error))

def start(bot, update):
    update.message.reply_text("Hola, soy el bot personal de Vylion.")

def whoami(bot, update):
    msg = update.message
    user = update.message.from_user
    name = user.first_name + ' ' + user.last_name if user.last_name else user.first_name

    answer = "Estamos en "
    if msg.chat == "private":
        answer += "un chat privado; "
    else:
        answer += '{title}, un chat de tipo "{type}"; '.format(title=msg.chat.title, type=msg.chat.type)
    answer += "de id {cid}.\nEres {n}, ".format(cid=msg.chat.id, n=name)
    if user.username:
        answer += "con nombre de usuario {uname} y ".format(uname=user.username)
    answer += "de id {uid}.\n\n".format(uid=user.id)

    answer += "Tu mensaje tiene fecha de " + str(msg.date) + "."
    msg.reply_text(answer)

def get_comm_msg(update):
    msg = update.message.text.split(None, maxsplit=1)
    if len(msg) < 2:
        return ""
    return msg[1]

def help(bot, update):
    param = get_comm_msg(update).casefold().split()
    if len(param) > 0:
        if "roll" in param:
            update.message.reply_text(textwrap.dedent("""/roll <tirada(s)>:
            Se lanzan los dados descritos en el mensaje (usando notación de dados). Se pueden concatenar varias tiradas separándolas con ",", y se muestran los resultados por separado. Una tirada es una concatenación de dados separados con "+", sumando los resultados entre sí. También se pueden usar números enteros en vez de un dado (usando paréntesis para los números negativos), o parametrizar cualquier valor entero (como X o Y en "XdY") usando expresiones de una tirada.

            No compatible con dados Fudge ni con dados explosivos."""))
        if "quote" in param:
            update.message.reply_text(textwrap.dedent("""/quote [<autor>:] <mensaje>:
            Crea una cita con el mensaje dado. No hace falta poner comillas en el mensaje, ya las añado yo."""))
        if "me" in param:
            update.message.reply_text(textwrap.dedent("""/me <mensaje>:
            Crea un mensaje repitiendo el mensaje dado pero precedido por tu nombre.

            Inspirado en el comando "/me" de World of Warcraft."""))
        if "idiot" in param:
            update.message.reply_text(textwrap.dedent("""/idiot:
            Insulta adecuadamente. Si el mensaje con el comando es una respuesta a otro, responde al mismo."""))
        return
    update.message.reply_text(help_msg)

def quote(bot, update):
    msg = get_comm_msg(update)
    if len(msg) > 0:
        msg = msg.split(":", maxsplit=1)
        print('Processing quote: ' + str(msg))
        if len(msg) == 2:
            bot.sendMessage(update.message.chat.id, "\"" + msg[1].strip() + "\"\n- " + msg[0].strip())
        elif len(msg) == 1:
            bot.sendMessage(update.message.chat.id, "\"" + msg[0] + "\"")
    else:
        update.message.reply_text("Formato incorrecto. Es:\n/quote nombre: mensaje")

def meQuote(bot, update):
    msg = get_comm_msg(update)
    if len(msg) > 0:
        print('Processing "me" quote: ' + text)
        username = update.message.from_user.name
        bot.sendMessage(update.message.chat.id, username + " " + text)

def roll(bot, update):
    msg = get_comm_msg(update)
    if len(msg) > 0:
        print('Processing roll: ' + msg)
        try:
            roll_result = dice.parse_roll(msg)
            update.message.reply_text(update.message.from_user.name + roll_result, parse_mode=ParseMode.MARKDOWN)
        except:
            update.message.reply_text('Formato incorrecto. Consulta "/help roll" para más información')

def idiot(bot, update):
    message = update.message.reply_to_message
    if message:
        message.reply_text(idiot_msg)
    else:
        username = update.message.from_user.username
        bot.sendMessage(update.message.chat.id, username + " " + text)

def main():
    parser = argparse.ArgumentParser(description='A Telegram markov bot.')
    parser.add_argument('token', metavar='TOKEN', help='The Bot Token to work with the Telegram Bot API')

    args = parser.parse_args()

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(args.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("me", meQuote))
    dp.add_handler(CommandHandler("quote", quote))
    dp.add_handler(CommandHandler("roll", roll))
    dp.add_handler(CommandHandler("r", roll))
    dp.add_handler(CommandHandler("idiot", idiot))
    # dp.add_handler(CommandHandler("stop", stop))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    # dp.add_handler(MessageHandler(Filters.text, read))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
