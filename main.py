from rich.console import Console
from rich.table import Table
import random
import copy
import os
os.system("cls")

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
        return str(self._name) + ": " + str(len(self._sections)) + str(int(self.number_of_classes_per_year))
    
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
        self._course_requests = course_requests
        self._alternates = alternates
        self.student_classes = {}
        self._cr = course_requests
    def __str__ (self):
        return str("\n\nid = " + str(self._id) + " \nRequests = " + str(self._course_requests) + " \nAlternates = " + str(self._alternates) + "\nCourses: " + str(self.student_classes))
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
studentArr = [[0 for i in range(838)] for j in range(838)] #temporaty array which contains all student requests
test = [] #array used to store data read from file
studentlist = [[] for j in range(838)] #cleaned student requests are stored here before they are used to make a student object
altlist = [[] for j in range(838)] #temporaty array which contains all alternate requests
alternate = [[0 for i in range(838)] for j in range(838)]#cleaned alternate requests are stored here before they are used to make a student object
courselist = [] #array containing all course objects
student = [] #final list containing studen objects with their courses, altenates and id number
outside_the_timetable = [
    'XC---09--L', 'MDNC-09C-L', 'MDNC-09M-L', 'XBA--09J-L', 'XLDCB09S-L', 'YCPA-0AX-L',
    'MDNCM10--L', 'YED--0BX-L', 'MMUCC10--L', 'YCPA-0AXE-', 'MMUOR10S-L', 'MDNC-10--L',
    'MIDS-0C---', 'MMUJB10--L', 'MDNC-11--L', 'YCPA-1AX-L', 'MDNCM11--L', 'YCPA-1AXE-',
    'MGRPR11--L', 'MGMT-12L--', 'YED--1EX-L', 'MWEX-2A--L', 'MCMCC11--L', 'MWEX-2B--L',
    'MIMJB11--L', 'MMUOR11S-L', 'MDNC-12--L', 'YCPA-2AX-L', 'MDNCM12--L', 'YCPA-2AXE-',
    'MGRPR12--L', 'MGMT-12L--', 'YED--2DX-L', 'YED--2FX-L', 'MCMCC12--L', 'MWEX-2A--L',
    'MIMJB12--L', 'MWEX-2B--L', 'MMUOR12S-L', 'MCLC-12---'
] #hardcoded array with all outside the timetable classes

        
bad_courses = ['XLEAD09---',    'MGE--11',    'MGE--12', 'MKOR-10---',
                       'MKOR-11---', 'MKOR-12---', 'MIT--12---', 'MSPLG11---',
                       'MJA--10---', 'MJA--11---', 'MJA--12---',
                       
                       'MLTST10---', 'MLTST10--L']

# find the course object with a specific course CODE
def get_course(name_of_course, c_list):
    for c in c_list:
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
       




# gets data for blocking rules
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

    # if blocking_rules is a non-empty string array
    if blocking_rules:

        # look at simultaneous blocking
        if blocking_rules[-1] == "Simultaneous":
            
            collective_description = ""

            for blocked_course in blocking_rules:
                if not get_course(blocked_course, courselist) == "not found":
                    collective_description += get_course(blocked_course, courselist)._temp_description + " / "

            for blocked_course in blocking_rules:
                
                if not get_course(blocked_course, courselist) == "not found":
                    get_course(blocked_course,courselist)._description = collective_description
                    if blocking_rules[-1] == "Simultaneous":
                        get_course(blocked_course, courselist)._sim_blocking = blocking_rules

        elif blocking_rules[-1] == "Terms":

            for blocked_course in blocking_rules:
                
                if not get_course(blocked_course,courselist) == "not found":

                    get_course(blocked_course, courselist)._terms_blocking = blocking_rules


        arrayCBR.append(blocking_rules)




# SUCCESS METRICS

def score(set):
    total_score = 0
    total_requests = 0

    for s in set:
        
        total_requests += len(s._course_requests)

        # find overlap
        for c in s._course_requests:
            for block in list(s.student_classes.values()):
                if c in block:
                    total_score += 1
           

    return total_score / total_requests

def score_with_alternates(set):
    total_score = 0
    total_requests = 0

    for s in set:
        
        total_requests += len(s._course_requests) + len(s._alternates)

        # find overlap
        for c in s._course_requests:
            for block in list(s.student_classes.values()):
                if c in block:
                    total_score += 1
        
        # find overlap
        for c in s._alternates:
            for block in list(s.student_classes.values()):
                if c in block:
                    total_score += 1

    return total_score / total_requests

def has_eight_courses(stu):
    combined_list = []
    satisfied = 0

    for lst in list(stu.student_classes.values()):
        combined_list.extend(lst)

    for c in stu._course_requests:
        if c in combined_list and c not in outside_the_timetable:
            satisfied += 1
        
    return satisfied > 5

def students_with_eight_courses(set):
    score = 0

    for stu in set:
        if has_eight_courses(stu):
            score += 1

    return score / 838
        
def has_eight_courses_including_alternates(stu):
    combined_list = []
    satisfied = 0

    for lst in list(stu.student_classes.values()):
        combined_list.extend(lst)

    for c in stu._course_requests:
        if c in combined_list and c not in outside_the_timetable:
            satisfied += 1

    for c in stu._alternates:
        if c in combined_list and c not in outside_the_timetable:
            satisfied += 1
        
    return satisfied > 5

def students_with_eight_courses_including_alternates(set):
    counter = 0
    score = 0

    for stu in set:
        if has_eight_courses_including_alternates(stu):
            if counter < 3:
                #print(stu)
                counter += 1
            score += 1
    #print("\n")
    return score / 838
 







    
alpha = ["S1 A", "S1 B", "S1 C", "S1 D", "S2 A", "S2 B", "S2 C", "S2 D", "Outside"]
best_master = {"S1 A": [], "S1 B": [], "S1 C": [], "S1 D":[], "S2 A": [], "S2 B": [], "S2 C": [], "S2 D":[], "Outside":[]}
best_student = copy.deepcopy(student)

# OPTIMIZATION LOOP

for iteration in range(10):
    print(iteration)
    temp_courselist = copy.deepcopy(courselist)
    
    # timtable headers / keys   
    master = {"S1 A": [], "S1 B": [], "S1 C": [], "S1 D":[], "S2 A": [], "S2 B": [], "S2 C": [], "S2 D":[], "Outside":[]}       # master timetable

    # make a random course order
    for course in temp_courselist:
        popped = temp_courselist.pop(temp_courselist.index(course))
        temp_courselist.insert(random.randrange(0,len(courselist)), popped)

        





    # course sorting

    # linear courses inside the time table
    for course in temp_courselist:
        if course.is_linear:
            popped = temp_courselist.pop(temp_courselist.index(course))
            temp_courselist.insert(0, popped)


    # terms blocked courses come before outside
    for course in temp_courselist:
        if course._terms_blocking:
            popped = temp_courselist.pop(temp_courselist.index(course))
            temp_courselist.insert(0, popped)

    # otside comes first
    for course in temp_courselist:
        if course._name in outside_the_timetable:
            popped = temp_courselist.pop(temp_courselist.index(course))
            temp_courselist.insert(0, popped)


    p = ""
    thing = []

    def get_sequencing(name_of_course):
        for c in temp_courselist:
            if name_of_course == c._name:
                return list(c.sequencing)
        return []

    # returns true if student[i] has a linear course that needs to be paired
    def has_a_linear_course(i):
        for block in student[i].student_classes:
            if len(student[i].student_classes[block]) == 1 and get_course(student[i].student_classes[block][0], temp_courselist).is_linear and student[i].student_classes[block][0] not in outside_the_timetable:
                return block
        return False


    # places student[i] in course somewhere from alpha[start] to alpha[end]
    def place(start, end, i, course):

        # look through every available block
        for k in range(start, end + 1, 1):

            # if the slot is outside the time table or not yet taken up
            if k == 8 or (alpha[k] not in student[i].student_classes and not course.is_linear):

                # if the course is offered during this block and the class is not full
                if alpha[k] in course._sections and len(course._sections[alpha[k]]) < int(course._class_size):

                
                    course._sections[alpha[k]].append(student[i]._id)
                    
                    for sim_blk in course._sim_blocking:
                        if not sim_blk == "Simultaneous" and not sim_blk == course._name:
                            if student[i]._id not in get_course(sim_blk, temp_courselist)._sections[alpha[k]]:
                                get_course(sim_blk, temp_courselist)._sections[alpha[k]].append(student[i]._id)

                    student[i].student_classes[alpha[k]] = [course._name]

                    return True

                # if the course is not yet offered in this block and a new class can be made
                elif len(course._sections) < int(course.number_of_classes_per_year) and alpha[k] not in course._sections:

                    course._sections[alpha[k]] = [student[i]._id]
                    
                    for sim_blk in course._sim_blocking:
                        if not sim_blk == "Simultaneous" and not sim_blk == course._name:
                            get_course(sim_blk, temp_courselist)._sections[alpha[k]] = [student[i]._id]

                    student[i].student_classes[alpha[k]] = [course._name]
                    master[alpha[k]].append(course._description)

                    return True

            # if course is linear and inside the time table (second half implied)
            elif course.is_linear:
                
                # if student time table already has a linear course
                block = has_a_linear_course(i)
                if block:

                    # if the class exists in this block already and has space
                    if block in course._sections and len(course._sections[block]) < int(course._class_size):
                        
                        # add the student to the class and the sim blocking
                        course._sections[block].append(student[i]._id)

                        for sim_blk in course._sim_blocking:
                            if not sim_blk == "Simultaneous" and not sim_blk == course._name:
                                get_course(sim_blk, temp_courselist)._sections[block].append(student[i]._id)

                        # give the student the class combined with the other linear course
                        
                        student[i].student_classes[block].append(course._name)
                        student[i].student_classes[alpha[(alpha.index(block) + 4) % 8]].append(course._name)


                    # if a new course can be made
                    elif len(course._sections) < int(course.number_of_classes_per_year) and alpha[k] not in course._sections:

                        # create a new class with the student in it and for sim blocking
                        course._sections[block] = [student[i]._id]

                        for sim_blk in course._sim_blocking:
                            if not sim_blk == "Simultaneous" and not sim_blk == course._name:
                                get_course(sim_blk, temp_courselist)._sections[block] = [student[i]._id]


                        # give the student this class with the other linear class
                        student[i].student_classes[block].append(course._name)
                        student[i].student_classes[alpha[(alpha.index(block) + 4) % 8]].append(course._name)

                        # add the class to the master time table
                        master[block].append(course._description)
                        master[alpha[(alpha.index(block) + 4) % 8]].append(course._description)

                    # go to next student
                    return True
                

                # block not taken yet?
                elif alpha[k] not in student[i].student_classes and alpha[(k + 4) % 8] not in student[i].student_classes:
                
                    # if the class exists in this block already and has space
                    if alpha[k] in course._sections and len(course._sections[alpha[k]]) < int(course._class_size):
                        
                        # add student to the course and all its sim blocking
                        course._sections[alpha[k]].append(student[i]._id)

                        for sim_blk in course._sim_blocking:
                            if not sim_blk == "Simultaneous" and not sim_blk == course._name:
                                get_course(sim_blk, temp_courselist)._sections[alpha[k]].append(student[i]._id)

                        # give the student the course
                        student[i].student_classes[alpha[k]] = [course._name]
                        student[i].student_classes[alpha[(k + 4) % 8]] = [course._name]
                        
                        return True

                    # if a new course can be made
                    elif len(course._sections) < int(course.number_of_classes_per_year) and alpha[k] not in course._sections:
                        
                        # create a new class with the student in it and for sim blocking
                        course._sections[alpha[k]] = [student[i]._id]

                        for sim_blk in course._sim_blocking:
                            if not sim_blk == "Simultaneous" and not sim_blk == course._name:
                                get_course(sim_blk, temp_courselist)._sections[alpha[k]] = [student[i]._id]

                        # give the student this class
                        student[i].student_classes[alpha[k]] = [course._name]
                        student[i].student_classes[alpha[(k + 4) % 8]] = [course._name]

                        # add the class to the master time table
                        master[alpha[k]].append(course._description)
                        master[alpha[(k + 4) % 8]].append(course._description)

                        return True



        return False

    def is_prerequisite(c, i):
        for seq in c.sequencing:
            if seq in student[i]._course_requests:
                return True
        return False

    def has_prerequisite(c, i):
        for pre in temp_courselist:
            if c._name in pre.sequencing:
                for block in student[i].student_classes.values():
                    if pre._name in block:
                        return True
        return False        



    '''

                Main Algorithm

    '''

    # look through all courses
    for course in temp_courselist:
        
        # look through all students
        for i in range(len(student)):
            
            #look through their requests
            for j in range (len(student[i]._course_requests)):
                
                if (course._name == student[i]._course_requests[j]):
                    
                    if course._terms_blocking:
                        
                        if course._terms_blocking[0] == course._name:
                        
                            place(0, 3, i, course)
                            place(4, 7, i, get_course(course._terms_blocking[1], temp_courselist))
                        
                        break

                    if course._name in outside_the_timetable:
                        if place(8, 8, i, course):
                            break


                    if is_prerequisite(course, i):
                        if place(0, 3, i, course):
                        
                            break
                    
                    if has_prerequisite(course, i):
                        if place(4, 7, i, course):
                            
                            break

                    if place(0, 7, i, course):

                        break

                    break          

    def copy_terms(course, course_copy):
        
        # add class to the right blocking in the master timetable
        for j in range(4):
            if alpha[j] in course._sections:
                master[alpha[j + 4]] = list(map(lambda x: x.replace(course._description, course_copy._description), master[alpha[j+4]]))


        #master[alpha[k]].append(course_copy._description)

        # add students to the right blocks

        pass

    # tems blocking copying
    for course in temp_courselist:
        if course._terms_blocking:
            if course._terms_blocking[1] == course._name:
                copy_terms(get_course(course._terms_blocking[1], temp_courselist) , course)
                            


    # alternates

    # for all students
    for i in range(len(student)):

        # for their alternates
        for alt in student[i]._alternates:
            
            # check if course exists (some students are asking for courses MD doesn't have)
            if (get_course(alt, temp_courselist) == "not found"):
                continue
                    
            # for all blocks
            for k in range(8):

                # is taken?
                if alpha[k] not in student[i].student_classes:
                
                    # is the course offered during this block already?
                    if (alpha[k] in get_course(alt, temp_courselist)._sections):

                        # is full?
                        if(len(get_course(alt, temp_courselist)._sections[alpha[k]]) < int(get_course(alt, temp_courselist)._class_size)):
                            
                            # add to student schedule
                            student[i].student_classes[alpha[k]] = [get_course(alt, temp_courselist)._name]

                            # add to list of students in this class
                            get_course(alt, temp_courselist)._sections[alpha[k]].append(student[i]._id)

                            # break on success
                            break

                    # make a new class?
                    if(len(get_course(alt, temp_courselist)._sections) < int(get_course(alt, temp_courselist).number_of_classes_per_year)):

                        # make a new class and add the student to that class                    
                        arrrrrr = []
                        arrrrrr.append(student[i]._id)
                        get_course(alt, temp_courselist)._sections[alpha[k]] = arrrrrr

                        # give the student that class in their schedule                 
                        student[i].student_classes[alpha[k]] = [get_course(alt, temp_courselist)._name]

                        # add the course to the master timetable
                        master[alpha[k]].append(get_course(alt, temp_courselist)._description)

                        # check if linear
                        if (get_course(alt, temp_courselist).is_linear and alpha[(k + 4) % 8] not in student[i].student_classes):
                            
                            # add to the opposite semester same block in student classes
                            student[i].student_classes[alpha[(k + 4) % 8]] = [get_course(alt, temp_courselist)._name]

                            # add another slot in master timetable
                            master[alpha[(k + 4) % 8]].append(get_course(alt, temp_courselist)._description)

                        # update number of classes the course has
                        get_course(alt, temp_courselist)._currentClasses = get_course(alt, temp_courselist)._currentClasses + 1
                    
                        # break on success
                        break


    # see how good the solution is and store it if it is better than the last one, save it
        
        #best_master
        #best_student
        #best_courselist
    if (students_with_eight_courses(student) >= students_with_eight_courses(best_student)): 
        best_master = copy.deepcopy(master) 
        best_student = copy.deepcopy(student)
        best_courselist = copy.deepcopy(temp_courselist)  

    # clear curent variables
        # student
        # master
        # temp_courselist
    master.clear()
    del temp_courselist
    for i in range(len(student)):
        student[i].student_classes.clear()

# DISPLAY FOR THE BEST SOLUTION

def show(itemslist):
    out = ""
    for item in itemslist:
        out = out + item + "\n\n"
    return out


table = Table(title="TimeTable")
rows = list(best_master.values())
columns = alpha

for column in columns:
    table.add_column(column, no_wrap = False)
entries = []
for row in rows:
    entries.append(show(row))
table.add_row(*entries, style='bright_green')

console = Console() 
console.print(table)  




print("percent of courses granted", score(best_student) // 0.001 / 10, " % ")
print("percent of courses + alts granted", score_with_alternates(best_student) // 0.001 / 10, " % ")
print("percent of students with eight courses", students_with_eight_courses(best_student) // 0.001 / 10, " % ")
print("percent of students with 8 courses + alts", students_with_eight_courses_including_alternates(best_student) // 0.001 / 10, " % ")


def select_student(id):
    for key in best_student[int(id) - 1000].student_classes:
        for l in best_student[id - 1000].student_classes[key]:
            print(key, ": ", get_course(l, best_courselist)._description)
    print("\n")

STUDENT_ID = 1837
print("\nStudent ", STUDENT_ID, ":")
print(best_student[STUDENT_ID - 1000].student_classes)
print("\n")
select_student(STUDENT_ID)
print("\n")
print(best_student[STUDENT_ID - 1000]._course_requests)
print("\n")
print(best_student[STUDENT_ID - 1000]._alternates)
print("\n")

for upo in best_student[STUDENT_ID - 1000]._course_requests:
    print(get_course(upo, best_courselist)._description)

print("\n")

for upo in best_student[STUDENT_ID - 1000]._alternates:
    if (not get_course(upo, best_courselist) == "not found"):
        print(get_course(upo, best_courselist)._description)
print("\n\n")

COURSE_NAME = "MPHE-09--L"
print(COURSE_NAME, ":   ")
print(get_course(COURSE_NAME, best_courselist)._sections)

COURSE_NAME = "MADER09---"
print(COURSE_NAME, ":   ")
print(get_course(COURSE_NAME, best_courselist)._sections)

#for course in courselist:
 #   print(course._description, " : " , course._sections)

for i in range(len(best_courselist)):
    print(courselist[i]._name, " --> ", best_courselist[i]._name)

with open("seed.txt", "w") as file:
    
    
    for course in best_courselist:

        lin = 1
        if not course.is_linear:
            lin = 2

        file.write(str(course._name) + ",,"+ str(course._temp_description) + ",Department,,N,," + str(lin) + ",1," + str(course._class_size) + ",C,,Priority,," + str(int(course.number_of_classes_per_year)) + ",,,,Y\n")
