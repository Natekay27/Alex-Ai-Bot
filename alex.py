import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiohttp import web

# Токен берется из настроек Render (Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(lambda message: message.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("👋 Доброе утро! Я Alex. Я успешно запущен на Render и готов к работе 24/7!")

# Обработчик всех остальных сообщений
@dp.message()
async def talk_handler(message: types.Message):
    await message.answer(f"Я получил твое сообщение: {message.text}\n\nСвязь установлена! 🚀")

# Веб-сервер для того, чтобы Render не отключал бота
async def handle(request):
    return web.Response(text="Alex is alive and running!")

async def main():
    # Настройка и запуск веб-сервера
    app_web = web.Application()
    app_web.router.add_get('/', handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    
    # Порт 10000 стандартный для Render
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    print(f"🚀 Бот запущен! Слушаю порт {port}...")
    
    # Запуск опроса Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
        
