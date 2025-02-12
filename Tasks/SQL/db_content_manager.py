from datetime import datetime
import os
import json
import pyodbc
import hashlib
from csv_word_count_v2 import generate_words_csv
from csv_word_count_v2 import generate_letters_csv
from xml.etree import ElementTree as ET

def normalize_text(text):
    text = ' '.join(text.split())
    return text[0].upper() + text[1:] if text else text

class DBManager:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "content_storage.db")
        self.connection_string = f'DRIVER={{SQLite3 ODBC Driver}};Direct=True;Database={self.db_path};String Types=Unicode'
        self.create_tables()

    def get_connection(self):
        return pyodbc.connect(self.connection_string)

    def create_tables(self):
        with self.get_connection() as conn:
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

    def get_content_hash(self, content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def save_news(self, text, city):
        content_hash = self.get_content_hash(text)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO news (content, city, content_hash) VALUES (?, ?, ?)",
                    (text, city, content_hash)
                )
                conn.commit()
                return True
            except pyodbc.Error as e:
                if 'UNIQUE constraint failed' in str(e):
                    print("Warning: This news content already exists in the database")
                    return False
                raise

    def save_ad(self, text, expiration_date):
        content_hash = self.get_content_hash(text)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO ads (content, expiration_date, content_hash) VALUES (?, ?, ?)",
                    (text, expiration_date, content_hash)
                )
                conn.commit()
                return True
            except pyodbc.Error as e:
                if 'UNIQUE constraint failed' in str(e):
                    print("Warning: This ad content already exists in the database")
                    return False
                raise

    def save_joke(self, text, funny_rating):
        content_hash = self.get_content_hash(text)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO joke (content, funny_rating, content_hash) VALUES (?, ?, ?)",
                    (text, funny_rating, content_hash)
                )
                conn.commit()
                return True
            except pyodbc.Error as e:
                if 'UNIQUE constraint failed' in str(e):
                    print("Warning: This joke content already exists in the database")
                    return False
                raise

class Content:
    def __init__(self, text):
        self.text = text
        self.timestamp = datetime.now()

    def format_content(self):
        raise NotImplementedError("Subclasses must implement format_content")
    
    def to_json(self):
        raise NotImplementedError("Subclasses must implement to_json")
    
    def to_xml(self):
        raise NotImplementedError("Subclasses must implement to_xml")
    
    def save_to_db(self, db_manager):
        raise NotImplementedError("Subclasses must implement save_to_db")

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
    
    def to_json(self):
        return {
            "type": "news",
            "text": self.text,
            "city": self.city,
            "timestamp": self.timestamp.strftime('%d/%m/%Y %H.%M')
        }
    
    def to_xml(self):
        news = ET.Element("news")
        ET.SubElement(news, "text").text = self.text
        ET.SubElement(news, "city").text = self.city
        ET.SubElement(news, "timestamp").text = self.timestamp.strftime('%d/%m/%Y %H.%M')
        return news
    
    def save_to_db(self, db_manager):
        return db_manager.save_news(self.text, self.city)

class AdContent(Content):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.strptime(expiration_date, "%d-%m-%Y")

    def days_left(self):
        delta = self.expiration_date - datetime.now()
        return max(delta.days, 0)

    def format_content(self):
        return (
            f"Private Ad ------------------\n"
            f"{self.text}\n"
            f"Actual until: {self.expiration_date.strftime('%d/%m/%Y')}, {self.days_left()} days left\n"
            f"\n"
        )
    
    def to_json(self):
        return {
            "type": "ad",
            "text": self.text,
            "expiration_date": self.expiration_date.strftime('%d/%m/%Y'),
            "days_left": self.days_left()
        }
    
    def to_xml(self):
        ad = ET.Element("ad")
        ET.SubElement(ad, "text").text = self.text
        ET.SubElement(ad, "expiration_date").text = self.expiration_date.strftime('%d/%m/%Y')
        ET.SubElement(ad, "days_left").text = str(self.days_left())
        return ad
    
    def save_to_db(self, db_manager):
        return db_manager.save_ad(self.text, self.expiration_date.strftime('%d-%m-%Y'))

class JokeContent(Content):
    def __init__(self, text, funny_rating):
        super().__init__(text)
        self.funny_rating = min(max(1, int(funny_rating)), 10)

    def format_content(self):
        return (
            f"Joke of the day ------------\n"
            f"{self.text}\n"
            f"Funny meter – {self._number_to_word(self.funny_rating)} of ten\n"
            f"\n"
        )
    
    def to_json(self):
        return {
            "type": "joke",
            "text": self.text,
            "funny_rating": self.funny_rating,
            "funny_rating_word": self._number_to_word(self.funny_rating)
        }
    
    def to_xml(self):
        joke = ET.Element("joke")
        ET.SubElement(joke, "text").text = self.text
        ET.SubElement(joke, "funny_rating").text = str(self.funny_rating)
        ET.SubElement(joke, "funny_rating_word").text = self._number_to_word(self.funny_rating)
        return joke
    
    def save_to_db(self, db_manager):
        return db_manager.save_joke(self.text, str(self.funny_rating))
    
    def _number_to_word(self, num):
        numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 
                  'six', 'seven', 'eight', 'nine', 'ten']
        return numbers[num]

class ContentManager:
    def __init__(self):
        self.db_manager = DBManager()

    def user_choice(self):
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
        print("Enter the content (For quit type 'quit'):")
        lines = []
        while True:
            line = input()
            if line.strip().lower() == "quit":
                break
            lines.append(line)
        return normalize_text("\n".join(lines))

    def additional_info(self, choice):
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
        text = self.content_input()
        additional = self.additional_info(choice)
        match choice:
            case 1:
                return NewsContent(text, additional)
            case 2:
                return AdContent(text, additional)
            case 3:
                return JokeContent(text, additional)

    def save_content(self, content):
        # Save to text file
        txt_filename = os.path.join(os.path.dirname(__file__), "content_storage.txt")
        with open(txt_filename, "a", encoding="utf-8") as file:
            if file.tell() == 0:
                file.write("News feed:\n")
            file.write(content.format_content())
        
        # Save to JSON file
        json_filename = os.path.join(os.path.dirname(__file__), "content_storage.json")
        try:
            with open(json_filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.append(content.to_json())
        with open(json_filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

        # Save to XML file
        xml_filename = os.path.join(os.path.dirname(__file__), "content_storage.xml")
        try:
            tree = ET.parse(xml_filename)
            root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            root = ET.Element("content")
            tree = ET.ElementTree(root)
        
        root.append(content.to_xml())
        tree.write(xml_filename, encoding="utf-8", xml_declaration=True)

        # Save to database
        content.save_to_db(self.db_manager)

    def process_file(self):
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
                
                if current_record:
                    record = self.parse_record(current_record)
                    if record:
                        records.append(record)
            
            return records
            
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return []

    def parse_record(self, lines):
        if not lines:
            return None
            
        record_type = lines[0].strip().lower()
        content = lines[1].strip() if len(lines) > 1 else ""
        additional_info = lines[2].strip() if len(lines) > 2 else ""
        
        match record_type:
            case "news":
                return NewsContent(content, additional_info)
            case "ad" | "ads":
                return AdContent(content, additional_info)
            case "joke":
                return JokeContent(content, additional_info)
            case _:
                raise ValueError(f"Unknown record type: {record_type}")

    def run(self):
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