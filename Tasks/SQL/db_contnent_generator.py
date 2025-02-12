"""
# Important Implementation Details:
# 1. Uses SQLite for persistent storage with UNIQUE constraints
# 2. Implements three content types: News, Ads, Jokes
# 3. Supports multiple output formats (TXT, JSON, XML, DB)
# 4. Handles batch processing from text files
# 5. Includes input validation and error handling
# 6. Uses content hashing to prevent duplicates
# 7. Normalizes text input for consistency

# Note: The script automatically generates word and letter count CSVs
# after each content addition (see generate_words_csv and generate_letters_csv calls)
"""

from faker import Faker
import random
from pathlib import Path
import os
import pyodbc
import hashlib

# Створюємо екземпляр Faker з українською локалізацією
fake = Faker('uk_UA')
# Додаємо англійську локалізацію для деяких даних
fake_en = Faker('en_US')

# Список жартів та шаблони реклами залишаються без змін...
JOKES = [
    "Чому програмісти не люблять природу? Там дуже поганий інтернет!",
    "Як називається група програмістів? Git-ара банда!",
    "Чому Python такий популярний? Бо він не має фігурних дужок!",
    "Що сказав JavaScript Пітону? Ти занадто простий!",
    "Як заспокоїти програміста? Все ок, це просто баг, а не фіча!",
    "Що спільного між програмістом і пральною машиною? Обидва крутять цикли!",
    "Чому програмісти плутають Різдво і Хеловін? Бо Oct 31 = Dec 25!",
    "Скільки програмістів потрібно щоб замінити лампочку? Жодного, це проблема з hardware!",
    "Що сказав SQL-розробник офіціанту? SELECT coffee FROM menu WHERE price < 5!",
    "Чому програмісти носять окуляри? Бо вони не можуть C#!"
]

AD_TEMPLATES = [
    "АКЦІЯ! {product} зі знижкою до {discount}%! Тільки до {date}",
    "НОВИНКА! Представляємо {product}. Спеціальна ціна для перших покупців!",
    "Тільки сьогодні! {product} за неймовірною ціною. Економія {discount}%",
    "Відкриття нового магазину! {product} кожному покупцю у подарунок!",
    "Розпродаж колекції {season}! {product} за найкращими цінами року",
    "Святкові знижки на {product}! Поспішайте, кількість обмежена",
    "{brand} представляє: новий {product}. Передзамовлення зі знижкою {discount}%",
    "Грандіозний розпродаж! {product} та інші товари від {brand}",
    "Чорна п'ятниця триває! {product} за півціни",
    "Революційна новинка: {product} від {brand}. Змініть своє життя на краще!"
]

def create_tables(conn):
    """Create necessary tables if they don't exist"""
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        city TEXT NOT NULL,
        content_hash TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        expiration_date TEXT NOT NULL,
        content_hash TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS joke (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        funny_rating TEXT NOT NULL,
        content_hash TEXT NOT NULL UNIQUE
    );
    """)
    
    conn.commit()
    print("Tables created successfully")

def generate_ad():
    template = random.choice(AD_TEMPLATES)
    return template.format(
        product=random.choice(['смартфони', 'ноутбуки', 'планшети', 'телевізори', 
                             'навушники', 'книги', 'меблі', 'одяг', 'взуття', 
                             'косметика', 'побутова техніка']),
        discount=random.randint(10, 90),
        date=fake.date_between(start_date='today', end_date='+30d').strftime('%d.%m.%Y'),
        brand=fake.company(),
        season=random.choice(['весна', 'літо', 'осінь', 'зима'])
    )

def get_content_hash(content):
    """Generate a more reliable hash using SHA-256"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def generate_record():
    """Generate a unique record by ensuring unique content"""
    record_type = random.choice(["news", "ads", "joke"])
    
    if record_type == "news":
        content = fake.text(max_nb_chars=200)
        additional = fake.city()
    elif record_type == "ads":
        content = generate_ad()
        additional = fake.date_between(start_date='today', end_date='+30d').strftime('%d-%m-%Y')
    else:  # joke
        content = random.choice(JOKES)
        additional = str(random.randint(1, 10))
    
    return [record_type, content, additional]

def append_to_file(filename, record):
    """Append a single record to the file"""
    with open(filename, 'a', encoding='utf-8') as file:
        # Якщо файл не пустий, додаємо роздільник
        if os.path.getsize(filename) > 0:
            file.write("\n---\n")
        file.write(f"{record[0]}\n{record[1]}\n{record[2]}")

def create_or_clear_file(filename):
    """Create a new file or clear existing one"""
    with open(filename, 'w', encoding='utf-8') as file:
        pass
    print(f"File created/cleared: {filename}")

def generate_content(num_records=10):
    """Generate content and save it to both DB and file"""
    # Отримуємо шлях до поточної директорії
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Створюємо шляхи до файлів в поточній директорії
    db_path = os.path.join(current_dir, "generated_content.db")
    file_path = os.path.join(current_dir, "generated_content.txt")
    
    # Створюємо/очищуємо файл
    create_or_clear_file(file_path)
    
    # Підключаємося до бази даних
    connection_string = f'DRIVER={{SQLite3 ODBC Driver}};Direct=True;Database={db_path};String Types=Unicode'
    
    with pyodbc.connect(connection_string) as conn:
        # Створюємо таблиці
        create_tables(conn)
        cursor = conn.cursor()
        
        successful_inserts = 0
        attempts = 0
        max_attempts = num_records * 2

        while successful_inserts < num_records and attempts < max_attempts:
            record = generate_record()
            content_hash = get_content_hash(record[1])
            
            try:
                if record[0] == "news":
                    insert_query = """
                        INSERT INTO news (content, city, content_hash)        
                        VALUES (?, ?, ?);
                        """
                elif record[0] == "ads":
                    insert_query = """
                        INSERT INTO ads (content, expiration_date, content_hash)        
                        VALUES (?, ?, ?);
                        """
                else:  # joke
                    insert_query = """
                        INSERT INTO joke (content, funny_rating, content_hash)        
                        VALUES (?, ?, ?);
                        """
                
                # Спроба вставки в БД
                cursor.execute(insert_query, (record[1], record[2], content_hash))
                cursor.commit()
                
                # Якщо вставка в БД успішна, додаємо запис у файл
                append_to_file(file_path, record)
                
                successful_inserts += 1
                print(f"Successfully inserted record {successful_inserts}/{num_records} of type {record[0]}")
                
            except pyodbc.Error as e:
                if 'UNIQUE constraint failed' in str(e):
                    print(f"Duplicate content hash encountered for {record[0]}, trying again...")
                else:
                    print(f"Database error: {str(e)}")
                    raise
            
            attempts += 1
        
        if successful_inserts < num_records:
            print(f"Warning: Only managed to insert {successful_inserts} unique records out of {num_records} requested")
        else:
            print(f"Successfully inserted all {num_records} records")

if __name__ == "__main__":
    generate_content(100)