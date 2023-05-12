import os
os.system("cls")


class Course:
    def __init__(self, name, number_of_classes_per_year, class_size, is_required, is_outside_timetable, sequencing, blocking):
        self._name = name
        self.number_of_classes_per_year = number_of_classes_per_year
        self._class_size = class_size
        self._is_required = is_required
        self._is_outside_timetable  = is_outside_timetable
        self.sequencing = sequencing
        self.blocking = blocking
    def __str__(self):
        return str(self._name) + "\n"


math = Course("math", 2, 20, False, False, [], [])
print(math)

class Student:
    def __init__(self, id, course_requests, alternates):
        self._id = id
        self._course_requets = course_requests
        self._alternates = alternates
    def __str__ (self):
        return str("id = " + str(self._id) + " \nRequests = " + str(self._course_requets) + " \nAlternates = " + str(self._alternates))


bob = Student(1000, ["MMA9", "XBA12"], [])
print(bob)