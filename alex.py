import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# Берем токен из настроек Render (Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Приветственное сообщение
@dp.message(lambda message: message.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("👋 Привет! Я Alex, твой новый ИИ-помощник. Я работаю автономно 24/7!")

# Простой эхо-ответ для проверки связи
@dp.message()
async def talk_handler(message: types.Message):
    await message.answer(f"Ты написал: {message.text}\n\nЯ тебя слышу! Скоро мой создатель добавит мне еще больше ума. 🗿")

# Фиктивный веб-сервер, чтобы Render не отключал бота
async def handle(request):
    return web.Response(text="Alex is alive and running!")

async def main():
    # Настройка веб-сервера
    app_web = web.Application()
    app_web.router.add_get('/', handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    
    # Порт берется из настроек Render (обычно 10000)
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    await site.start()
    print(f"🚀 Сервер запущен на порту {port}")
    
    # Запуск самого бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
        

