import sqlite3
import math
import os

# Шлях до БД
current_dir = os.path.dirname(os.path.abspath(__file__))
file_db = os.path.join(current_dir, "cities.db")

def create_database():
    """Створення бази даних міст, якщо вона не існує"""
    conn = sqlite3.connect('cities.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            name TEXT PRIMARY KEY,
            latitude REAL,
            longitude REAL
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM cities')
    if cursor.fetchone()[0] == 0:
        sample_cities = [
            ('Київ', 50.4501, 30.5234),
            ('Львів', 49.8397, 24.0297),
            ('Харків', 49.9935, 36.2304),
            ('Одеса', 46.4825, 30.7233),
            ('Дніпро', 48.4647, 35.0462)
        ]
        cursor.executemany('INSERT INTO cities VALUES (?, ?, ?)', sample_cities)
    
    conn.commit()
    conn.close()

def add_city_to_db(name, latitude, longitude):
    """Додавання нового міста до бази даних"""
    conn = sqlite3.connect('cities.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO cities VALUES (?, ?, ?)', (name, latitude, longitude))
        conn.commit()
        print(f"Місто {name} успішно додано до бази даних")
    except sqlite3.IntegrityError:
        print(f"Місто {name} вже існує в базі даних")
    finally:
        conn.close()

def get_coordinates_from_user(city_name):
    """Запит координат міста у користувача"""
    print(f"\nМісто {city_name} не знайдено в базі даних.")
    while True:
        try:
            latitude = float(input(f"Введіть широту для міста {city_name} (наприклад, 50.4501): "))
            longitude = float(input(f"Введіть довготу для міста {city_name} (наприклад, 30.5234): "))
            
            # Базова перевірка координат
            if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                add_city_to_db(city_name, latitude, longitude)
                return (latitude, longitude)
            else:
                print("Помилка: некоректні координати. Широта має бути від -90 до 90, довгота від -180 до 180")
        except ValueError:
            print("Помилка: введіть числове значення координат")

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

def get_city_coordinates(city_name):
    """Отримання координат міста з бази даних"""
    conn = sqlite3.connect('cities.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT latitude, longitude FROM cities WHERE name = ?', (city_name,))
    result = cursor.fetchone()
    
    conn.close()
    return result

def main():
    create_database()
    
    city1 = input("Введіть початкове місто: ")
    city2 = input("Введіть кінцеве місто: ")
    
    # Отримання координат першого міста
    coords1 = get_city_coordinates(city1)
    if coords1 is None:
        coords1 = get_coordinates_from_user(city1)
    
    # Отримання координат другого міста
    coords2 = get_city_coordinates(city2)
    if coords2 is None:
        coords2 = get_coordinates_from_user(city2)
    
    # Розрахунок та виведення відстані
    distance = calculate_distance(coords1[0], coords1[1], coords2[0], coords2[1])
    print(f"\nВідстань між {city1} та {city2}: {distance} км")

if __name__ == "__main__":
    main()