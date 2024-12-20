from vkbottle import Keyboard, KeyboardButtonColor, Text

keyboard = (
    Keyboard(one_time=True, inline=False)
    .add(Text("Выключить"), color=KeyboardButtonColor.POSITIVE)
).get_json()
