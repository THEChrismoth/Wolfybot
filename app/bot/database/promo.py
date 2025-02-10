import datetime

from database.database import connect_to_db
from config.config import admin_id


async def check_promo():
    from config.bot import bot
    # Подключение к БД
    connection = connect_to_db()
    cursor = connection.cursor()

    current_date_str = datetime.date.today().isoformat()  # Преобразуем текущую дату в строку формата 'YYYY-MM-DD'

    # Удаление записей, где дата меньше текущей
    cursor.execute("DELETE FROM promo WHERE data < %s", (current_date_str,))

    rows_deleted = cursor.rowcount  # Получаем количество удалённых строк

    connection.commit()  # Применяем изменения

    cursor.close()
    connection.close()

    if rows_deleted > 0:
        await bot.api.messages.send(
            user_id=admin_id,
            message=f"Удалено {rows_deleted} устаревших промокодов",
            random_id=0
        )
