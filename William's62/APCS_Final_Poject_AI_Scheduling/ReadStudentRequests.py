from rich.console import Console
from rich.table import Table
import json
import os
os.system("cls")

student_list = {}           # list of students
student_information = {}    # values for each student
current_id = 0
test = []                   # array used to store data read from file
requests = []
alternates = []

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
                #reads line of file, stores it into test array
                line=f.readline()
                test = line.split(",", 16)

                if line=='':
                    break
                
                #if the first word in test is id then that means it is a new students requests
                #so the line number becomes 0 and the amount of alternates also becomes 0
                if test[0] == 'ID':
                    
                    if int(current_id) >= 1000:

                        #appends requests with alternates
                        student_information["Requests"] = requests
                        student_information["Alternates"] = alternates

                        # clear the lists
                        requests.clear()
                        alternates.clear()
                        
                        #creates a new student
                        student_list[int(current_id)] = student_information

                    count = 0
                    alt = 0
                    
                    #updstes the current id number of the new student
                    current_id = test[1]     

                #sees if this is a course request or not
                elif test[0] != 'Course':

                    #if it is an alternate add it to the alternate list
                    #otherwise add it to the student request list
                    if test[11] == 'Y':
                        alternates.append(test[0])
                    else:    
                        requests.append(test[0])

except FileNotFoundError:
       print ("File is not found")
else:
       f.close()


      
    
with open('studentList.json', 'w') as file:
    json.dump(student_list, file)
