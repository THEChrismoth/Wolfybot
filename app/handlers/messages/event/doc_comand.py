
from vkbottle.bot import MessageEvent

from config import labeler
from functions.read_file import read_file
from bot import bot

labeler.vbml_ignore_case = True


# Хендлер для отправки списка команд по запросу "Команды"
@labeler.message(payload={"command": "help"})
async def start(message):
    doc = await read_file("comand.txt")
    await message.answer(doc)


# Хендлер для отправки списка промокодов по запросу "Промокоды"
@labeler.message(payload={"command": "promo"})
async def promo(message):
    doc = await read_file("promo.txt")
    await message.answer(doc)


# Хендлер для отправки списка ивентв по запросу "Иенты"
@labeler.message(payload={"command": "ivent"})
async def ivent(message):
    doc = await read_file("ivent.txt")
    await message.answer(doc)


# Хендлер для отправки списка полезных ресурсов от комьюнити по запросу "Полезные ссылки"
@labeler.message(payload={"command": "link"})
async def resources(message):
    doc = await read_file("resources.txt")
    await message.answer(doc)


