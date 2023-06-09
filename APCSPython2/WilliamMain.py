from rich.console import Console
from rich.table import Table
import json
import csv
import math

import os
os.system("cls")


outside_the_timetable = [
    'XC---09--L', 'MDNC-09C-L', 'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L', 'YCPA-0AX-L',
    'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'YCPA-0AXE-', 'MMUOR10S-L', 'MDNC-10--L',
    'MIDS-0C---', 'MMUJB10--L', 'MDNC-11--L', 'YCPA-1AX-L', 'MDNCM11--L', 'YCPA-1AXE-',
    'MGRPR11--L', 'MGMT-12L--', 'YED--1EX-L', 'MWEX-2A--L', 'MCMCC11--L', 'MWEX-2B--L',
    'MIMJB11--L', 'MMUOR11S-L', 'MDNC-12--L', 'YCPA-2AX-L', 'MDNCM12--L', 'YCPA-2AXE-',
    'MGRPR12--L', 'MGMT-12L--', 'YED--2DX-L', 'YED--2FX-L', 'MCMCC12--L', 'MWEX-2A--L',
    'MIMJB12--L', 'MWEX-2B--L', 'MMUOR12S-L', 'MCLC-12---'
] #hardcoded array with all outside the timetable classes

bad_courses = ['XLEAD09---', 'MGE--11', 'MGE--12', 'MKOR-10---', 'MKOR-11---', 
               'MKOR-12---', 'MIT--12---', 'MSPLG11---', 'MJA--10---', 
               'MJA--11---', 'MJA--12---', 'MLTST10---', 'MLTST10--L']



# classes
class Course:

    def __init__(self, name, class_size, is_outside_timetable, sequencing, number_of_classes_per_year, is_linear, description):
        self._name = name
        self.number_of_classes_per_year = number_of_classes_per_year
        self._class_size = class_size
        self.is_linear = is_linear
        self._is_outside_timetable  = is_outside_timetable
        self.sequencing = sequencing
        self._sections = {}
        self._currentClasses = 0
        self._description = description         # includes courses blocked with it
        self._temp_description = description    # holds the unique description
        self._sim_blocking = []                 # simultaneous blocking rules
        self._terms_blocking = []
        

  
    def __str__(self):
        return str(self._name)
    
    def __repr__(self):
        return self.__str__()


class Student:
    def __init__(self, id, course_requests, alternates):
        self._id = id
        self._course_requests = course_requests
        self._course_requestsCopy = course_requests # a copy of their original course requests
        self._alternates = alternates
        self.student_classes = {}
        self._cr = course_requests

    def __str__ (self):
        return str("\n\nid = " + str(self._id) + " \nRequests = " + str(self._course_requests) + " \nAlternates = " + str(self._alternates) + "\nCourses: " + str(self.student_classes))
    def __repr__(self):
        return self.__str__()


# ReadCBR
##################################################################
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

# ReadCIF
##################################################################
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

def array_to_dictionary(array):
    dictionary = {}
    for item in array:
        key = item[0]
        values = item[1:]
        dictionary[key] = values
    return dictionary

# the dictionary
my_dict = array_to_dictionary(data)

'''# print the dictionary
for key, values in my_dict.items():
    print(key, values)'''


# ReadCSR
##################################################################
def get_word_before_after(string, target_word):
    
    # remove all commas and split the string into a list of words
    words = string.replace(",", "").split() 
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

os.system('cls')
counter = 0 # the counter for the while loop
target = "before" # the target word for the while loop\
array = [] # the array of the order of things

f = open("Data for Project\\Course Sequencing Rules.csv", "r") # opens the file
data = f.read().splitlines() # stores the file as an string array with each line as an element 

while counter < len(data):
    my_string = data[counter]
    counter += 1
    before, after = get_word_before_after(my_string, target)
    if before != None and after != None:
        after = after.replace('"', "") # deletes all "
        array.append(before + after)

def split_string(string, chunk_size):
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

array_asso = {}
arr = []
for i in range(len(array)):
    arr = split_string(array[i], 10)

    # if this course already exist as a key in the array
    if array_asso.get(arr[0]) is not None:
        counter1 = 1 # counter for
        while counter1 < len(arr):
            array_asso[arr[0]].append(arr[counter1])
            counter1 += 1
    else:
        array_asso[arr[0]] = arr[1:]

# start of algorithem 
count = 0
alt = 0
idArr = []
studentArr = [[0 for i in range(838)] for j in range(838)] #temporaty array which contains all student requests
test = [] #array used to store data read from file
studentlist = [[] for j in range(838)] #cleaned student requests are stored here before they are used to make a student object
altlist = [[] for j in range(838)] #temporaty array which contains all alternate requests
alternate = [[0 for i in range(838)] for j in range(838)]#cleaned alternate requests are stored here before they are used to make a student object
courselist = [] #array containing all course objects
student = [] #final list containing studen objects with their courses, altenates and id number

# find the course object with a specific course CODE
def get_course(name_of_course):
    for c in courselist:
        if c._name == name_of_course:
            return c
    return "not found"

try:
       f=open("python.txt","r")
       while True:
                #reads line of file, stores it into test array, then adds one to count which is the line number
                count = count + 1
                line=f.readline()
                test = line.split(",", 16)

                if line=='':
                    break
                
                #if the first word in test is id then that means it is a new students requests
                #so the line number becomes 0 and the amount of alternates also becomes 0
                if test[0] == 'ID':
                    count = 0
                    alt = 0
                    
                    #stores the id number of the new student in idArr
                    for i in range(len(test)):
                        if test[i] == 'ID':    
                            test[i] = test[i+1]
                            test[i+1] == ""
                            idArr.append(test[i])

                    #sees if this is a course request or not
                elif test[0] != 'Course':

                    #if it is an alternate add it to the alternate list
                    #otherwise add it to the student request list
                    if test[11] == 'Y':
                        count = count - 1
                        alternate[len(idArr) -1][alt] = test[0]
                        alt = alt + 1
                    else:    
                        studentArr[len(idArr) -1][count -1] = test[0]        
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()

try:
       fi=open("pyp.txt","r")
       while True:
                #sets linear and out(short for outside the timetable) to false
                linear = False
                out = False
                line=fi.readline()
                test = line.split(",", 16)
                if line=='':
                    break
               
               #if the course read in the file is an outside the timetable course set out to true
                for i in range(len(outside_the_timetable)):
                    if outside_the_timetable[i] == test[0]:
                        out = True

                #if the course is a linear course the base term will be set to 1 thus if the base term is 1
                #set linear to true
                if test[7] == '1':
                    linear = True

                #if the course is part of course sequencing, create a course object with 
                #the name of the course, the amount of students, if its outside the timetable, course sequencing, amount of times it runs and if its linear
                #if not do the same but without course sequencing
                if  test[0] in array_asso.keys():
                    courselist.append(Course(test[0],test[9] ,out, array_asso[test[0]],test[14], linear, test[2]))
                else:
                     courselist.append(Course(test[0],test[9] ,out, "",test[14], linear, test[2]))
      
except FileNotFoundError:
       print ("File is not found")
else:
       fi.close()

#for loops that take the student requests and alternate requests from the remporary arrays they are stored in 
#and creats a list with student objects with their alternate requests, course requests and id number
for i in range(len(idArr) - 1):
    for j in range(838):
      if studentArr[i][j] != 0 and studentArr[i][j] not in bad_courses:
        studentlist[i].append(studentArr[i][j])
      if alternate[i][j] != 0:
        altlist[i].append(alternate[i][j])
    if j == 837:
        student.append(Student(idArr[i][0:4],studentlist[i],altlist[i])) 
'''print("student")
print(student)'''

#add all the courses in a list
arrayOfCourses = []
for course in courselist:
    arrayOfCourses.append(course._name)

#dictionary of the courses and it's class number
my_dict222 = {key: 0 for key in arrayOfCourses}

# get the number of requests for each course
for stu in student:
    for stuElement in stu._course_requests:
        if stuElement in my_dict222:
            my_dict222[stuElement] += 1

# remove all courses with 0 requests
my_dict222 = {key: value for key, value in my_dict222.items() if value != 0}

# calculate the number of classes for each course
for value in my_dict222:
    for obj in courselist:
        if obj._name == value:
            if int(obj._class_size) != 0:
                my_dict222[value] = my_dict222[value]/int(obj._class_size)

# the numberof classes for each course
md222_copy = my_dict222.copy()

for value in md222_copy:
    whole_number = int(md222_copy[value])
    deci_num = md222_copy[value] - whole_number
    # only make this class if more than 60% is filled
    if deci_num < 0.6:
        md222_copy[value] = whole_number
    else:
        md222_copy[value] = whole_number + 1

'''for value in my_dict222:
    print(value, my_dict222[value])'''

'''for value in md222_copy:
    print(value, md222_copy[value])'''

#print(courselist)

# if a course has 0 requests, remove it
filteredArrayCBR = []

for inner_array in arrayCBR:
    filtered_inner_array = []
    for element in inner_array:
        if element in md222_copy:
            filtered_inner_array.append(element)
    filtered_inner_array.append(inner_array[-1])
    if len(filtered_inner_array) > 2:
        filteredArrayCBR.append(filtered_inner_array)

for value in filteredArrayCBR:
    print(value)
'''for value in arrayCBR:
    if value[-1] == "Simultaneous":
        for courseValue in courselist:
            if courseValue._name == value[0]:
                for courseValue2 in courselist:
                    if courseValue2._name == value[1]:'''



#print(arrayCBR)


















'''alpha = ["S1 A", "S1 B", "S1 C", "S1 D", "S2 A", "S2 B", "S2 C", "S2 D", "Outside"]                                         # timtable headers / keys   
master = {"S1 A": [], "S1 B": [], "S1 C": [], "S1 D":[], "S2 A": [], "S2 B": [], "S2 C": [], "S2 D":[], "Outside":[]}       # master timetable

# main algorithmn
for student in student:
    student.student_classes.append'''























































'''def show(itemslist):
    out = ""
    for item in itemslist:
        out = out + item + "\n\n"
    return out

table = Table(title="TimeTable")
rows = list(master.values())
columns = alpha

for column in columns:
    table.add_column(column, no_wrap = False)
entries = []
for row in rows:
    entries.append(show(row))
table.add_row(*entries, style='bright_green')

console = Console() 
console.print(table)'''