from vkbottle import API
from vkbottle.bot import BotLabeler
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Устанавливаем токен ВКонтакте API
api = API(os.getenv('TOKEN'))
labeler = BotLabeler()

# Указываем идентификатор администратора группы VK
admin_id = os.getenv('ID')

# Указываем авторизационные данные OpenAI
GPT_key = os.getenv('AITOKEN')

DATABASE_URL = os.getenv("DATABASE_URL", "default_value_if_not_set")
