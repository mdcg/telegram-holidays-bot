import sqlite3

from decouple import config
from datetime import datetime, timedelta
from src import logger


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


if __name__ == "__main__":
    logger.info(next_holiday())
