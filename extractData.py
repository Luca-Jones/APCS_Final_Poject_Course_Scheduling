import os
os.system("cls")

class Course:
    def __init__(self, name, class_size, is_outside_timetable, sequencing, number_of_classes_per_year, is_linear):
        self._name = name
        self.number_of_classes_per_year = number_of_classes_per_year
        self._class_size = class_size
        self.is_linear = is_linear
        self._is_outside_timetable  = is_outside_timetable
        self.sequencing = sequencing
       
    def __str__(self):
        return "\n" + str(self._name) + " is outside  " + str(self._is_outside_timetable )
    
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
studentArr = [[0 for i in range(23)] for j in range(23)]
test = []
studentlist = [[] for j in range(23)]
altlist = [[] for j in range(23)]
alternate = [[0 for i in range(23)] for j in range(23)]
courselist = []
numStudents = []
numClasses = []
student = []
outside_the_timetable = [
    'XC---09--L', 'MDNC-09C-L', 'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L', 'YCPA-0AX-L',
    'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'YCPA-0AXE-', 'MMUOR10S-L', 'MDNC-10--L',
    'MIDS-0C---', 'MMUJB10--L', 'MDNC-11--L', 'YCPA-1AX-L', 'MDNCM11--L', 'YCPA-1AXE-',
    'MGRPR11--L', 'MGMT-12L--', 'YED--1EX-L', 'MWEX-2A--L', 'MCMCC11--L', 'MWEX-2B--L',
    'MIMJB11--L', 'MMUOR11S-L', 'MDNC-12--L', 'YCPA-2AX-L', 'MDNCM12--L', 'YCPA-2AXE-',
    'MGRPR12--L', 'MGMT-12L--', 'YED--2DX-L', 'YED--2FX-L', 'MCMCC12--L', 'MWEX-2A--L',
    'MIMJB12--L', 'MWEX-2B--L', 'MMUOR12S-'
]






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
       fi=open("pyp.txt","r")
       while True:
                linear = False
                out = False
                line=fi.readline()
                test = line.split(",", 16)
                if line=='':
                    break
               
                for i in range(len(outside_the_timetable)):
                    if outside_the_timetable[i] == test[0]:
                        out = True

                if test[7] == '1':
                    linear = True
                if  test[0] in array_asso.keys():
                    courselist.append(Course(test[0],test[9] ,out, array_asso[test[0]],test[14], linear))
                else:
                     courselist.append(Course(test[0],test[9] ,out, "",test[14], linear))
                

                     
              
except FileNotFoundError:
       print ("File is not found")
else:
       f.close()


for i in range(23):
    for j in range(23):
      
      if studentArr[i][j] != 0:
        studentlist[i].append(studentArr[i][j])
      if alternate[i][j] != 0:
        altlist[i].append(alternate[i][j])
    if j == 22:
       student.append(Student(idArr[i],studentlist[i],altlist[i]))  
print(courselist)
print(student)
      
    
