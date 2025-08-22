import os
import random
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

    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик команды
    application.add_handler(CommandHandler("boobs", boobs))

    # Настраиваем webhook
    port = int(os.getenv("PORT", 8443))
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    await application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())