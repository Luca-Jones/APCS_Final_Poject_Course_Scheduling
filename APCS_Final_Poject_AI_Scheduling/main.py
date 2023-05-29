#main algorithm for sorting students into the timetable

from rich.console import Console
from rich.table import Table
import json
import os
os.system("cls")


# create timetable of classes

fp = open('Schedule2022.json')

master_schedule = json.load(fp)

for sem in master_schedule:
    print(sem)

fp.close()

# create student schedules

# student_schedules = {}


f = open('studentList.json')

student_list = json.load(f)

for i in student_list.values():
    
    # resets courses for each student
    courses = []

    for j in i["Requests"]:

        # if class is still available, add
        courses.append(j)

    if len(courses) < 8:
        for j in i["Alternates"]:

            # if class is still available, add
            courses.append(j)
    
    # add courses to student
    i["Courses"] = courses
    
print(student_list)


f.close()

with open('master_schedule.json', 'w') as file:
    json.dump(master_schedule, file)

'''
with open('studentSchedules.json', 'w') as file:
    json.dump(student_schedules, file)
'''