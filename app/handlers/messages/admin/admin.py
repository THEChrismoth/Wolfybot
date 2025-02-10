from config import admin_id
from bot import bot
from database.database import connect_to_db

from vkbottle.bot import BotLabeler, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, BaseStateGroup


class States(BaseStateGroup):
    WAITING_FOR_PROMO = "waiting_for_promo"
    WAITING_FOR_IVENT = "waiting_for_ivent"


admin_keyboard = (
    Keyboard(one_time=False, inline=False)
    .add(Text("добавить промокод", payload={"command": "edit_promo"}), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("добавить ивент", payload={"command": "edit_ivent"}), color=KeyboardButtonColor.POSITIVE)
).get_json()

admin_id = int(admin_id)

admin_labeler = BotLabeler()
admin_labeler.auto_rules = [rules.FromPeerRule(admin_id)]
admin_labeler.vbml_ignore_case = True


@admin_labeler.message(text="админ панель")
async def admin_panel(message):
    await message.answer("вы в админ панель", keyboard=admin_keyboard)


@admin_labeler.message(payload={"command": "edit_promo"})
async def edit_promo(message):
    await message.answer("Введите три значения: промокод, ссылку и дата формата YYYY-MM-DD")
    await bot.state_dispenser.set(message.peer_id, States.WAITING_FOR_PROMO)


@admin_labeler.message(state=States.WAITING_FOR_PROMO)
async def waiting_for_promo(message):
    # Получаем текст сообщения
    text = message.text.strip()
    # Разделение сообщения на части
    parts = text.split(' ')

    if len(parts) != 3:
        await message.answer(
            "Неверный формат! Пожалуйста, введите три значения: промокод, ссылку и дата формата YYYY-MM-DD")
        return

    promo_code = parts[0]
    promo_link = parts[1]
    promo_data = parts[2]

    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        # Проверка существования таблицы и ее создание, если необходимо
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS promo (
                promo_code VARCHAR(255) PRIMARY KEY,
                link TEXT NOT NULL,
                data TEXT NOT NULL
            );
        """)
        connection.commit()

        # Добавление записи в таблицу
        cursor.execute("INSERT INTO promo (promo_code, link, data) VALUES (%s, %s, %s);",
                       (promo_code, promo_link, promo_data))
        connection.commit()
        await message.answer(f"Промокод {promo_code} успешно сохранен!")
        # Возвращаем пользователя в начальное состояние
        await bot.state_dispenser.delete(message.peer_id)
    except IntegrityError as e:
        connection.rollback()  # Откат транзакции в случае ошибки
        await message.answer("Ошибка при сохранении промокода. Возможно, такой промокод уже существует.")
    except Exception as e:
        await message.answer(f"Произошла непредвиденная ошибка: {e}")
    finally:
        cursor.close()
        connection.close()


@admin_labeler.message(payload={"command": "edit_ivent"})
async def edit_promo(message):
    await message.answer("Введите три значения: название ивента, ссылку и дата формата YYYY-MM-DD")
    await bot.state_dispenser.set(message.peer_id, States.WAITING_FOR_IVENT)


@admin_labeler.message(state=States.WAITING_FOR_IVENT)
async def waiting_for_ivent(message):
    # Получаем текст сообщения
    text = message.text.strip()
    # Разделение сообщения на части
    parts = text.split(' ')

    if len(parts) != 3:
        await message.answer(
            "Неверный формат! Пожалуйста, введите три значения: название ивента, ссылку и дата формата YYYY-MM-DD")
        return

    ivent_name = parts[0].replace('-', ' ')
    ivent_link = parts[1]
    ivent_data = parts[2]

    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        # Проверка существования таблицы и ее создание, если необходимо
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ivent (
                ivent_name VARCHAR(255) PRIMARY KEY,
                link TEXT NOT NULL,
                data TEXT NOT NULL
            );
        """)
        connection.commit()

        # Добавление записи в таблицу
        cursor.execute("INSERT INTO ivent (ivent_name, link, data) VALUES (%s, %s, %s);",
                       (ivent_name, ivent_link, ivent_data))
        connection.commit()
        await message.answer(f"Ивент {ivent_name} успешно сохранен!")
        # Возвращаем пользователя в начальное состояние
        await bot.state_dispenser.delete(message.peer_id)
    except IntegrityError as e:
        connection.rollback()  # Откат транзакции в случае ошибки
        await message.answer("Ошибка при сохранении ивента. Возможно, такой ивент уже существует.")
    except Exception as e:
        await message.answer(f"Произошла непредвиденная ошибка: {e}")
    finally:
        cursor.close()
        connection.close()
