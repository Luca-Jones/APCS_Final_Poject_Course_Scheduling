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