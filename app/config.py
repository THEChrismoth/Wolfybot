from vkbottle import API
from vkbottle.bot import BotLabeler
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Устанавливаем токен ВКонтакте API
api = API(os.getenv('VK_TOKEN'))
labeler = BotLabeler()

# Указываем идентификатор администратора группы VK
admin_id = os.getenv('ADMIN_ID')

# Указываем авторизационные данные OpenAI
GPT_key = os.getenv('AITOKEN')


