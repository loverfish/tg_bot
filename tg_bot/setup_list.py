import os

from dotenv import load_dotenv


load_dotenv()

user_id_vk = os.getenv('user_id_vk')
api_token_vk = os.getenv('token_vk')

root_url_vk = 'https://api.vk.com/method/'
version_api_vk = '5.130'

bot_assistant_tg_token = os.getenv('bot_assistant_tg_token')
user_id_telegram = os.getenv('user_id_telegram')  # =chat_id
