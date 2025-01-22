"""
 Refactor homeworks from module 2 and 3 using functional approach with decomposition.
"""

# Refactoring homework 2
# https://github.com/Sharovic/Study_Python_for_Data_Quality/blob/main/Tasks/02_homework.py

import random
from string import ascii_letters


def generate_random_dictionary():
    """Generate a dictionary with random keys (letters) and values (0 - 100)."""
    dictionary_length = random.randint(2, 10)
    return {
        random.choice(ascii_letters): random.randint(0, 100)
        for _ in range(dictionary_length)
    }


def create_list_of_dicts():
    """Create a list of a random number of dictionaries (from 2 to 10)."""
    return [generate_random_dictionary() for _ in range(random.randint(2, 10))]


def consolidate_dic(origin_list):
    """Consolidate all dictionaries into a single dictionary with keys and all existed values."""
    consolidate_dic = {}
    for index_in_origin_list, element_dic in enumerate(origin_list):
        for key, value in element_dic.items():
            if key in consolidate_dic:
                consolidate_dic[key].append([index_in_origin_list, value])
            else:
                consolidate_dic[key] = [[index_in_origin_list, value]]
    return consolidate_dic


def create_common_dic(consolidate_dic):
    common_dic = {}
    for k, v in consolidate_dic.items():
        if len(v) == 1:  # Key appears only once
            common_dic[k] = v[0][0]  # Store the index of the dictionary
        else:  # Key appears multiple times
            max_value = max(
                consolidate_dic[k], key=lambda value: value[1]
            )  # Find max by value
            new_name = (
                k + "_" + str(max_value[0])
            )  # Modify key to include the index of dictionary in origin_list
            common_dic[new_name] = max_value[1]  # Store the maximum value
    return common_dic


# Execution
origin_list = create_list_of_dicts()  # Generate the list of random dictionaries
consolidate_dic = consolidate_dic(origin_list)  # Consolidate the dictionaries
common_dic = create_common_dic(consolidate_dic)  # Create the final dictionary

# Output the results
print("Original list of dicts:")
print(origin_list)
print("\nConsolidated dictionary:")
print(consolidate_dic)
print("\nFinal common dictionary:")
print(common_dic)
