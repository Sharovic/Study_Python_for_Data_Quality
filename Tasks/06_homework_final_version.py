from datetime import datetime
from pathlib import Path
import os
import re


def normalize_text(text):
    """Normalize text by removing extra spaces and making first letter capital"""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text.strip())
    # Capitalize first letter
    return text[0].upper() + text[1:] if text else text


class Content:
    def __init__(self, text):
        self.text = text
        self.timestamp = datetime.now()

    def format_content(self):
        return (
            f"{'-'*30}\n"
            f"{self.text}\n"
            f"Published on: {self.timestamp.strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"{'-' * 30}\n"
        )


class NewsContent(Content):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city

    def format_content(self):
        return (
            f"{'-' * 30}\n"
            f"{self.text}\n"
            f"{self.city}\n"
            f"Published on: {self.timestamp.strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"{'-' * 30}\n"
        )


class AdContent(Content):
    def __init__(self, text, expiration_date):
        super().__init__(text)
        self.expiration_date = datetime.strptime(expiration_date, "%d-%m-%Y")

    def days_left(self):
        delta = self.expiration_date - datetime.now()
        return max(delta.days, 0)

    def format_content(self):
        return (
            f"{'-' * 30}\n"
            f"Ad: {self.text}\n"
            f"Expires on: {self.expiration_date.strftime('%d-%m-%Y')}\n"
            f"Days left: {self.days_left()}\n"
            f"{'-' * 30}\n"
        )


class QuoteContent(Content):
    def __init__(self, text, author):
        super().__init__(text)
        self.author = author

    def format_content(self):
        return (
            f"{'-'*30}\n"
            f"Quote: {self.text}\n"
            f"Author: {self.author}\n"
            f"Published on: {self.timestamp.strftime('%d-%m-%Y %H:%M:%S')}\n"
            f"{'-'*30}\n"
        )


class FileProcessor:
    def __init__(self, default_folder="input_files"):
        self.default_folder = default_folder
        Path(default_folder).mkdir(exist_ok=True)
    
    def parse_record(self, lines):
        """Parse a single record from lines of text."""
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
            case "quote":
                return QuoteContent(content, additional_info)
            case _:
                raise ValueError(f"Unknown record type: {record_type}")
    
    def process_file(self, filepath=None):
        """Process a single file and create content records."""
        if filepath is None:
            # Get the first file from default folder
            files = list(Path(self.default_folder).glob("*.txt"))
            if not files:
                raise FileNotFoundError("No files to process in default folder")
            filepath = files[0]
        else:
            filepath = Path(filepath)
            
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
            
        records = []
        current_record = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if line == "---":  # Record separator
                        if current_record:
                            record = self.parse_record(current_record)
                            if record:
                                records.append(record)
                            current_record = []
                    else:
                        current_record.append(line)
                
                # Don't forget the last record
                if current_record:
                    record = self.parse_record(current_record)
                    if record:
                        records.append(record)
            
            # Remove file after successful processing
            os.remove(filepath)
            return records
            
        except Exception as e:
            print(f"Error processing file {filepath}: {str(e)}")
            return []


class ContentManager:
    def __init__(self):
        self.contents = []
        self.file_processor = FileProcessor()

    def user_choice(self):
        while True:
            print("\nChoose option:")
            print("1 - News")
            print("2 - Ad")
            print("3 - Quote")
            print("4 - Process file")
            print("5 - Exit")
            try:
                choice = int(input(">"))
                if 1 <= choice <= 5:
                    return choice
                else:
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
                return input("Enter the author: ")

    def create_content(self, choice):
        text = self.content_input()
        additional = self.additional_info(choice)
        match choice:
            case 1:
                return NewsContent(text, additional)
            case 2:
                return AdContent(text, additional)
            case 3:
                return QuoteContent(text, additional)

    def process_file_input(self):
        print("Enter file path (press Enter to use default folder):")
        filepath = input().strip()
        return filepath if filepath else None

    def save_content(self, content):
        with open("content_storage.txt", "a", encoding="utf-8") as file:
            file.write(content.format_content())

    def run(self):
        while True:
            choice = self.user_choice()
            if choice == 5:
                print("Exiting program.")
                break
            
            if choice == 4:
                try:
                    filepath = self.process_file_input()
                    records = self.file_processor.process_file(filepath)
                    for record in records:
                        self.save_content(record)
                    print(f"Processed {len(records)} records successfully.")
                except Exception as e:
                    print(f"Error processing file: {str(e)}")
            else:
                content = self.create_content(choice)
                try:
                    self.save_content(content)
                    print("Content saved successfully.")
                except FileNotFoundError:
                    print("Can't find file")


if __name__ == "__main__":
    manager = ContentManager()
    manager.run()