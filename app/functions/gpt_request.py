from httpx import AsyncClient
from openai import AsyncOpenAI
from config import GPT_key
from database.database import connect_to_db
from bot import bot


# Создаем экземпляр клиента OpenAI с использованием прокси и базы данных
gpt = AsyncOpenAI(
    api_key=GPT_key,
    base_url="https://api.proxyapi.ru/openai/v1",
    http_client=AsyncClient(),
)


# Функция для получения ответов от модели GPT
async def gpt_request(prompt, user_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        id = str(user_id)

        # Проверяем баланс пользователя
        cursor.execute("SELECT balance FROM balance WHERE id = %s;", (id,))
        result = cursor.fetchone()

        if result is None:
            await bot.api.messages.send(user_id=user_id, message=f"Ваш баланс равен 0. Пожалуйста, пополните счет.", random_id=0)
            return None

        balance = float(result[0])

        if balance > 1:
            # Успешный запрос к модели GPT
            response = await gpt.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": str(prompt)}]
            )

            # Получение информации о количестве использованных токенов
            tokens_used = response.usage.total_tokens

            # Расчет стоимости запроса (цена за 1000 токенов = 546)
            cost_per_1000_tokens = 0.546
            total_cost = (tokens_used / 1000) * cost_per_1000_tokens

            # Обновляем баланс пользователя, уменьшая его на стоимость запроса
            new_balance = balance - total_cost
            cursor.execute("UPDATE balance SET balance = %s WHERE id = %s;", (new_balance, id))
            connection.commit()  # Сохраняем изменения в базе данных

            return response
        else:
            await bot.api.messages.send(user_id=user_id, message=f"Недостаточно средств на счете.", random_id=0)
    except Exception as e:
        await bot.api.messages.send(user_id=user_id, message=f"Ошибка при выполнении операции: {e}", random_id=0)
    finally:
        cursor.close()
        connection.close()


# Функция для получения изображений от модели GPT
async def gpt_image(prompt, user_id):
    connection = connect_to_db()
    cursor = connection.cursor()

    try:
        id = str(user_id)

        # Проверяем баланс пользователя
        cursor.execute("SELECT balance FROM balance WHERE id = %s;", (id,))
        result = cursor.fetchone()

        if result is None:
            await bot.api.messages.send(user_id=user_id, message=f"Ваш баланс равен 0. Пожалуйста, пополните счет.", random_id=0)
            return None

        balance = float(result[0])

        if balance > 12:
            # Успешный запрос к модели GPT
            response = await gpt.images.generate(
                prompt=prompt, n=1, size="1024x1024", model="dall-e-3"
            )

            # Расчет стоимости 1 изображения
            cost_image = 12

            # Обновляем баланс пользователя, уменьшая его на стоимость запроса
            new_balance = balance - cost_image
            cursor.execute("UPDATE balance SET balance = %s WHERE id = %s;", (new_balance, id))
            connection.commit()  # Сохраняем изменения в базе данных

            return response
        else:
            await bot.api.messages.send(user_id=user_id, message=f"Недостаточно средств на счете.", random_id=0)
    except Exception as e:
        await bot.api.messages.send(user_id=user_id, message=f"Ошибка при выполнении операции: {e}", random_id=0)
    finally:
        cursor.close()
        connection.close()
