from rich.console import Console
from rich.table import Table

import os
os.system("cls")

class Course:
    currentClasses = 0
    sections = {}
    
    def __init__(self, name, class_size, is_outside_timetable, sequencing, number_of_classes_per_year, is_linear):
        
        self._name = name
        self.number_of_classes_per_year = number_of_classes_per_year
        self._class_size = class_size
        self.is_linear = is_linear
        self._is_outside_timetable  = is_outside_timetable
        self.sequencing = sequencing
        

  
    def __str__(self):
        return "\n" + str(self._name) + "\nis outside  " + str(self._is_outside_timetable ) + "\nis linear  " + str(self.is_linear) + "\nnumber of classes  " + str(self.number_of_classes_per_year ) +" \nclass size  " + str(self._class_size )  +"\nSequencing  " + str(self.sequencing ) + "\n\n"
    
    def __repr__(self):
        return self.__str__()
    

class Class(Course):
    def __init__(self, name, class_size, is_outside_timetable, sequencing, blocking, semester):
        super().__init__(self, name, class_size, is_outside_timetable, sequencing, blocking)
        self.semester = semester
        self.students = []
    def __str__(self):
        return str(self._name) + " in Semester " + self.semester + " Block " + self.block + "\n"
    def __repr__(self):
        return self.__str__()


class Student:
    def __init__(self, id, course_requests, alternates):
        self._id = id
        self._course_requets = course_requests
        self._alternates = alternates
        self.student_classes = []
    def __str__ (self):
        return str("\n\nid = " + str(self._id) + "Requests = " + str(self._course_requets) + " \nAlternates = " + str(self._alternates))
    def __repr__(self):
        return self.__str__()
    
    
 


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


count = 0
alt = 0
idArr = []
studentArr = [[0 for i in range(23)] for j in range(23)] #temporaty array which contains all student requests
test = [] #array used to store data read from file
studentlist = [[] for j in range(23)] #cleaned student requests are stored here before they are used to make a student object
altlist = [[] for j in range(23)] #temporaty array which contains all alternate requests
alternate = [[0 for i in range(23)] for j in range(23)]#cleaned alternate requests are stored here before they are used to make a student object
courselist = [] #array containing all course objects
student = [] #final list containing studen objects with their courses, altenates and id number
outside_the_timetable = [
    'XC---09--L', 'MDNC-09C-L', 'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L', 'YCPA-0AX-L',
    'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'YCPA-0AXE-', 'MMUOR10S-L', 'MDNC-10--L',
    'MIDS-0C---', 'MMUJB10--L', 'MDNC-11--L', 'YCPA-1AX-L', 'MDNCM11--L', 'YCPA-1AXE-',
    'MGRPR11--L', 'MGMT-12L--', 'YED--1EX-L', 'MWEX-2A--L', 'MCMCC11--L', 'MWEX-2B--L',
    'MIMJB11--L', 'MMUOR11S-L', 'MDNC-12--L', 'YCPA-2AX-L', 'MDNCM12--L', 'YCPA-2AXE-',
    'MGRPR12--L', 'MGMT-12L--', 'YED--2DX-L', 'YED--2FX-L', 'MCMCC12--L', 'MWEX-2A--L',
    'MIMJB12--L', 'MWEX-2B--L', 'MMUOR12S-'
] #hardcoded array with all outside the timetable classes






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
                    courselist.append(Course(test[0],test[9] ,out, array_asso[test[0]],test[14], linear))
                else:
                     courselist.append(Course(test[0],test[9] ,out, "",test[14], linear))
      
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()

#for loops that take the student requests and alternate requests from the remporary arrays they are stored in 
#and creats a list with student objects with their alternate requests, course requests and id number
for i in range(23):
    for j in range(23):
      
      if studentArr[i][j] != 0:
        studentlist[i].append(studentArr[i][j])
      if alternate[i][j] != 0:
        altlist[i].append(alternate[i][j])
    if j == 22:
       student.append(Student(idArr[i],studentlist[i],altlist[i]))  
    
alpha = ["A", "B", "C", "D", "A", "B", "C", "D"]    
master = {"Semester 1": {"A": [], "B": [], "C": [], "D":[]}, "Semester 2": {"A": [], "B": [], "C": [], "D":[]}}


for course in courselist:

    for i in range(len(student)):
        for j in range (min(len(student[i]._course_requets), 8)):#len(student[i]._course_requets
            if (course._name == student[i]._course_requets[j]):
                if(alpha[j] in course.sections):
                    
                        course.sections[alpha[j]].append(student[i]._id)

                        
                else:
                    arrrrrr = []
                    arrrrrr.append(student[i]._id)
                    course.sections[alpha[j]] = arrrrrr
                    if(j < 4):
                        master["Semester 1"][alpha[j]].append(course._name)
                    
                    else:
                        master["Semester 2"][alpha[j]].append(course._name)
                        

print (master)




      
    
