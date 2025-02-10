from config.config import labeler

from vkbottle import  Keyboard, KeyboardButtonColor, Text

labeler.vbml_ignore_case = True

event_keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Список команд", payload={"command": "help"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("рассылки", payload={"command": "mailing"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("промокоды", payload={"command": "promo"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("ивенты", payload={"command": "ivent"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("полезные ссылки", payload={"command": "link"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("связаться с администратором", payload={"command": "admin"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Вернуться", payload={"command": "back_start"}), color=KeyboardButtonColor.PRIMARY)

).get_json()

@labeler.message(payload={"command": "eventon"})
async def start_forwarding(message):
    await message.answer("выберите действие", keyboard=event_keyboard)

@labeler.message(payload={"command": "evenback"})
async def start_forwarding(message):
    await message.answer("выберите действие", keyboard=event_keyboard)