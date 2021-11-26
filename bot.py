import logging
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, commandhandler
import os
from instaloader import Instaloader, Profile
import time


'''Coded by Anish Gowda 😃😃😃😃'''
L = Instaloader()
TOKEN = os.getenv("BOT_TOKEN")
APP_NAME = os.getenv("APP_NAME")
TELEGRAM_USERNAME = os.getenv("TELEGRAM_USERNAME")

START_MSG = '''*Welcome To the Bot🖐🖐*

_Send me anyones instagram username to get their DP_

*ex :* `mirshad_kvr`...., *etc*'''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def acc_type(val):
    if(val):
        return "🔒Private🔒"
    else:
        return "🔓Public🔓"

# Start the Bot


def start(update, context):
    id = update.message.chat_id
    name = update.message.from_user['username']
    update.message.reply_text(
        START_MSG,
        parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("How To Own & Use", url="")]]))

def help_msg(update, context):
    update.message.reply_text("Enter Your Instagram UserName")


def contact(update, context):
    keyboard = [[InlineKeyboardButton(
        "🗣️Contact✔️", url=f"telegram.me/{TELEGRAM_USERNAME}")], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Contact The Maker:', reply_markup=reply_markup)

# get the username and send the DP


def username(update, context):
    msg = update.message.reply_text("Downloading...")
    query = update.message.text
    chat_id = update.message.chat_id
    try:
        user = Profile.from_username(L.context, query)
        caption_msg = f'''♥️*Name*♥️: {user.full_name} \n😁*Followers*😁: {user.followers} \n🤩*Following*🤩: {user.followees}\
         \n🧐*Account Type*🧐: {acc_type(user.is_private)}\n🤪*Bio🤪*: {user.biography}\n👀*Midia*👀 {user.mediacount} \n\n*Thank You For Using The bot എന്നെ കൂടി follow ചെയ്യാൻ പറഞ്ഞേക്ക് 😅😅🤣😀😀 @dev_mirshad *'''
       
        context.bot.send_photo(
            chat_id=chat_id, photo=user.profile_pic_url,
            caption=caption_msg, parse_mode='MARKDOWN')
        msg.edit_text("finished.")
        time.sleep(5)
    except Exception:
        msg.edit_text("Try again 😕😕 Check the username correctly എന്തേലും പ്രശ്നം ഉണ്ടങ്കിൽ admin @dev_mirshad നെ അറിയിച്ചേക്ക് അവനല്ലേ ഉണ്ടാക്കിയെ 🤣🤣😂 അതോണ്ടാ ")



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater(TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_msg))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(MessageHandler(Filters.text, username))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN,
                          webhook_url=f"https://{APP_NAME}.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
