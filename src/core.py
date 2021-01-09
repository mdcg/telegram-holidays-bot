import sqlite3
from datetime import datetime, timedelta
import sys
from decouple import config
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from src import logger

TELEGRAM_TOKEN = config("TELEGRAM_TOKEN", "")

def read_vacations_db():
    conn = sqlite3.connect("vacations.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vacations")
    vacations = []

    for entry in cursor.fetchall():
        vacations.append(map_vacation_result(entry))

    conn.close()
    return vacations


def map_vacation_result(entry):
    return {
        "data": entry[0],
        "dia_semana": entry[1],
        "nome_feriado": entry[2],
    }


def next_holiday():
    vacations = read_vacations_db()
    now = datetime.now()
    for v in vacations:
        vacation_date = datetime.strptime(v["data"], "%d/%m/%Y")
        if vacation_date > now:
            return v


def start(update, context):
    response_message = "Fala essa galera!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)


def unknown(update, context):
    response_message = "Tá doidé?"
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)


def holiday(update, context):
    next_holiday_info = next_holiday()
    message = (
        f"O próximo feriado é em {next_holiday_info['data']}, "
        f"referente a {next_holiday_info['nome_feriado']}, "
        f"{next_holiday_info['dia_semana']}."
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("holiday", holiday))
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
