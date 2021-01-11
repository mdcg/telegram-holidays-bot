import sqlite3
from datetime import datetime
import sys
from decouple import config
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from src.exceptions import NoNextHolidaysException
from src.constants import WEEKDAYS, WEEKENDS
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
        "nome_feriado": entry[1],
        "dia_semana": entry[2],
    }


def next_holiday():
    vacations = read_vacations_db()
    now = datetime.now()
    for v in vacations:
        vacation_date = datetime.strptime(v["data"], "%d/%m/%Y")
        if vacation_date > now:
            return v
    raise NoNextHolidaysException()


def start(update, context):
    response_message = "Fala essa galera!"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def unknown(update, context):
    response_message = "Tá doidé?"
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response_message
    )


def holiday(update, context):
    try:
        next_holiday_info = next_holiday()
        message = generate_message_by_date(next_holiday_info)
    except NoNextHolidaysException:
        message = "Não teremos mais nenhum feriado esse ano! :("

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def how_many_days_until_the_holiday(_date):
    now = datetime.now()
    vacation_date = datetime.strptime(_date, "%d/%m/%Y")
    delta = vacation_date - now
    return delta.days


def generate_message_by_date(holiday_info):
    days_until_the_holiday = how_many_days_until_the_holiday(
        holiday_info["data"]
    )

    weekday_message = ""
    if holiday_info["dia_semana"].lower() in WEEKENDS:
        weekday_message = (
            f"Infelizmente o próximo feriado cairá em um final "
            f"de semana ({holiday_info['dia_semana']}).\n"
        )
    else:
        weekday_message = (
            f"Receba! Teremos feriado em dia de "
            f"semana ({holiday_info['dia_semana']})!\n"
        )

    plural = ["m", "s"] if days_until_the_holiday > 1 else ["", ""]
    days_left = "Falta{} apenas {} dia{} para ele ({}).\n".format(
        plural[0], days_until_the_holiday, plural[1], holiday_info["data"]
    )

    return (
        f"{weekday_message}{days_left}Se ficou curioso, será: "
        f"{holiday_info['nome_feriado']}."
    )


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
