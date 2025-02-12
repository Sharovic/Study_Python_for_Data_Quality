"""
import sqlite3

with sqlite3.connect('content_storage.db') as connection:
# Для роботи з БД, вносення змін, отримання результатів. Повинно відкриватись та 
#закриватись для кожної дії. Cursor може бути "синтетичним цукром", що робить за нас це.
#connection = sqlite3.connect('content_storage.db')

    # Як тільки ці строки написали, відразу пишемо закриваючі. А вже потім між ними пишемо 
    # все, що нам потрібно  зробити. Небезпечно тримати курсор та коннекшен відкритими.
    cursor = connection.cursor()

    # cursor.execute() - для виконання дій в БД. Всередині пишемо так, ніби працюємо з БД напряму.
    # створюємо таблицю
    #cursor.execute('CREATE TABLE people (first_name text, last_name text, age real)')

    # вносимо дані
    cursor.execute("INSERT INTO people VALUES ('Stepan', 'Sraka', 46)")

    # Отримуємо дані
    cursor.execute('select * from people')

    # Отримані дані вносимо до змінної
    result = cursor.fetchall()
    print(result)



    # Тепер цю створену команду відравляємо на виконання в БД.
    connection.commit()
    # Закриття прописуємо ще коли тільки відкривали 
    cursor.close()
#connection.close()

"""

import pyodbc

# # Маємо вказати драйвер
# connection = pyodbc.connect('DRIVER= {SQLite3 ODBC Driver};Direct=True;Database=content_storage.db;String Types = Unicode')
# connection.close()
# print(type(connection))


# def __init__(self):
#     db_path = os.path.join(os.path.dirname(__file__), 'content_db.sqlite')
#     self.conn_str = (
#         "Driver=SQLite3 ODBC Driver;"
#         f"Database={db_path};"
#     )
with pyodbc.connect('DRIVER= {SQLite3 ODBC Driver};Direct=True;Database=content_storage.db;String Types = Unicode') as conn:
    cursor = conn.cursor()
    
    # Create News table
    create_news_table = """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            city TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            content_hash TEXT NOT NULL UNIQUE
            )
    """
    cursor.execute(create_news_table)

    # Create Ads table
    create_ads_table = """
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            expiration_date DATETIME NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            content_hash TEXT NOT NULL UNIQUE
            )
    """
    cursor.execute(create_ads_table)

    # Create Joke table
    create_joke_table = """
        CREATE TABLE IF NOT EXISTS joke (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            funny_rating INTEGER NOT NULL CHECK (funny_rating BETWEEN 1 AND 10),
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            content_hash TEXT NOT NULL UNIQUE
            )
    """
    cursor.execute(create_joke_table)

    conn.commit()
