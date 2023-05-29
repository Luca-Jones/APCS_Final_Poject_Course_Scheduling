import json
import os
import pandas as pd
import csv
import sys
os.system("cls")
print(sys.path)
time_table = {}



filename = 'Data for Project\\Schedule 2022.csv'

# Read the CSV file using pandas
dataframe = pd.read_csv(filename)
print(dataframe)

semester1 = {}
semester2 = {}

i = 0

# Iterate over each column
for col in dataframe.columns:
    # Access the values in the column
    #values = dataframe[col].tolist()
    #print(f'{col}: {values}')
    if i > 4:
        break
    semester1[dataframe[col][0]] = dataframe[col].tolist()[1:]
    i = i + 1

i = 0

for col in dataframe.columns:
    if i > 4:
        semester2[dataframe[col][0]] = dataframe[col].tolist()[1:]
    i = i + 1

time_table["Semester 1"] = semester1
time_table["Semester 2"] = semester2

with open('Shedule2022.json', 'w') as file:
    json.dump(time_table, file)