from telegram import *
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler, Filters
import requests
import os


def get_Download_URL_From_API(url):
    API_URL = "https://youtube-video-info.p.rapidapi.com/video_formats"
    querystring = {"video": "edPREMPZ5RA"}

    headers = {
        'x-rapidapi-host': "youtube-video-info.p.rapidapi.com",
        'x-rapidapi-key': "39ad10fb39mshd9c362a66d3ee69p13a7ebjsn876d08b4e67f"  # This is your API key token. Keep it secret!
    }

    response = requests.request("GET", API_URL, headers=headers, params=querystring)
    data = response.json()
    return data['streams'][0]['url']


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='Welcome to URL downloader!\nPlease provide a valid url')


def textHandler(update: Update, context: CallbackContext) -> None:
    if update.message.parse_entities(types=MessageEntity.URL):
        update.message.reply_text(text='You sent a valid URL!', quote=True)


def main():
    PORT = int(os.environ.get('PORT', 5000))
    TOKEN = "YOUR BOT TOKEN"

    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, textHandler, run_async=True))
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
