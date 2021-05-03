from datetime import datetime
import sys
from decouple import config
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from src.exceptions import NoNextHolidaysException
from src.constants import (
    BRAZIL_HOLIDAYS_CSV,
    USA_HOLIDAYS_CSV,
    MESSAGE_LANGUAGE,
    COUNTRIES,
)
from src import logger
from src.utils import next_holiday, generate_message_by_date


TELEGRAM_TOKEN = config("TELEGRAM_TOKEN", "1755403223:AAEsfYCI7IXM4OKo-TzyHBDRwx2xdpn-67c")


def start(update, context):
    response_message = "Fala essa galera!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)


def unknown(update, context):
    response_message = "Tá doidé?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)


def check_for_holiday(update, context, language):
    country = COUNTRIES[language]
    try:
        next_holiday_info = next_holiday(country["CSV_PATH"])
        message = generate_message_by_date(next_holiday_info, country)
    except NoNextHolidaysException:
        message = country["NO_HOLIDAYS_MESSAGE"]

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def feriados(update, context):
    return check_for_holiday(update, context, "BRAZIL")


def holidays(update, context):
    return check_for_holiday(update, context, "USA")


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("feriados", feriados))
    dispatcher.add_handler(CommandHandler("holidays", holidays))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    logger.info("Initializing bot...")
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopping bot...")
        sys.exit(0)
