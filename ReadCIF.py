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

print(data)

'''def split_string(string, chunk_size):
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

array_asso = {}
arr = []
for i in range(len(data)):
    arr = split_string(data[i], 10)

    # if this course already exist as a key in the array
    if array_asso.get(arr[0]) is not None:
        counter1 = 1 # counter for
        while counter1 < len(arr):
            array_asso[arr[0]].append(arr[counter1])
            counter1 += 1
    else:
        array_asso[arr[0]] = arr[1:]

print(array_asso)'''