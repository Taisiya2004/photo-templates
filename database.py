import sqlite3
from datetime import datetime, timedelta


def init_database():
    conn = sqlite3.connect('phototemplates.db')
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS technologies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tech_id INTEGER,
        template_number TEXT NOT NULL,
        route TEXT NOT NULL,
        mikron_group TEXT NOT NULL,
        FOREIGN KEY (tech_id) REFERENCES technologies(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quality_mapping (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mikron_group TEXT NOT NULL,
        factory1_group TEXT,
        factory2_group TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS factory_prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        factory_name TEXT NOT NULL,
        group_name TEXT NOT NULL,
        price INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exchange_rates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rate_date DATE NOT NULL,
        rate_value REAL NOT NULL,
        description TEXT
    )
    ''')

    # Очистка таблиц перед заполнением
    cursor.execute("DELETE FROM technologies")
    cursor.execute("DELETE FROM templates")
    cursor.execute("DELETE FROM quality_mapping")
    cursor.execute("DELETE FROM factory_prices")
    cursor.execute("DELETE FROM exchange_rates")

    # Заполнение технологий
    technologies = [
        ("Технология №1",),
        ("Технология №2",),
        ("Технология №3",)
    ]
    cursor.executemany("INSERT INTO technologies (name) VALUES (?)", technologies)

    # Заполнение шаблонов для Технологии №1 (данные из Таблицы 1.1)
    tech1_templates = [
        (1, "002", "B", "E"),
        (1, "061", "B", "E"),
        (1, "024", "B", "C"),
        (1, "001", "B", "C"),
        (1, "083", "B", "C"),
        (1, "008", "B", "C"),
        (1, "082", "B", "C"),
        (1, "006", "B", "C"),
        (1, "013", "B", "H"),
        (1, "076", "B", "C"),
        (1, "014", "B", "C"),
        (1, "077", "B", "C"),
        (1, "015", "B", "C"),
        (1, "026", "H", "C"),
        (1, "016", "B", "C"),
        (1, "017", "B", "C"),
        (1, "018", "B", "C"),
        (1, "039", "B", "H"),
        (1, "019", "B", "E"),
        (1, "023", "B", "E"),
        (1, "025", "B", "E"),
        (1, "027", "B", "E"),
        (1, "032", "B", "E"),
        (1, "034", "B", "E"),
        (1, "035", "B", "E"),
        (1, "036", "B", "E"),
        (1, "052", "B", "E"),
        (1, "080", "M", "C"),
        (1, "092", "HKM", "C"),
        (1, "053", "B", "C"),
        (1, "054", "B", "C"),
        (1, "055", "B", "C"),
        (1, "031", "B", "A")
    ]
    cursor.executemany(
        "INSERT INTO templates (tech_id, template_number, route, mikron_group) VALUES (?, ?, ?, ?)",
        tech1_templates
    )

    # Заполнение шаблонов для Технологии №2 (данные из Таблицы 1.2)
    tech2_templates = [
        (2, "105", "B", "E"),
        (2, "106", "B", "E"),
        (2, "275", "B", "C"),
        (2, "265", "B", "D"),
        (2, "405", "B", "D"),
        (2, "555", "B", "O"),
        (2, "015", "B", "D"),
        (2, "055", "B", "D"),
        (2, "025", "B", "C"),
        (2, "065", "B", "C"),
        (2, "067", "B", "B"),
        (2, "525", "B", "B"),
        (2, "395", "B", "B"),
        (2, "515", "B", "E"),
        (2, "505", "B", "H"),
        (2, "550", "B", "D"),
        (2, "615", "B", "C"),
        (2, "645", "B", "C"),
        (2, "026", "H", "C"),
        (2, "605", "B", "B"),
        (2, "655", "B", "B"),
        (2, "425", "B", "B"),
        (2, "710", "B", "M"),
        (2, "705", "B", "M"),
        (2, "800", "B", "E"),
        (2, "815", "B", "E"),
        (2, "820", "B", "E"),
        (2, "825", "B", "E"),
        (2, "830", "B", "E"),
        (2, "835", "B", "E"),
        (2, "840", "B", "E"),
        (2, "845", "B", "E"),
        (2, "080", "M", "C"),
        (2, "092", "HKM", "C"),
        (2, "850", "B", "C"),
        (2, "855", "B", "C"),
        (2, "860", "B", "C"),
        (2, "900", "B", "A")
    ]
    cursor.executemany(
        "INSERT INTO templates (tech_id, template_number, route, mikron_group) VALUES (?, ?, ?, ?)",
        tech2_templates
    )

    # Заполнение шаблонов для Технологии №3 (данные из Таблицы 1.3)
    tech3_templates = [
        (3, "002", "B", "K"),
        (3, "024", "B", "C"),
        (3, "001", "B", "C"),
        (3, "083", "B", "E"),
        (3, "084", "B", "C"),
        (3, "008", "B", "C"),
        (3, "082", "B", "E"),
        (3, "085", "B", "C"),
        (3, "094", "B", "C"),
        (3, "006", "B", "C"),
        (3, "016", "B", "E"),
        (3, "013", "B", "L"),
        (3, "076", "B", "E"),
        (3, "077", "B", "E"),
        (3, "014", "B", "E"),
        (3, "015", "B", "E"),
        (3, "017", "B", "E"),
        (3, "026", "B", "E"),
        (3, "042", "H", "C"),
        (3, "018", "B", "C"),
        (3, "019", "B", "Q"),
        (3, "023", "B", "K"),
        (3, "027", "B", "I"),
        (3, "025", "B", "Q"),
        (3, "034", "B", "I"),
        (3, "032", "B", "Q"),
        (3, "036", "B", "I"),
        (3, "035", "B", "Q"),
        (3, "053", "B", "I"),
        (3, "052", "B", "Q"),
        (3, "055", "B", "I"),
        (3, "054", "B", "Q"),
        (3, "066", "B", "I"),
        (3, "064", "B", "Q"),
        (3, "130", "B", "E"),
        (3, "131", "B", "D"),
        (3, "132", "B", "E"),
        (3, "133", "B", "D"),
        (3, "081", "M", "C"),
        (3, "096", "M", "C"),
        (3, "040", "B", "A"),
        (3, "041", "B", "A"),
        (3, "031", "B", "A")

    ]
    cursor.executemany(
        "INSERT INTO templates (tech_id, template_number, route, mikron_group) VALUES (?, ?, ?, ?)",
        tech3_templates
    )

    # Заполнение соответствия групп качества (Таблица 2)
    quality_mappings = [
        ("A", "C", "C"),
        ("B", "E", "C"),
        ("C", "F", "E"),
        ("D", "F", "F"),
        ("E", "H", "G"),
        ("F", "H", "H"),
        ("G", "I", "H"),
        ("H", "I", "H"),
        ("I", None, "J"),
        ("J", None, "J"),
        ("K", None, "J"),
        ("L", None, "J"),
        ("M", None, "PG"),
        ("N", None, "PH"),
        ("O", None, "PH"),
        ("P", None, "PJ"),
        ("Q", None, "PJ"),
        ("R", None, "PJ"),
        ("S", None, "PJ")
    ]
    cursor.executemany(
        "INSERT INTO quality_mapping (mikron_group, factory1_group, factory2_group) VALUES (?, ?, ?)",
        quality_mappings
    )

    # Заполнение цен фабрик (Таблица 3)
    factory1_prices = [
        ("Фабрика №1", "A", 600),
        ("Фабрика №1", "B", 800),
        ("Фабрика №1", "C", 900),
        ("Фабрика №1", "D", 950),
        ("Фабрика №1", "E", 1000),
        ("Фабрика №1", "F", 1100),
        ("Фабрика №1", "G", 1200),
        ("Фабрика №1", "H", 2000),
        ("Фабрика №1", "I", 3000)
    ]

    factory2_prices = [
        ("Фабрика №2", "A", 900),
        ("Фабрика №2", "B", 1100),
        ("Фабрика №2", "C", 1500),
        ("Фабрика №2", "D", 1700),
        ("Фабрика №2", "E", 2000),
        ("Фабрика №2", "F", 2500),
        ("Фабрика №2", "G", 4000),
        ("Фабрика №2", "H", 5000),
        ("Фабрика №2", "I", 6000),
        ("Фабрика №2", "J", 15000),
        ("Фабрика №2", "PG", 7500),
        ("Фабрика №2", "PH", 8000),
        ("Фабрика №2", "Pi", 9500),
        ("Фабрика №2", "PJ", 17500)
    ]

    cursor.executemany(
        "INSERT INTO factory_prices (factory_name, group_name, price) VALUES (?, ?, ?)",
        factory1_prices + factory2_prices
    )

    # Заполнение курсов валют
    today = datetime.now().strftime("%Y-%m-%d")
    last_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m-%d")
    next_month = (datetime.now().replace(day=28) + timedelta(days=4)).strftime("%Y-%m-%d")

    exchange_rates = [
        (today, 11.0, "Текущий курс"),
        (last_month, 12.1, "Месяц назад (+10%)"),
        (next_month, 10.45, "Месяц вперед (-5%)"),
        (next_month, 9.9, "Месяц вперед (-10%)")
    ]
    cursor.executemany(
        "INSERT INTO exchange_rates (rate_date, rate_value, description) VALUES (?, ?, ?)",
        exchange_rates
    )

    conn.commit()
    conn.close()
    print("База данных успешно создана и заполнена")


if __name__ == "__main__":
    init_database()
