"""
Content Management System
------------------------
A system for managing different types of content (news, ads, jokes) with multiple storage backends.
Supports text, JSON, XML file storage and SQLite database.

Features:
- Content validation and normalization
- Duplicate prevention using content hashing
- Multiple storage formats
- Batch processing from files
- Word and letter counting analytics

Author: [Your Name]
Date: [Current Date]
"""

from datetime import datetime
import os
import json
import pyodbc
import hashlib
from csv_word_count_v2 import generate_words_csv
from csv_word_count_v2 import generate_letters_csv
from xml.etree import ElementTree as ET

def normalize_text(text: str) -> str:
    """
    Normalizes input text by removing extra spaces and capitalizing first letter.
    
    Args:
        text (str): Input text to normalize
        
    Returns:
        str: Normalized text
    """
    text = ' '.join(text.split())
    return text[0].upper() + text[1:] if text else text

class DBManager:
    """
    Manages SQLite database operations for content storage.
    Handles creation and maintenance of database tables.
    Implements methods for saving different types of content.
    """
    
    def __init__(self):
        """Initializes database connection and creates required tables."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "content_storage.db")
        self.connection_string = f'DRIVER={{SQLite3 ODBC Driver}};Direct=True;Database={self.db_path};String Types=Unicode'
        self.create_tables()

    def get_connection(self):
        """Creates and returns a new database connection."""
        return pyodbc.connect(self.connection_string)

    def create_tables(self):
        """Creates necessary database tables if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Create tables with proper schemas
            # Add table creation SQL...

    def get_content_hash(self, content: str) -> str:
        """
        Creates SHA256 hash of content to prevent duplicates.
        
        Args:
            content (str): Content to hash
            
        Returns:
            str: SHA256 hash of content
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def save_news(self, text: str, city: str) -> bool:
        """
        Saves news content to database.
        
        Args:
            text (str): News content
            city (str): City where news occurred
            
        Returns:
            bool: True if save successful, False if duplicate
            
        Raises:
            pyodbc.Error: If database operation fails
        """
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

class Content:
    """
    Base class for all content types.
    Provides common functionality and enforces interface.
    """
    
    def __init__(self, text: str):
        """
        Initialize content with text and timestamp.
        
        Args:
            text (str): Content text
        """
        self.text = text
        self.timestamp = datetime.now()

    def format_content(self):
        """Format content for text output. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement format_content")

class NewsContent(Content):
    """
    Handles news content with city information.
    Formats news for different output formats (text, JSON, XML).
    """
    
    def __init__(self, text: str, city: str):
        """
        Initialize news content.
        
        Args:
            text (str): News content
            city (str): City where news occurred
        """
        super().__init__(text)
        self.city = city

    def format_content(self) -> str:
        """
        Format news content for text output.
        
        Returns:
            str: Formatted news content
        """
        return (
            f"News -------------------------\n"
            f"{self.text}\n"
            f"{self.city}, {self.timestamp.strftime('%d/%m/%Y %H.%M')}\n"
            f"\n"
        )

class ContentManager:
    """
    Main class coordinating all content operations.
    Handles user input, file processing, and storage in multiple formats.
    """
    
    def __init__(self):
        """Initialize content manager with database manager."""
        self.db_manager = DBManager()

    def process_file(self) -> list:
        """
        Process batch content from file.
        
        Returns:
            list: List of Content objects created from file
            
        Raises:
            Exception: If file processing fails
        """
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
            
            return records
            
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return []

    def run(self):
        """
        Main program loop.
        Handles user input and content processing.
        """
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