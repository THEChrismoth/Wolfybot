from config import labeler
from bot import bot
from vkbottle import PhotoMessageUploader, Keyboard, KeyboardButtonColor, Text
from functions.read_file import read_file

photo_uploader = PhotoMessageUploader(bot.api)

labeler.vbml_ignore_case = True

start_keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text("режим ассистента", payload={"command": "eventon"}), color=KeyboardButtonColor.POSITIVE)
    .add(Text("режим нейросетей", payload={"command": "aionn"}), color=KeyboardButtonColor.POSITIVE)
).get_json()


@labeler.message(payload={"command": "back_start"})
async def start_forwarding(message):
    await message.answer("вы вернулись в главное меню", keyboard=start_keyboard)


# Хендлер для отправки стартового сообщения
@labeler.message(text="Начать")
async def Photo_upload(message):
    doc = await read_file("start.txt")
    photo = await photo_uploader.upload(
        file_source="images/wolf.png",
        peer_id=message.peer_id,
    )
    await message.answer(doc, attachment=photo, keyboard=start_keyboard)
