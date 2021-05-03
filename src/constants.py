from pathlib import Path

BASEDIR = Path(__file__).parent.parent
BRAZIL_HOLIDAYS_CSV = BASEDIR / Path("csvs/feriados.csv")
USA_HOLIDAYS_CSV = BASEDIR / Path("csvs/holidays.csv")

WEEKDAYS = [
    "segunda-feira",
    "monday",
    "terça-feira",
    "tuesday",
    "quarta-feira",
    "wednesday",
    "quinta-feira",
    "thursday",
    "sexta-feira",
    "friday",
]
WEEKENDS = ["sábado", "saturday", "domingo", "sunday"]

MESSAGE_LANGUAGE = {
    "PORTUGUESE": {
        "WEEKEND_MESSAGE": "Infelizmente o próximo feriado cairá em um final de semana ({}).\n",
        "WEEKDAY_MESSAGE": "Teremos feriado em dia da semana! ({})\n",
        "NEXT_HOLIDAY_MESSAGE": "Próximo feriado em {} dia(s)\n",
        "HOLIDAY_NAME_MESSAGE": "Se você ficou curioso, será: {}\n",
        "TODAY_IS_HOLIDAY_MESSAGE": "Hoje é feriado, Bom descanso! ({})",
        "NO_HOLIDAYS_MESSAGE": "Não teremos mais nenhum feriado esse ano! :(",
    },
    "ENGLISH": {
        "WEEKEND_MESSAGE": "Unfortunately the next holiday will be on a weekend ({}).\n",
        "WEEKDAY_MESSAGE": "We will have a holiday on a weekday! ({})\n",
        "NEXT_HOLIDAY_MESSAGE": "Next holiday in {} day(s)\n",
        "HOLIDAY_NAME_MESSAGE": "If you were curious, it will be: {}\n",
        "TODAY_IS_HOLIDAY_MESSAGE": "Today is a holiday, Good rest! ({})",
        "NO_HOLIDAYS_MESSAGE": "We won't have any more holidays this year! :(",
    },
}

COUNTRIES = {
    "BRAZIL": {
        "CSV_PATH": BRAZIL_HOLIDAYS_CSV,
        **MESSAGE_LANGUAGE["PORTUGUESE"],
    },
    "USA": {
        "CSV_PATH": USA_HOLIDAYS_CSV,
        **MESSAGE_LANGUAGE["ENGLISH"],
    },
}
