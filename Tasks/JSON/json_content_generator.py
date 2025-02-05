from faker import Faker
import random
import json
from pathlib import Path
import os

# Створюємо екземпляр Faker з українською локалізацією
fake = Faker('uk_UA')
# Додаємо англійську локалізацію для деяких даних
fake_en = Faker('en_US')

# Список жартів
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

# Шаблони для реклами
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

def generate_record():
    record_type = random.choice(["news", "ad", "joke"])
    
    if record_type == "news":
        content = fake.text(max_nb_chars=200)
        additional = fake.city()
    elif record_type == "ad":
        content = generate_ad()
        additional = fake.date_between(start_date='today', end_date='+30d').strftime('%d-%m-%Y')
    else:  # joke
        content = random.choice(JOKES)
        additional = str(random.randint(1, 10))
    
    return {
        "type": record_type,
        "content": content,
        "additional": additional
    }

def create_files(base_filename, num_records=10):
    try:
        # Створюємо директорію, якщо вона не існує
        directory = os.path.dirname(base_filename)
        if directory:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Генеруємо записи
        records = [generate_record() for _ in range(num_records)]
        
        # Створюємо txt файл
        txt_filename = base_filename + ".txt"
        with open(txt_filename, 'w', encoding='utf-8') as file:
            for i, record in enumerate(records):
                file.write(f"{record['type']}\n{record['content']}\n{record['additional']}")
                if i < num_records - 1:
                    file.write("\n---\n")
        
        # Створюємо json файл
        json_filename = base_filename + ".json"
        with open(json_filename, 'w', encoding='utf-8') as file:
            json.dump(records, file, ensure_ascii=False, indent=2)
        
        print(f"Файли успішно створено: {txt_filename} та {json_filename}")
        return True
    
    except Exception as e:
        print(f"Помилка при створенні файлів: {str(e)}")
        return False

if __name__ == "__main__":
    # Створюємо абсолютний шлях до файлу
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_filename = os.path.join(current_dir, "generated_content")
    
    # Створюємо файли
    create_files(base_filename, 10)