import os
import re
os.system('cls')

def get_word_before_after(string, target_word):
    string_without_commas = string.replace(",", "") # remove all commas
    words = string_without_commas.split()  # Split the string into a list of words
    word_after = ""

    # if the word "before" exists in this line
    try:
        index = words.index(target_word)  # Get the index of the target word
    except :
        return None, None
    
    # Retrieve the word before the target word (if available)
    if index > 0:
        word_before = words[index - 1]
    else:
        word_before = None
  
    # get all the words after index
    if index > 0:
        while index < len(words) - 1:
            index += 1
            word_after += words[index]

    return word_before, word_after


counter = 0 # the counter for the while loop
target = "before" # the target word for the while loop\
array = [] # the array of the order of things

f = open("Data for Project\\Course Sequencing Rules.csv", "r")
data = f.read().splitlines()

while counter < len(data):
    my_string = data[counter]
    counter += 1
    before, after = get_word_before_after(my_string, target)
    if before != None and after != None:
        after = after.replace('"', "") # deletes all "s
        array.append(before + after)

'''for i in array:
    print(i)'''

def split_string(string, chunk_size):
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

array_asso = {}
arr = []
for i in range(len(array)):
    arr = split_string(array[i], 10)

    if array_asso.get(arr[0]) is not None:
        counter1 = 1
        while counter1 < len(arr):
            array_asso[arr[0]].append(arr[counter1])
            counter1 += 1
    else:
        array_asso[arr[0]] = arr[1:]

print(array_asso)