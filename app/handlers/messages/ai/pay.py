from vkbottle import Keyboard, KeyboardButtonColor, OpenLink
from yoomoney import Client, Quickpay

from database.database import connect_to_db

from config import labeler, admin_id
from bot import bot


@labeler.message(payload={"command": "pay"})
async def subscribe_handler(message):
    new = message.peer_id
    quickpay = Quickpay(
        receiver='4100118956551285',
        quickpay_form='shop',
        targets='Sponsor this project',
        paymentType='SB',
        sum=100,
        label=new
    )
    pey_keyboard = (
        Keyboard(one_time=False, inline=True)
        .add(OpenLink(link=quickpay.base_url, label="перейди чтобы оплатить"), color=KeyboardButtonColor.POSITIVE)
    ).get_json()

    await message.answer("ссылка на оплату", keyboard=pey_keyboard)


async def get_payment(vk_id, balance):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        # Проверяем существование таблицы и создаем её, если она отсутствует
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS balance (
                    id VARCHAR(255) PRIMARY KEY,
                    balance REAL NOT NULL
                );
            """)

        # Попытка вставки данных с обновлением существующего значения balance
        cursor.execute(
            """
            INSERT INTO balance (id, balance)
            VALUES (%s, %s)
            ON CONFLICT (id)
            DO UPDATE SET balance = balance.balance + EXCLUDED.balance;
            """,
            (vk_id, balance),
        )

        connection.commit()
        await bot.api.messages.send(user_id=vk_id, message=f"Ваш баланс успешно пополнен на : {balance}.руб",
                                    random_id=0)

    except Exception as e:
        connection.rollback()
        await bot.api.messages.send(user_id=vk_id, message=f"Произошла непредвиденная ошибка: {e}", random_id=0)
    finally:
        cursor.close()
        connection.close()
