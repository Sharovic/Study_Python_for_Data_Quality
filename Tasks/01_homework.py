"""
Create a python script:
 1. create list of 100 random numbers from 0 to 1000
 2. sort list from min to max (without using sort())
 3. calculate average for even and odd numbers
 4. print both average result in console
 5. Each line of code should be commented with description.
Commit script to git repository and provide link as home task result.
"""

# import necessary modules
from random import randint

# create empty list
l = []

# filling List with random numbers
for i in range(100):
    l.append(randint(1, 1000))
# display unsorted list
print("List with random elements:", l)

# sort list from min to max using bubble sort
for i in range(100):  # Outer loop for passes through the whole list
    for j in range(0, 99 - i):  # Inner loop for comparing neighbor element
        # if current element is greater than next - swap them
        if l[j] > l[j + 1]:
            l[j], l[j + 1] = l[j + 1], l[j]
# display sorted list
print("Sorted list: ", l)

# initialize variables for counting and summing even and odd numbers
even_counter, even_sum, odd_counter, odd_sum = 0, 0, 0, 0

# find and calculate average for even and odd elements (zero - is even number)
# process each element in the list
for i in l:
    # check if element is even (divisible by 2 without remainder)
    if i % 2 == 0:
        even_counter += 1  # increment even numbers counter
        even_sum += i  # add number to sum of even numbers
    else:
        odd_counter += 1  # increment odd numbers counter
        odd_sum += i  # add number to sum of odd numbers

# try to calculate average of even elements, handle division by zero
try:
    even_average = even_sum / even_counter
except ZeroDivisionError:
    print("Even numbers don't exist on list")

# try to calculate average of odd elements, handle division by zero
try:
    odd_average = odd_sum / odd_counter
except ZeroDivisionError:
    print("Odd numbers don't exist on list")

# display the averages of even and odd elements
print("Average even numbers: ", even_average)
print("Average odd numbers: ", odd_average)
