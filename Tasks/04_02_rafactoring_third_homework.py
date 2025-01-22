"""
 Refactor homeworks from module 2 and 3 using functional approach with decomposition.
"""

# Refactoring homework 3
# https://github.com/Sharovic/Study_Python_for_Data_Quality/blob/main/Tasks/03_homework.py

import re
import string


def count_whitespace_characters(text):
    """Counts all whitespace characters (spaces, tabs, newlines) in the text."""
    return sum(text.count(char) for char in string.whitespace)


def normalize_text(text):
    """Normalizes text by fixing letter cases and capitalizing the first word of each sentence."""
    sentences = re.sub(r"\s+", " ", text).strip().split(".")
    normalized_sentences = []

    for sentence in sentences:
        sentence = sentence.lower().strip().capitalize()
        sentence = re.sub(r"\biz\b", "is", sentence)  # Replace incorrect 'iz' with 'is'
        if sentence:  # Avoid empty sentences
            normalized_sentences.append(sentence + ".")
    return normalized_sentences


def extract_last_words(sentences):
    """Extracts the last word from each sentence."""
    return [
        sentence.strip().split()[-1].strip(".") for sentence in sentences if sentence
    ]


def process_text(text):
    """Processes the text by normalizing it, fixing 'iz', extracting last words, and counting whitespaces."""
    whitespace_count = count_whitespace_characters(text)
    normalized_sentences = normalize_text(text)
    last_words = extract_last_words(normalized_sentences)
    extended_paragraph = (
        " ".join(normalized_sentences) + " " + " ".join(last_words) + "."
    )

    return {
        "whitespace_count": whitespace_count,
        "normalized_text": normalized_sentences,
        "last_words": last_words,
        "extended_paragraph": extended_paragraph,
    }


# Input text
incoming_string = r"""
homEwork:
  tHis iz your homeWork, copy these Text to variable.

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# Process the text
result = process_text(incoming_string)

# Output the results
print(f"Total number of whitespace characters: {result['whitespace_count']}")
print("\nNormalized text:")
print(" ".join(result["normalized_text"]))
print("\nList of last words from each sentence:")
print(result["last_words"])
print("\nExtended paragraph with last words added:")
print(result["extended_paragraph"])
