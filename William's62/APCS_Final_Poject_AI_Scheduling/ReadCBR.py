import os
os.system('cls')

# cleans the data
def get_data(string):
    try:
        index = string.index("in")
    except:
        return None
    
    # remove all commas and split the string into a list of words
    words = string[29:][:-13].replace(",", "").split()

    # words == None
    if not words:
        return None
    del words[-3:-1]
    return words

arrayCBR = []

with open("Data for Project\\Course Blocking Rules.csv", "r") as course_blocking_rules:
    data = course_blocking_rules.read().splitlines()

for my_string in data:
    blocking_rules = get_data(my_string)
    if blocking_rules:
        arrayCBR.append(blocking_rules)

for i in arrayCBR:
    print(i)
