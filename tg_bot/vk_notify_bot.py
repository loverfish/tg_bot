import logging
from threading import Thread

from telegram.ext import Updater, CommandHandler
from time import sleep

from tg_bot.setup_list import *
from tg_bot.utils import get_user_info_vk, create_online_report, get_user_fullname

updater = Updater(token=bot_assistant_tg_token)
dispatcher = updater.dispatcher


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def notify_user_is_online(update, context):
    user_id = context.args[0] if len(context.args) == 1 else user_id_vk
    while True:
        response = get_user_info_vk(user_id)
        if response.get('online'):
            message = f"Пользователь {response.get('first_name')} {response.get('last_name')} появился в сети вк"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            break
        sleep(80)


def online_stream(update, context):
    Thread(target=notify_user_is_online, args=(update, context)).start()


def report_user_online(update, context):
    user_id, duration = user_id_vk, 10
    if len(context.args) == 2:
        user_id = context.args[0]
        duration = int(context.args[1])
    message = create_online_report(user_id, duration)
    if not message:
        message = f"Пользователь {get_user_fullname(user_id)} не появлялся в сети"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def report_stream(update, context):
    Thread(target=report_user_online, args=(update, context)).start()


start_handler = CommandHandler('start', start)
online_handler = CommandHandler('online', online_stream)
report_handler = CommandHandler('report', report_stream)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(online_handler)
dispatcher.add_handler(report_handler)

updater.start_polling()
updater.idle()
