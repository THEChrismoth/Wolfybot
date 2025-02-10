from config.config import labeler, admin_id
from config.bot import bot
from vkbottle import BaseStateGroup, CtxStorage



# Определяем состояния
class States(BaseStateGroup):
    WAITING_FOR_FORWARD = "waiting_for_forward"

ctx_storage = CtxStorage()

labeler.vbml_ignore_case = True


# Хендлер для создания состояния ожидания сообщения для пересылки
@labeler.message(payload={"command": "admin"})
async def start_forwarding(message):
    await message.answer("Напишите сообщение, которое нужно переслать администратору.")
    await bot.state_dispenser.set(message.peer_id, States.WAITING_FOR_FORWARD)


# Хендлер для отправки сообщения от пользователя в состоянии ожидания сообщения
@labeler.message(state=States.WAITING_FOR_FORWARD)
async def message_to_forward(message):
    user = await bot.api.users.get(message.from_id)
    # Получаем текст сообщения
    remaining_text = "Вам сообщение :" + message.text

    # Отправляем сообщение администратору
    await bot.api.messages.send(user_id=admin_id, message=remaining_text, random_id=0)

    await message.answer("Ваше сообщение отправлено администратору.")

    # Возвращаем пользователя в начальное состояние
    await bot.state_dispenser.delete(message.peer_id)