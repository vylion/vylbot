#!/usr/bin/env python3

import sys, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import *
import logging
import argparse

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

names = ["vylion's bot", "vylion bot", "vyl's bot", "vyl bot", "vylbot", "vylionbot", "bot de vyl"]
discoFire = False

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def start(bot, update):
    update.message.reply_text("Hola, soy el bot de pruebas de Vylion.")

def help(bot, update):
    update.message.reply_text("""Los comandos que acepto son:

/start - saludo
/help - Envío este mensaje.
/echo mensaje - Repito el mensaje.
/quote nombre: mensaje - Cito a [nombre] diciendo [mensaje].
/me mensaje - Te describo usando [mensaje].

También respondo a varias palabras clave por cuenta propia.
    """)

def echo(bot, update):
    text = update.message.text.split(None, maxsplit=1)
    if len(text) == 2:
        text = text[1]
        print("Processing echo: " + text)
        if update.message.text.startswith("/echo"):
            update.message.reply_text("Qué manía con los nested /echo")
        else:
            bot.sendMessage(update.message.chat.id, "\"" + text + "\"")

def quote(bot, update):
    text = update.message.text.split(None, maxsplit=1)
    if len(text) == 2:
        text = text[1]
        text = text.split(":", maxsplit=1)
        print("Processing quote: \"" + text[1] + "\" by \"" + text[0] + "\"")
        if len(text) == 2:
            bot.sendMessage(update.message.chat.id, "\"" + text[1] + "\"\n- " + text[0])
        else:
            update.message.reply_text("Formato incorrecto. Es:\n/quote nombre: mensaje")
    else:
        update.message.reply_text("Formato incorrecto. Es:\n/quote nombre: mensaje")

def meQuote(bot, update):
    text = update.message.text.split(None, maxsplit=1)
    if len(text) > 1:
        text = text[1]
        print("Processing *me* quote: " + text)
        username = update.message.from_user.name
        bot.sendMessage(update.message.chat.id, username + " " + text)

def mentioned(update):
    text = update.message.text.casefold()
    for name in names:
        if name in text:
            update.message.reply_text("That's me!")
            return True
    return False

def read(bot, update):
    text = update.message.text.casefold()

    messaged = False
    if "biene" in text:
        update.message.reply_text("Alessio")
        messaged = True
    if "lmao" in text:
        update.message.reply_text("ayy")
        messaged = True
    elif "ayy" in text:
        update.message.reply_text("lmao")
        messaged = True
    elif "qyy" in text:
        update.message.reply_text(">failing this hard")
        messaged = True
    if "fire in the" in text:
        global discoFire
        if "taco bell" in text:
            discoFire = True
        if discoFire:
            update.message.reply_text("Fire in the Gates of Hell!")
            discoFire = False
        else:
            update.message.reply_text("Fire in the Taco Bell!")
            discoFire = True
        messaged = True
    if ("danger danger" in text) or ("danger, danger" in text):
        update.message.reply_text("High Voltage!")
        messaged = True
    if "when we touch" in text:
        update.message.reply_text("When we kiss!")
        messaged = True
    if "h3h3" in text:
        update.message.reply_text("Wow Ethan, great moves, keep it up! Proud of you")
        messaged = True
    if "exodia" in text:
        update.message.reply_text("EXODIA, ANIQUILA")
        messaged = True
    if "kebab" in text:
        update.message.reply_text("https://www.youtube.com/watch?v=ocW3fBqPQkU")
        messaged = True
    if ("vaporwave" in text) or ("v a p o r w a v e" in text) or ("﻿ｖａｐｏｒｗａｖｅ" in text):
        update.message.reply_text("ＡＥＳＴＨＥＴＩＣＳ")
        messaged = True
    elif ("aesthetics" in text) or ("a e s t h e t i c s" in text) or ("﻿﻿ａｅｓｔｈｅｔｉｃｓ" in text):
        update.message.reply_text("﻿﻿ｎｉｃｅ")
        messaged = True
    if "me voy" in text and str(chat.id) == "-1001036575277":
        update.message.reply_text("﻿﻿\"Me voy del Whatsapp, adiós.\"")
        messaged = True

    if not messaged:
        mentioned(update)

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
    # dp.add_handler(CommandHandler("stop", stop))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.text, read))

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
