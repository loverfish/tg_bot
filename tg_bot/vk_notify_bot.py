import logging
from telegram.ext import Updater, CommandHandler
from time import sleep

from tg_bot.setup_list import *
from tg_bot.utils import get_user_info_vk, create_online_report


updater = Updater(token=bot_assistant_tg_token)
dispatcher = updater.dispatcher


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def online(update, context):
    user_id = context.args[0] if len(context.args) == 1 else '111297977'
    while True:
        response = get_user_info_vk(user_id)
        if response.get('online'):
            message = f"Пользователь {response.get('first_name')} {response.get('last_name')} появился в сети вк"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            break
        sleep(180)


def report(update, context):
    user_id, duration = '111297977', 10
    if len(context.args) == 2:
        user_id = context.args[0]
        duration = int(context.args[1])
    context.bot.send_message(chat_id=update.effective_chat.id, text=create_online_report(user_id, duration))


start_handler = CommandHandler('start', start)
online_handler = CommandHandler('online', online)
report_handler = CommandHandler('report', report)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(online_handler)
dispatcher.add_handler(report_handler)

updater.start_polling()
updater.idle()
