"""
homEwork:
	tHis iz your homeWork, copy these Text to variable.

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.

"""

# Import necessary modules
import re
import string
from collections import Counter

# Our incoming string
incoming_string = r"""

homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""
# Create Counter object from input string
c = Counter(incoming_string)

# Count all whitespace characters using Counter and string.whitespace
whitespace_counter = sum(c[char] for char in string.whitespace)

# Print the total number of whitespace characters
print(f"Total summa of whitespace is {whitespace_counter}")

# Define list to store last word from each sentence.
final_sentence = []

# Remove multiply whitespaces, split by periods into sentences
text = re.sub(r"\s+", " ", incoming_string).strip().split(".")

# Define pattern for replacing "iz" with "is"
subsitute_char = r"\biz\b"

# Process each sentence
for sentence in text:
    # Conver to lowercase and capitalize first letter
    edited_sentence = sentence.lower().strip().capitalize()

    # If sentence is not empty
    if edited_sentence:
        # Get the last word of current sentence
        final_word = (edited_sentence.strip().split())[-1]
        # Add last word to final_word list
        final_sentence.append(final_word)
        # Add 'period' at the end of sentence
        edited_sentence += "."
        # Replace 'iz' with 'is' in the sentence
        edited_sentence = re.sub(subsitute_char, "is", edited_sentence)
        # Print processed sentence
        print(edited_sentence)

# Print list of last words from each sentences
print(f"List of last words:\n {final_sentence}")
