import os
os.system('cls')



def get_word_before_after(string, target_word):
    words = string.split()  # Split the string into a list of words
    #print(words)
    try:
        index = words.index(target_word)  # Get the index of the target word
    except :
        return None, None
    # Retrieve the word before the target word (if available)
    if index > 0:
        word_before = words[index - 1]
    else:
        word_before = None

    '''while index < len(words):
        index += 1
        word_after = words[index]
        if words[index + 1] != ",":
            word_after += words[index + 1]'''

    # Retrieve the word after the target word (if available)
    if index < len(words) - 1:
        word_after = words[index + 1]
        while 
    else:
        word_after = None

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
        array.append(before + " before " + after)

for i in array:
    print(i)