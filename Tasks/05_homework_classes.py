"""
Homework:
Create a tool, which will do user generated news feed:
 - User select what data type he wants to add
 - Provide record type required data
 - Record is published on text file in special format

You need to implement:
 - News – text and city as input. Date is calculated during publishing.
 - Privat ad – text and expiration date as input. Day left is calculated during publishing.
 - Your unique one with unique publish rules.

Each new record should be added to the end of file. Commit file in git for review.
"""

from datetime import datetime


# Створюємо класс для отримання контенту та форматування його для збереження
# На виході маємо готовий для запису кусок контенту
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


# Для новин в нас додається до класу Контент ще місто, звідки новина.
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


class ContentManager:
    def __init__(self):
        self.contents = []

    def user_choice(self):
        while True:
            print("Choose content type: 1 - News, 2 - Ad, 3 - Quote, 4 - Exit")
            try:
                choice = int(input(">"))
                if 1 <= choice <= 4:
                    return choice
                else:
                    print("Please, choose a valid option (1-4).")
            except ValueError:
                print("Please enter a number (1-4).")

    def content_input(self):
        print("Enter content:")
        return input(">")

    def additional_info(self, choice):
        match choice:
            case 1:
                return input("Enter the city: ")
            case 2:
                return input("Enter the expiration date (DD-MM-YYYY)")
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

    def save_content(self, content):
        with open("content_storage.txt", "a", encoding="utf-8") as file:
            file.write(content.format_content())

    def run(self):
        while True:
            choice = self.user_choice()
            if choice == 4:
                print("Exiting program.")
                break

            content = self.create_content(choice)
            try:
                self.save_content(content)
                print("Content saved successfully.")
            except FileNotFoundError:
                print("Can't find file")


if __name__ == "__main__":
    manager = ContentManager()
    manager.run()
