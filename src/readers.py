import csv
from src import logger


def read_csv(csv_path):
    logger.info("Reading CSV file containing the holidays.")

    data = []
    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            data.append(row)

    return data
