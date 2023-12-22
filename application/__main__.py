import flet

from flet import Page, MainAxisAlignment, TextField, TextAlign, ElevatedButton, Text

from aiogram import Bot

from motor.motor_asyncio import AsyncIOMotorClient


bot = Bot("token")

cluster = AsyncIOMotorClient(host="localhost", port=27017)

db = cluster.megaprojectdb

async def main(page: Page) -> None:
  page.vertical_alignment = MainAxisAlignment.CENTER
  page.window_width = 500
  page.window_height = 700
  page.window_resizable = False

  async def auth(event) -> None:
    _login = login_input.value
    _pwd = password_input.value

    if user := await db.users.find_one({"_id": int(_login), "password": _pwd}):
      await page.clean_async()
      await page.add_async(Text(f"Hello, {user['_id']}!"))
      await bot.send_message(user["_id"], "New Authorization!")

  login_input = TextField(text_align=TextAlign.CENTER, label="Логин")
  password_input = TextField(text_align=TextAlign.CENTER, label="Пароль")

  await page.add_async(
    login_input,
    password_input,
    ElevatedButton("Авторизоваться", on_click=auth)
  )

if __name__ == "__main__":
  flet.app(target=main)