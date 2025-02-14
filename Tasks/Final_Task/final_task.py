"""
Create a tool which will calculate straight-line distance between different cities based on coordinates:
 1. User will provide two city names by console interface
 2. If tool do not know about city coordinates, it will ask user for input and store it in SQLite database for future use
 3. Return distance between cities in kilometers

Do not forgot that Earth is a sphere, so length of one degree is different.
"""
import os
import sqlite3
import math

# Перевіряємо шлях. БД буде розташована поряд з цим файлом.
current_dir = os.path.dirname(os.path.abspath(__file__))
file_db = os.path.join(current_dir, "cities.db")

def format_city_name(city_name):
    """Форматування назви міста"""
    # Розділяємо назву за дефісом, форматуємо кожну частину і з'єднуємо назад
    parts = city_name.strip().split('-')
    formatted_parts = [part.strip().title() for part in parts]
    return '-'.join(formatted_parts)

def create_db(file_db=file_db):
    db_exists = os.path.exists(file_db)
    with sqlite3.connect(file_db) as conn:
        cursor = conn.cursor()
        # створюємо таблицю
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                city_name TEXT PRIMARY KEY,
                latitude REAL,
                longitude REAL
            )
        """)
        conn.commit()
        if not db_exists:
            print("New database created successfully")
        else:
            print("Using existing database")
        

def get_city_coordinates(city_name):
    formatted_name = format_city_name(city_name)
    with sqlite3.connect(file_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT latitude, longitude FROM cities WHERE city_name = ?", (formatted_name,))
        result = cursor.fetchone()
    return result

def get_coordinates_from_user(city_name):
    """Запит координат міста у користувача"""
    formatted_name = format_city_name(city_name)
    print(f"\nМісто {formatted_name} не знайдено в базі даних.")
    while True:
        try:
            latitude = float(input(f"Введіть широту для міста {formatted_name} (наприклад, 50.4501): "))
            longitude = float(input(f"Введіть довготу для міста {formatted_name} (наприклад, 30.5234): "))
            
            # Базова перевірка координат
            if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                add_city_to_db(formatted_name, latitude, longitude)
                return (latitude, longitude)
            else:
                print("Помилка: некоректні координати. Широта має бути від -90 до 90, довгота від -180 до 180")
        except ValueError:
            print("Помилка: введіть числове значення координат")

def add_city_to_db(city_name, latitude, longitude):
    """Додавання нового міста до бази даних"""
    with sqlite3.connect(file_db) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO cities VALUES (?, ?, ?)', (city_name, latitude, longitude))
            conn.commit()
            print(f"Місто {city_name} успішно додано до бази даних")
        except sqlite3.IntegrityError:
            print(f"Місто {city_name} вже існує в базі даних")

def calculate_distance(lat1, lon1, lat2, lon2):
    """Розрахунок відстані між двома точками за координатами"""
    R = 6371  # Радіус Землі в кілометрах
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c
    
    return round(distance, 2)

def main():
    # якщо нема БД, то створюємо її
    create_db()

    # отримуємо від користувача міста, відстань між якими шукаємо
    origin_city = input("Enter the name of the city from which we will calculate the distance: ").strip()
    target_city = input("Enter the name of the city to which we will calculate the distance: ").strip()
    
    # форматуємо назви міст
    formatted_origin = format_city_name(origin_city)
    formatted_target = format_city_name(target_city)
    
    # шукаємо координати міст в БД, якщо ні, то питаємо користувача
    coords_origin = get_city_coordinates(formatted_origin)
    if coords_origin is None:
        coords_origin = get_coordinates_from_user(formatted_origin)

    coords_target = get_city_coordinates(formatted_target)
    if coords_target is None:
        coords_target = get_coordinates_from_user(formatted_target)

    # розрахунок відстані
    distance = calculate_distance(coords_origin[0], coords_origin[1], coords_target[0], coords_target[1])
    print(f"\nВідстань між {formatted_origin} та {formatted_target}: {distance} км")
    
if __name__ == "__main__":
    main()