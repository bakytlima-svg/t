import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Получаем ключи из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY не найден!")

# Подключаем Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# Telegram
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Я Telegram-бот с искусственным интеллектом 🤖\n"
        "Напиши мне любой вопрос, и я постараюсь ответить!"
    )


@dp.message()
async def message_handler(message: types.Message):
    user_text = message.text

    if not user_text:
        await message.answer("Пожалуйста, отправь текстовое сообщение 😊")
        return

    try:
        # Отправляем запрос Gemini
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=user_text
        )

        answer = response.text

        if not answer:
            answer = "Не удалось получить ответ от Gemini 😔"

        await message.answer(answer)

    except Exception as e:
        logging.error(f"Ошибка Gemini: {e}")
        await message.answer(
            "Произошла ошибка при обращении к Gemini 😔\n"
            "Попробуй ещё раз через несколько секунд."
        )


async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
