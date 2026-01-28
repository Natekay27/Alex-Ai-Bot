import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiohttp import web
import google.generativeai as genai

# Загружаем ключи из Render
TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Настройка ИИ
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Самая быстрая версия

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(lambda message: message.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("🤖 Привет! Теперь я подключен к Google Gemini. Спрашивай что угодно, я постараюсь ответить!")

@dp.message()
async def ai_handler(message: types.Message):
    try:
        # Отправляем вопрос в нейросеть
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка ИИ: {e}")
        await message.answer("Ой, я запнулся... Попробуй еще раз через минуту!")

async def handle(request):
    return web.Response(text="Alex AI is online!")

async def main():
    app_web = web.Application()
    app_web.router.add_get('/', handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 10000)))
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
