import asyncio
import secrets

from contextlib import suppress

from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hcode

from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase as MDB

from pymongo.errors import DuplicateKeyError

router = Router()

@router.message(CommandStart())
async def start(message: Message, db: MDB) -> None:
    with suppress(DuplicateKeyError):
        await db.users.insert_one({
            "_id": message.from_user.id,
            "password": secrets.token_urlsafe(8),
            "items": []
        })

    user = await db.users.find_one({"_id": message.from_user.id})
    await message.reply(
        f"Ваш ID: {hcode(user['_id'])}\n"
        f"Ваш пароль: {hcode(user['password'])}\n\n"
        f"<blockquote>Чтобы посмотреть список предметов: /items</blockquote>"
    )


async def main() -> None:
    bot = Bot("token",parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    cluster = AsyncIOMotorClient(host="localhost", port=27017)
    db = cluster.megaprojectdb

    dp.include_router(router)

    await bot.delete_webhook(True)
    await dp.start_polling(bot, db=db)


if __name__ == "__main__":
    asyncio.run(main())