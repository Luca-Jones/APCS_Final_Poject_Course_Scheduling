import os
import csv
os.system('cls')

def cleanData(row):
    counter = 0 # the counter

    if row[-1] != "Y":
        return None

    # remove all commas
    while counter < len(row):
        if row[counter] == ",":
            row.remove(counter)
            counter -= 1
        counter += 1

    #remove all
    updated_array = [x for x in row if x != ""]

    #print(updated_array)
    if updated_array[6] == "0":
        return None
    
    indexes_to_remove = [2, 3, 5, 8, 10]  # Example indexes to remove
    updated_array2 = [updated_array[i] for i in range(len(updated_array)) if i not in indexes_to_remove]
    return updated_array2

# Initialize an empty array or 2D array
data = []

# Open the CSV file
with open('Data for Project\\Course Information.csv', 'r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)

    # Iterate over each row in the CSV file
    for row in csv_reader:
        # Append the row to the data array or 2D array
        temp = cleanData(row)
        if temp != None:
            data.append(temp)

'''for i in range(len(data)):
    print(data[i])'''

def array_to_dictionary(array):
    dictionary = {}
    for item in array:
        key = item[0]
        values = item[1:]
        dictionary[key] = values
    return dictionary

# the dictionary
my_dict = array_to_dictionary(data)

# print the dictionary
for key, values in my_dict.items():
    print(key, values)