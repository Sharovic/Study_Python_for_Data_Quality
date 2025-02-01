from datetime import datetime
import os
from csv_word_count_v2 import generate_words_csv
from csv_word_count_v2 import generate_letters_csv

# Функція для нормалізації тексту (видалення зайвих пробілів та капіталізація першої літери)
def normalize_text(text):
    text = ' '.join(text.split())  # Видаляємо зайві пробіли
    return text[0].upper() + text[1:] if text else text

# Базовий клас для всіх типів контенту
class Content:
    def __init__(self, text):
        self.text = text
        self.timestamp = datetime.now()  # Зберігаємо час створення

    def format_content(self):
        raise NotImplementedError("Підкласи мають реалізувати метод format_content")

# Клас для новин
class NewsContent(Content):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def format_content(self):
        return (
            f"News -------------------------\n"
            f"{self.text}\n"
            f"{self.city}, {self.timestamp.strftime('%d/%m/%Y %H.%M')}\n"
            f"\n"
        )

# Клас для оголошень
class AdContent(Content):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.strptime(expiration_date, "%d-%m-%Y")

    def days_left(self):
        # Розраховуємо кількість днів до закінчення терміну дії
        delta = self.expiration_date - datetime.now()
        return max(delta.days, 0)

    def format_content(self):
        return (
            f"Private Ad ------------------\n"
            f"{self.text}\n"
            f"Actual until: {self.expiration_date.strftime('%d/%m/%Y')}, {self.days_left()} days left\n"
            f"\n"
        )

# Клас для жартів
class JokeContent(Content):
    def __init__(self, text, funny_rating):
        super().__init__(text)
        # Обмежуємо рейтинг від 1 до 10
        self.funny_rating = min(max(1, int(funny_rating)), 10)

    def format_content(self):
        return (
            f"Joke of the day ------------\n"
            f"{self.text}\n"
            f"Funny meter – {self._number_to_word(self.funny_rating)} of ten\n"
            f"\n"
        )
    
    def _number_to_word(self, num):
        # Конвертуємо числа в слова
        numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 
                  'six', 'seven', 'eight', 'nine', 'ten']
        return numbers[num]

# Головний клас для управління контентом
class ContentManager:
    def user_choice(self):
        # Показуємо меню користувачу та отримуємо вибір
        while True:
            print("\nChoose option:")
            print("1 - News")
            print("2 - Ad")
            print("3 - Joke")
            print("4 - Process file")
            print("5 - Exit")
            try:
                choice = int(input(">"))
                if 1 <= choice <= 5:
                    return choice
                print("Please, choose a valid option (1-5).")
            except ValueError:
                print("Please enter a number (1-5).")

    def content_input(self):
        # Отримуємо текст контенту від користувача
        print("Enter the content (For quit type 'quit'):")
        lines = []
        while True:
            line = input()
            if line.strip().lower() == "quit":
                break
            lines.append(line)
        return normalize_text("\n".join(lines))

    def additional_info(self, choice):
        # Отримуємо додаткову інформацію в залежності від типу контенту
        match choice:
            case 1:
                return input("Enter the city: ")
            case 2:
                return input("Enter the expiration date (DD-MM-YYYY): ")
            case 3:
                while True:
                    try:
                        rating = int(input("Enter funny rating (1-10): "))
                        if 1 <= rating <= 10:
                            return str(rating)
                        print("Please enter a number between 1 and 10.")
                    except ValueError:
                        print("Please enter a valid number.")

    def create_content(self, choice):
        # Створюємо об'єкт контенту відповідного типу
        text = self.content_input()
        additional = self.additional_info(choice)
        match choice:
            case 1:
                return NewsContent(text, additional)
            case 2:
                return AdContent(text, additional)
            case 3:
                return JokeContent(text, additional)

    def process_file(self):
        # Читаємо записи з файлу generated_content.txt
        try:
            records = []
            current_record = []
            
            filename = os.path.join(os.path.dirname(__file__), "generated_content.txt")
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line == "---":
                        if current_record:
                            record = self.parse_record(current_record)
                            if record:
                                records.append(record)
                            current_record = []
                    else:
                        current_record.append(line)
                
                if current_record:  # Обробляємо останній запис
                    record = self.parse_record(current_record)
                    if record:
                        records.append(record)
            
            return records
            
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return []

    def parse_record(self, lines):
        # Розбираємо окремий запис з файлу
        if not lines:
            return None
            
        record_type = lines[0].strip().lower()
        content = lines[1].strip() if len(lines) > 1 else ""
        additional_info = lines[2].strip() if len(lines) > 2 else ""
        
        match record_type:
            case "news":
                return NewsContent(content, additional_info)
            case "ad":
                return AdContent(content, additional_info)
            case "joke":
                return JokeContent(content, additional_info)
            case _:
                raise ValueError(f"Unknown record type: {record_type}")

    def save_content(self, content):
        # Записуємо контент у файл content_storage.txt
        filename = os.path.join(os.path.dirname(__file__), "content_storage.txt")
        with open(filename, "a", encoding="utf-8") as file:
            if file.tell() == 0:  # Якщо файл порожній, додаємо заголовок
                file.write("News feed:\n")
            file.write(content.format_content())

    def statistic_to_csv(self,):
        # Сюди вставляти буду з того, що зараз тестую в sample.py
        pass

    def run(self):
        # Головний цикл програми
        while True:
            choice = self.user_choice()
            if choice == 5:
                print("Exiting program.")
                break
            
            if choice == 4:
                try:
                    records = self.process_file()
                    for record in records:
                        self.save_content(record)
                    print(f"Processed {len(records)} records successfully.")
                    generate_words_csv()
                    generate_letters_csv()
                except Exception as e:
                    print(f"Error processing file: {str(e)}")
            else:
                content = self.create_content(choice)
                try:
                    self.save_content(content)
                    print("Content saved successfully.")
                    generate_words_csv()
                    generate_letters_csv()
                except Exception as e:
                    print(f"Error saving content: {str(e)}")

if __name__ == "__main__":
    manager = ContentManager()
    manager.run()