from vkbottle.bot import Bot
from vkbottle import LoopWrapper

from functions.mailing import check_mailing
from database.promo import check_promo
from config import api, labeler
from database.ivent import check_ivent

lw = LoopWrapper()

bot = Bot(api=api, labeler=labeler, loop_wrapper=lw)


# Проверяем ивентов каждую 1 минуту
@lw.interval(seconds=59)
async def task_mailing():
    await check_mailing()


# Проверяем промокод каждые 1 день
@lw.interval(days=1)
async def task_promo():
    await check_promo()


#Проверяем ивенты каждые 1 день секунд
@lw.interval(days=1)
async def task_ivent():
    await check_ivent()
