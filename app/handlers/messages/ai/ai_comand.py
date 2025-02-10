from vkbottle import BaseStateGroup, CtxStorage, Keyboard, KeyboardButtonColor, Text

from functions.gpt_request import gpt_request, gpt_image
from config import labeler
from bot import bot


# Определяем состояния
class States(BaseStateGroup):
    WAITING_FOR_REQUEST = "waiting_for_request"
    WAITING_FOR_IMAGE = "waiting_for_image"


ctx_storage = CtxStorage()

labeler.vbml_ignore_case = True

ai_keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text("режим gpt", payload={"command": "gpt"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("вернуться", payload={"command": "back_start"}), color=KeyboardButtonColor.PRIMARY)
    .row()
    .add(Text("режим генирации картинок", payload={"command": "draw"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Оплатить подписку", payload={"command": "pay"}), color=KeyboardButtonColor.SECONDARY)

).get_json()

off_keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Выключить"), color=KeyboardButtonColor.POSITIVE)
).get_json()


@labeler.message(payload={"command": "aionn"})
async def aionn(message):
    await message.answer("включен режим нейросети", keyboard=ai_keyboard)


# Хендлер для создания состояния ожидания запроса к нейросети
@labeler.message(payload={"command": "gpt"})
async def start_forwarding(message):
    await message.answer("Напишите ваш запрос нейросети", keyboard=off_keyboard)
    await bot.state_dispenser.set(message.peer_id, States.WAITING_FOR_REQUEST)


# Хендлер для отправки ответа нейросети пользователю состояния ожидания запроса
@labeler.message(state=States.WAITING_FOR_REQUEST)
async def message_to_forward(message):
    user_id = message.peer_id

    if message.text == "Выключить":
        # Возвращаем пользователя в начальное состояние
        await bot.state_dispenser.delete(message.peer_id)

        await message.answer("Вы вышли из режима gpt", keyboard=ai_keyboard)
    else:
        answer = await gpt_request(message.text, user_id)

        await message.answer(answer.choices[0].message.content, keyboard=off_keyboard)


# Хендлер для создания состояния ожидания запроса для рисовки изображения
@labeler.message(payload={"command": "draw"})
async def start_forwarding(message):
    await message.answer("Опишите что вы хотите чтобы я нарисовал", keyboard=off_keyboard)
    await bot.state_dispenser.set(message.peer_id, States.WAITING_FOR_IMAGE)


# Хендлер для отправки изображения полученного нейросетью
@labeler.message(state=States.WAITING_FOR_IMAGE)
async def message_to_forward(message):
    user_id = message.peer_id

    if message.text == "Выключить":
        # Возвращаем пользователя в начальное состояние
        await bot.state_dispenser.delete(message.peer_id)

        await message.answer("Вы вышли из режима генерации картинок", keyboard=ai_keyboard)
    else:
        answer = await gpt_image(message.text, user_id)

        await message.answer(answer.data[0].url, keyboard=off_keyboard)

        # Возвращаем пользователя в начальное состояние
        await bot.state_dispenser.delete(message.peer_id)
