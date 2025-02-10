import psycopg2

from vkbottle.bot import BotLabeler, Message, rules
from functions.read_file import read_file
from database.database import connect_to_db


# Получение сообщений только из чатов
class ChatInfoRule(rules.ABCRule[Message]):
    async def check(self, message: Message) -> dict:
        chats_info = await message.ctx_api.messages.get_conversations_by_id(
            message.peer_id
        )
        return {"chat": chats_info.items[0]}


chat_labeler = BotLabeler()
chat_labeler.vbml_ignore_case = True
chat_labeler.auto_rules = [rules.PeerRule(from_chat=True), ChatInfoRule()]


# Хендлер для отправки списка команд по запросу "Команды"
@chat_labeler.message(text="Команды")
async def start(message):
    doc = await read_file("comand.txt")
    await message.answer(doc)


# Хендлер для отправки списка промокодов по запросу "Промокоды"
@chat_labeler.message(text="Промокоды")
async def promo(message):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM promo;")
        results = cursor.fetchall()

        if not results:
            await message.answer("Нет активных промокодов.")
            return

        response = "Список промокодов:\n"
        for promo_code, promo_link, promo_data in results:
            response += f"{promo_code} - {promo_link}, действует до {promo_data}\n"

        await message.answer(response)
    except psycopg2.Error as e:
        await message.answer(f"Произошла ошибка при получении списка промокодов: {e}")
    finally:
        cursor.close()
        connection.close()


# Хендлер для отправки списка ивентв по запросу "Иенты"
@chat_labeler.message(text="Ивенты")
async def ivent(message):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM ivent;")
        results = cursor.fetchall()

        if not results:
            await message.answer("Нет активных ивентов.")
            return

        response = "Список ивентов:\n"
        for ivent_name, ivent_link, ivent_data in results:
            response += f"{ivent_name} - {ivent_link}, действует до {ivent_data}\n"

        await message.answer(response)
    except psycopg2.Error as e:
        await message.answer(f"Произошла ошибка при получении списка ивентов: {e}")
    finally:
        cursor.close()
        connection.close()

# Хендлер для отправки списка полезных ресурсов от комьюнити по запросу "Полезные ссылки"
@chat_labeler.message(text="Полезные ссылки")
async def resources(message):
    doc = await read_file("resources.txt")
    await message.answer(doc)
