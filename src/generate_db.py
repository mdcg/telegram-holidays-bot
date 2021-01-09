import csv
import sqlite3
import os
from src import logger
import sys


def delete_db():
    logger.info("Deleting an existing database.")
    if os.path.exists("vacations.db"):
        os.remove("vacations.db")


def init_db():
    logger.info("Creating holiday table.")
    conn = sqlite3.connect("vacations.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE vacations (
            data VARCHAR(10) NOT NULL,
            nome_feriado VARCHAR(255) NOT NULL,
            dia_semana VARCHAR(255) NOT NULL
    );
    """
    )
    conn.close()


def read_csv(csv_path):
    logger.info("Reading csv file containing the holidays.")
    data = []
    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            data.append(row)

    return data


def insert_data(row):
    logger.info(
        f"Inserting data into sqlite: "
        f"({row['data']}, {row['nome_feriado']}, {row['dia_semana']})"
    )
    try:
        conn = sqlite3.connect("vacations.db")
        cursor = conn.cursor()
        sql = """INSERT INTO vacations
            (data, nome_feriado, dia_semana) 
            VALUES (?, ?, ?);"""

        data_tuple = (row["data"], row["nome_feriado"], row["dia_semana"])
        cursor.execute(sql, data_tuple)
        conn.commit()
        cursor.close()
    except sqlite3.Error as error:
        logger.error(f"Failed to insert data into sqlite. {error}")
    finally:
        if conn:
            conn.close()
            logger.info("The SQLite connection is closed.")


if __name__ == "__main__":
    logger.info("Initializing generate_db script.")

    delete_db()
    init_db()

    try:
        data = read_csv(sys.argv[1])
    except IndexError:
        logger.error(
            "No path to the file containing the holidays was reported."
        )
        sys.exit(1)

    for row in data:
        insert_data(row)

    logger.info("Holidays successfully inserted.")
