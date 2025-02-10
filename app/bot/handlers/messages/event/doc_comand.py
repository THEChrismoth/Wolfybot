import psycopg2

from config.config import labeler
from functions.read_file import read_file
from database.database import connect_to_db

labeler.vbml_ignore_case = True


# Хендлер для отправки списка команд по запросу "Команды"
@labeler.message(payload={"command": "help"})
async def start(message):
    doc = await read_file("comand.txt")
    await message.answer(doc)


# Хендлер для отправки списка промокодов по запросу "Промокоды"
@labeler.message(payload={"command": "promo"})
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
@labeler.message(payload={"command": "ivent"})
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
@labeler.message(payload={"command": "link"})
async def resources(message):
    doc = await read_file("resources.txt")
    await message.answer(doc)


