from datetime import datetime
import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from csv_word_count_v2 import generate_words_csv
from csv_word_count_v2 import generate_letters_csv

def normalize_text(text):
    """
    Нормалізує текст: видаляє зайві пробіли та капіталізує першу літеру
    Args:
        text (str): Вхідний текст для нормалізації
    Returns:
        str: Нормалізований текст
    """
    text = ' '.join(text.split())
    return text[0].upper() + text[1:] if text else text

def prettify_xml(elem):
    """
    Форматує XML документ для кращої читабельності
    Args:
        elem (Element): XML елемент для форматування
    Returns:
        str: Відформатований XML рядок
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

class Content:
    def __init__(self, text):
        self.text = text
        self.timestamp = datetime.now()

    def format_content(self):
        raise NotImplementedError("Підкласи мають реалізувати метод format_content")
    
    def to_json(self):
        raise NotImplementedError("Підкласи мають реалізувати метод to_json")
    
    def to_xml_element(self):
        raise NotImplementedError("Підкласи мають реалізувати метод to_xml_element")

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
    
    def to_xml_element(self):
        item = ET.Element("item")
        text_elem = ET.SubElement(item, "text")
        text_elem.text = self.text
        city_elem = ET.SubElement(item, "city")
        city_elem.text = self.city
        timestamp_elem = ET.SubElement(item, "timestamp")
        timestamp_elem.text = self.timestamp.strftime('%d/%m/%Y %H.%M')
        return item

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
    
    def to_xml_element(self):
        item = ET.Element("item")
        text_elem = ET.SubElement(item, "text")
        text_elem.text = self.text
        exp_date_elem = ET.SubElement(item, "expiration_date")
        exp_date_elem.text = self.expiration_date.strftime('%d/%m/%Y')
        days_left_elem = ET.SubElement(item, "days_left")
        days_left_elem.text = str(self.days_left())
        return item

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
    
    def _number_to_word(self, num):
        numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 
                  'six', 'seven', 'eight', 'nine', 'ten']
        return numbers[num]
    
    def to_xml_element(self):
        item = ET.Element("item")
        text_elem = ET.SubElement(item, "text")
        text_elem.text = self.text
        rating_elem = ET.SubElement(item, "funny_rating")
        rating_elem.text = str(self.funny_rating)
        rating_word_elem = ET.SubElement(item, "funny_rating_word")
        rating_word_elem.text = self._number_to_word(self.funny_rating)
        return item

class ContentManager:
    def __init__(self):
        self.xml_root = None
        self.load_or_create_xml()

    def load_or_create_xml(self):
        xml_filename = os.path.join(os.path.dirname(__file__), "generated_content.xml")
        try:
            tree = ET.parse(xml_filename)
            self.xml_root = tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            self.xml_root = ET.Element("content_feed")
            ET.SubElement(self.xml_root, "news")
            ET.SubElement(self.xml_root, "advertisements")
            ET.SubElement(self.xml_root, "jokes")

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
            case "ad":
                return AdContent(content, additional_info)
            case "joke":
                return JokeContent(content, additional_info)
            case _:
                raise ValueError(f"Unknown record type: {record_type}")

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
        content_type = content.to_json()["type"]
        if content_type == "news":
            section = self.xml_root.find("news")
        elif content_type == "ad":
            section = self.xml_root.find("advertisements")
        else:  # joke
            section = self.xml_root.find("jokes")
        
        section.append(content.to_xml_element())
        
        # Save XML file with pretty formatting
        xml_filename = os.path.join(os.path.dirname(__file__), "content_storage.xml")
        pretty_xml = prettify_xml(self.xml_root)
        with open(xml_filename, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)

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