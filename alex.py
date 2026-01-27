from aiohttp import web
import os

# Фиктивный веб-сервер для Render
async def handle(request):
    return web.Response(text="Alex is alive!")

app_web = web.Application()
app_web.router.add_get('/', handle)

# В конце твоей функции main() добавь запуск веб-сервера
async def main():
    # Запуск бота
    asyncio.create_task(dp.start_polling(bot))
    
    # Запуск веб-сервера на порту, который даст Render
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 10000)))
    await site.start()
    
    while True:
        await asyncio.sleep(3600)

