"""Дуже не зручно зберігає в xml. Тому буду додавати minidom для форматування та запису в xml_generated_content.xml"""
# Імпортуємо необхідні бібліотеки
from faker import Faker  # Бібліотека для генерації фейкових даних
import random  # Бібліотека для генерації випадкових значень
import json  # Бібліотека для роботи з JSON форматом
from pathlib import Path  # Бібліотека для роботи з шляхами файлів
import os  # Бібліотека для роботи з операційною системою
import xml.etree.ElementTree as ET  # Бібліотека для роботи з XML
from datetime import datetime  # Бібліотека для роботи з датами та часом
from xml.dom import minidom # Бібліотека для зручного форматування та запису у читабельному вигляді в xml-файл


# Створюємо екземпляр Faker з українською локалізацією
fake = Faker('uk_UA')
# Додаємо англійську локалізацію для деяких даних
fake_en = Faker('en_US')

# Список жартів для генерації контенту
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
    """
    Генерує рекламне оголошення на основі шаблонів
    
    Returns:
        str: Згенерований рекламний текст з підставленими значеннями
    """
    template = random.choice(AD_TEMPLATES)  # Вибираємо випадковий шаблон реклами
    return template.format(  # Заповнюємо шаблон даними
        product=random.choice(['смартфони', 'ноутбуки', 'планшети', 'телевізори', 
                             'навушники', 'книги', 'меблі', 'одяг', 'взуття', 
                             'косметика', 'побутова техніка']),
        discount=random.randint(10, 90),  # Генеруємо випадкову знижку
        date=fake.date_between(start_date='today', end_date='+30d').strftime('%d.%m.%Y'),  # Генеруємо дату
        brand=fake.company(),  # Генеруємо назву компанії
        season=random.choice(['весна', 'літо', 'осінь', 'зима'])  # Вибираємо випадковий сезон
    )

def generate_record():
    """
    Генерує один запис (новину, рекламу або жарт)
    
    Returns:
        dict: Словник з типом запису, контентом та додатковою інформацією
    """
    record_type = random.choice(["news", "ad", "joke"])  # Вибираємо випадковий тип запису
    
    if record_type == "news":  # Якщо тип - новина
        content = fake.text(max_nb_chars=200)  # Генеруємо текст новини
        additional = fake.city()  # Генеруємо місто
    elif record_type == "ad":  # Якщо тип - реклама
        content = generate_ad()  # Генеруємо рекламний текст
        additional = fake.date_between(start_date='today', end_date='+30d').strftime('%d-%m-%Y')  # Генеруємо дату
    else:  # Якщо тип - жарт
        content = random.choice(JOKES)  # Вибираємо випадковий жарт
        additional = str(random.randint(1, 10))  # Генеруємо рейтинг
    
    return {
        "type": record_type,
        "content": content,
        "additional": additional
    }

def create_xml_content(records):
    """
    Створює XML структуру на основі згенерованих записів
    
    Args:
        records (list): Список згенерованих записів
        
    Returns:
        xml.etree.ElementTree.Element: Кореневий елемент XML структури
    """
    root = ET.Element("content_feed")  # Створюємо кореневий елемент
    
    # Створюємо контейнери для кожного типу контенту
    news = ET.SubElement(root, "news")  # Створюємо елемент для новин
    advertisements = ET.SubElement(root, "advertisements")  # Створюємо елемент для реклами
    jokes = ET.SubElement(root, "jokes")  # Створюємо елемент для жартів
    
    # Обробляємо кожний запис
    for record in records:
        item = ET.Element("item")  # Створюємо елемент для запису
        
        # Додаємо текстовий контент
        text = ET.SubElement(item, "text")
        text.text = record["content"]
        
        if record["type"] == "news":  # Якщо це новина
            city = ET.SubElement(item, "city")
            city.text = record["additional"]
            timestamp = ET.SubElement(item, "timestamp")
            timestamp.text = datetime.now().strftime("%d/%m/%Y %H.%M")
            news.append(item)
        elif record["type"] == "ad":  # Якщо це реклама
            expiration_date = ET.SubElement(item, "expiration_date")
            expiration_date.text = record["additional"]
            days_left = ET.SubElement(item, "days_left")
            # Розраховуємо кількість днів до закінчення акції
            exp_date = datetime.strptime(record["additional"], '%d-%m-%Y')
            days = (exp_date - datetime.now()).days
            days_left.text = str(max(0, days))
            advertisements.append(item)
        else:  # Якщо це жарт
            funny_rating = ET.SubElement(item, "funny_rating")
            funny_rating.text = record["additional"]
            funny_rating_word = ET.SubElement(item, "funny_rating_word")
            # Конвертуємо число в текстовий опис
            numbers_dict = {
                '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
                '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten'
            }
            funny_rating_word.text = numbers_dict.get(record["additional"], "unknown")
            jokes.append(item)
    
    return root

def create_files(base_filename, num_records=10):
    """
    Створює файли з згенерованим контентом у форматах TXT, JSON та XML
    
    Args:
        base_filename (str): Базова назва файлу без розширення
        num_records (int): Кількість записів для генерації
        
    Returns:
        bool: True якщо файли успішно створено, False у випадку помилки
    """
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
        
        # Створюємо xml файл
        xml_filename = base_filename + ".xml"
        root = create_xml_content(records)  # Створюємо XML структуру
        tree = ET.ElementTree(root)  # Створюємо XML дерево
        # tree.write(xml_filename, encoding='utf-8', xml_declaration=True)  # Зберігаємо XML файл
        # Додаємо відступи для кращої читабельності
        xml_str = ET.tostring(root, encoding='utf-8')
        reparsed = minidom.parseString(xml_str)
        with open(xml_filename, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="    "))
        


        print(f"Файли успішно створено: {txt_filename}, {json_filename} та {xml_filename}")
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