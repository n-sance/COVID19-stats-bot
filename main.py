#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import json
import ast

import xlrd
import datetime
import smtplib
from string import Template

import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

TOKEN = 'your token should be pasted here'

russia = '🇷🇺'
world = '🌎'
infected = '🚑'
covid = '🦠'
dead = '🖤'
survived = '💚'
graphic = '📊'
house = '🏠'
mask = '😷'
healthy = '👪'

url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"
url_global = "https://covid-19-data.p.rapidapi.com/totals"

update_id = None

USER_REQUEST, START, CANCEL, ELSE, AGAIN, HANDLE = range(6)

def start(update, context):
    reply_keyboard = [['Russia', 'World']]
    string_out = (graphic + " Check COVID-19 situation\n\n\n" + house + " Work from home\n" + mask + " Wear mask\n" + healthy + " Stay healthy! \n\n\n made by: @Hendrix37")
    update.message.reply_text(string_out,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return USER_REQUEST

def usr_request(update, context):
    user = update.message.text
    if (user == ('Russia')):
        response = requestForCountry(url, 'Russia')
        update.message.reply_text((russia + 'Russia'), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(getConfirmed(response), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(getDeaths(response), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(getRecovered(response), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(getTime(response), reply_markup=ReplyKeyboardRemove())
        return smth_else(update, context)
    if (user == ('World')):
        response = requestForGlobal(url_global)
        update.message.reply_text((world + 'World'), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(getGlobalConfirmed(response), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(getGlobalDeaths(response), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(getGlobalRecovered(response), reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('updated: Today', reply_markup=ReplyKeyboardRemove())
        return smth_else(update, context)
    return ELSE

def cancel(update, context):
    update.message.reply_text('Bye!\n\n\nInstagram: comandante37\nGithub: https://github.com/n-sance',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def smth_else(update, context):
    reply_keyboard = [['Cancel'], ['Again']]
    string_out = "..."
    update.message.reply_text(string_out, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return HANDLE

def hndler(update, context):
    user = update.message.text
    if update.message.text == 'Again':
        return start(update, context)
    if update.message.text == 'Cancel':
        return cancel(update, context)

def requestForGlobal(url):
    querystring = {"format":"undefined"}
    headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': "90cccd1147mshbcde39eb88447b0p1fce9bjsn4429dd2a10da"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return(response.text)

def getDeaths(response):
    d = json.loads(response)
    return(dead + '   Dead: ' + str(d["data"]["covid19Stats"][0]["deaths"]))

def getRecovered(response):
    d = json.loads(response)
    return(survived + '   Recovered: ' + str(d["data"]["covid19Stats"][0]["recovered"]))

def getConfirmed(response):
    d = json.loads(response)
    return(covid + '   Infected: ' + str(d["data"]["covid19Stats"][0]["confirmed"]))

def getGlobalConfirmed(response):
    d = json.loads(response)
    return(covid + '   Infected: ' + str(d[0]["confirmed"]))

def getGlobalDeaths(response):
    d = json.loads(response)
    return(dead + '   Dead: ' + str(d[0]["deaths"]))

def getGlobalRecovered(response):
    d = json.loads(response)
    return(survived + '   Recovered: ' + str(d[0]["recovered"]))

def getTime(response):
    d = json.loads(response)
    st = (d["data"]["lastChecked"]).split("T", 1)
    return(str("updated " + str(st[0])))

def requestForCountry(url, country):
    querystring = {"country":country}
    headers = {
    'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    'x-rapidapi-key': "90cccd1147mshbcde39eb88447b0p1fce9bjsn4429dd2a10da"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return(response.text)


def main():
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            USER_REQUEST: [MessageHandler(Filters.regex('^(Russia|World)$'), usr_request)],

            ELSE: [MessageHandler(Filters.all, smth_else)],

            HANDLE: [MessageHandler(Filters.regex('^(Again|Cancel)$'), hndler)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
