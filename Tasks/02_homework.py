""""
Write a code, which will:

1. create a list of random number of dicts (from 2 to 10)
    - dict's random numbers of keys should be letter,
    - dict's values should be a number (0-100),
        example: [{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]

2. get previously generated list of dicts and create one common dict:
    - if dicts have same key, we will take max value, and rename key with dict number with max value
    - if key is only in one dict - take it as is,
        example: {'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}
        Each line of code should be commented with description.

3. Commit script to git repository and provide link as home task result.
"""

import random

# from pprint import pprint
from string import ascii_letters

# Create a list with random number of dicts (from 2 to 10)
list_length = random.randint(2, 10)
origin_list = [{} for i in range(list_length)]

# Populate each dictionary in the list with random key-value pairs.
# Keys are random letters, and values are random number (0 - 100)
for element_dic in origin_list:
    dictionary_length = random.randint(
        0, 20
    )  # Random number of elements in each dictionary
    for j in range(dictionary_length):
        k = random.choice(ascii_letters)  # Random letters as a key
        v = random.randint(0, 100)  # Random integer as a value
        element_dic[k] = v

# Create a consolidated dictionary where:
# - If the key exists, it stores a list of [index of dictionary in origin_list, value]
# - If the key is new, it initializes with the [index of dictionary in origin_list, value].
consolidated_dic = {}

for index_in_origin_list, element_dic in enumerate(origin_list):
    for key, value in element_dic.items():
        if key in consolidated_dic:
            consolidated_dic[key].append([index_in_origin_list, value])
        else:
            consolidated_dic[key] = [[index_in_origin_list, value]]


# Create a final dictionary where:
# - If a key appears only once, store its key and index directly.
# - If a key appears multiple times, find the maximum value and add the key
#   with a modified name (key_index) and the maximum value.
common_dic = {}
for k, v in consolidated_dic.items():
    if len(v) == 1:  # Key appears only once
        common_dic[k] = v[0][0]  # Store the index of the dictionary
    else:  # Key appears multiple times
        max_value = max(
            consolidated_dic[k], key=lambda value: value[1]
        )  # Find max by value
        new_name = (
            k + "_" + str(max_value[0])
        )  # Modify key to include the index of dictionary in origin_list
        common_dic[new_name] = max_value[1]  # Store the maximum value
        # print(max_value)

# print(origin_list)  # Uncomment to inspect the original_list of dictionaries
# print(consolidated_dic)  # Uncomment to inspect the consolidated dictionary
print(common_dic)  # Print the final result

"""
https://github.com/Sharovic/Study_Python_for_Data_Quality/blob/main/Tasks/02_homework.py
"""
