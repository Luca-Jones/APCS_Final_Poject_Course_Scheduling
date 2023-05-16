from rich.console import Console
from rich.table import Table
import os
os.system("cls")



class Course:
    def __init__(self, name, class_size, is_outside_timetable, sequencing, blocking, number_of_classes_per_year):
        self._name = name
        self.number_of_classes_per_year = number_of_classes_per_year
        self._class_size = class_size
        self._is_outside_timetable  = is_outside_timetable
        self.sequencing = sequencing
        self.blocking = blocking
    def __str__(self):
        return str(self._name) + "\n"

class Class(Course):
    def __init__(self, name, class_size, is_outside_timetable, sequencing, blocking, semester, block):
        super().__init__(self, name, class_size, is_outside_timetable, sequencing, blocking)
        self.semester = semester
        self.block = block
        self.students = []
    def __str__(self):
        return str(self._name) + " in Semester " + self.semester + " Block " + self.block + "\n"

class Student:
    def __init__(self, id, course_requests, alternates):
        self._id = id
        self._course_requets = course_requests
        self._alternates = alternates
        self.student_classes = []
    def __str__ (self):
        return str("id = " + str(self._id) + " \nRequests = " + str(self._course_requets) + " \nAlternates = " + str(self._alternates))

class Timetable:
    def __init__(self):
        self.block_1A = []
        self.block_1B = []
        self.block_1C = []
        self.block_1D = []
        self.block_2A = []
        self.block_2B = []
        self.block_2C = []
        self.block_2D = []
    def __str__(self):
        # makes a nice styled table
        table = Table(title="TimeTable")
        rows = [self.block_1A, self.block_1B, self.block_1C, self.block_1D, self.block_2A, self.block_2B, self.block_2C, self.block_2D]
        columns = ["S1 Block A", "S1 Block B", "S1 Block C", "S1 Block D","S2 Block A", "S2 Block B", "S2 Block C", "S2 Block D"]
        for column in columns:
            table.add_column(column)
        for row in rows:
            table.add_row(*row, style='bright_green')
        console = Console() 
        console.print(table)   
        return ""
    def add_class(self, class_slot, semester, block):
        if semester == 1:
            if block == "A":
                self.block_1A.append(class_slot)
            if block == "B":
                self.block_1B.append(class_slot)
            if block == "C":
                self.block_1C.append(class_slot)
            if block == "D":
                self.block_1D.append(class_slot)
        else:
            if block == "A":
                self.block_2A.append(class_slot)
            if block == "B":
                self.block_2B.append(class_slot)
            if block == "C":
                self.block_2C.append(class_slot)
            if block == "D":
                self.block_2D.append(class_slot)

tt = Timetable()
print(tt)


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

for i in array:
    print(i)


count = 0
alt = 0
idArr = []
studentArr = [[0 for i in range(838)] for j in range(838)]
test = []
studentlist = [[] for j in range(838)]
altlist = [[] for j in range(838)]
alternate = [[0 for i in range(838)] for j in range(838)]
courselist = []
numStudents = []
numClasses = []

try:
       f=open("python.txt","r")
       while True:
                count = count + 1
                line=f.readline()
                test = line.split(",", 16)
                if line=='':
                    break
                
                if test[0] == 'ID':
                    count = 0
                    alt = 0
                    for i in range(len(test)):
                        if test[i] == 'ID':    
                            test[i] = test[i+1]
                            test[i+1] == ""
                            idArr.append(test[i])
                elif test[0] != 'Course':
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
       fi=open("py.txt","r")
       while True:
                
                line=fi.readline()
                test = line.split(",", 16)
                if line=='':
                    break
                courselist.append(test[0])
                c = Course(test[0], test[9], False, "", "", test[14])
                numStudents.append(test[9])
                numClasses.append(test[14])
                
           
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()

print (numClasses)
for i in range(23):
    for j in range(23):
      if j == 0:
           print(idArr[i])
      if studentArr[i][j] != 0:
        studentlist[i].append(studentArr[i][j])
      if alternate[i][j] != 0:
        altlist[i].append(alternate[i][j])
      
    if i == 22:
        print(studentlist)
        print(" ")
        print(" ")
        print(" ")
        print(altlist)
