from collections import Counter
import os
import csv
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
content_file = os.path.join(current_dir, "content_storage.txt")
csv_words = os.path.join(current_dir, "csv_words.csv")
csv_counter = os.path.join(current_dir, "csv_counts.csv")

def analyze_words(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        content = file.read()
    
    words = re.findall(r'\b\w+\b', content.lower())
    word_counter = Counter(words)
    
    return word_counter


def analyze_letters(filename):
    # Читаємо файл
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
   
    # Підраховуємо тільки літери
    letters = [char for char in content if char.isalpha()]
    letter_counter = Counter(letters)
    
    # Загальна кількість літер для відсотків
    total_letters = len(letters)
   
    # Створюємо розширений словник зі статистикою
    letter_stats = {}
    for letter, count in letter_counter.items():
        letter_stats[letter] = {
            'count': count,
            'uppercase': sum(1 for c in content if c == letter.upper()),
            'percentage': round((count / total_letters) * 100, 2)
        }
   
    return letter_stats
# letter_stats - словник із вкладеним словником 
# {'літера' : {'count': кількість, 'uppercase': кількість, 'percentage': кількість}}

# Використання
words = analyze_words(content_file)
letters = analyze_letters(content_file)

# Записуємо в csv
def generate_words_csv():
    with open(csv_words, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=":", quoting=csv.QUOTE_ALL)
        writer.writerow(['word', 'count'])
        for word, vcount in sorted(words.items()):
            writer.writerow([word, vcount])

def generate_letters_csv():
    with open(csv_counter, 'w', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=":", quoting=csv.QUOTE_ALL)
        writer.writerow(['letter', 'count_all', 'count_uppercase', 'percentage'])
        for letter, stat in sorted(letters.items()):
            writer.writerow([letter, stat['count'], stat['uppercase'], stat['percentage']])

generate_words_csv()
generate_letters_csv()

