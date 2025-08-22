import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def boobs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /thing@BotName"""
    user = update.effective_user
    random_length = random.randint(80, 150)  # Случайное число от 1 до 100
    response = f"@{user.username}, ваша грудь {random_length} сантиметров в обхвате"
    await update.message.reply_text(response)

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчик команды
    application.add_handler(CommandHandler("thing", boobs))

    # Запускаем бота в режиме webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()