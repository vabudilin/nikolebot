import os
import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def boobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /thing@BotName"""
    user = update.effective_user
    if not user.username:
        response = f"{user.first_name}, ваша грудь {random.randint(75, 150)} сантиметров в обхвате"
    else:
        response = f"@{user.username}, ваша грудь {random.randint(75, 150)} сантиметров в обхвате"
    await update.message.reply_text(response)


async def main() -> None:
    """Запуск бота"""
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")

    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик команды
    application.add_handler(CommandHandler("boobs", boobs))

    # Инициализируем приложение
    await application.initialize()

    # Настраиваем webhook
    port = int(os.getenv("PORT", 8443))
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

    # Устанавливаем webhook
    await application.bot.set_webhook(webhook_url)

    # Запускаем приложение в режиме webhook
    await application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=webhook_url
    )

    # Останавливаем приложение при завершении
    await application.stop()
    await application.shutdown()


if __name__ == "__main__":
    # Используем существующий event loop или создаем новый, если он отсутствует
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Запускаем задачу в существующем event loop
    loop.create_task(main())

    # Держим event loop активным
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()