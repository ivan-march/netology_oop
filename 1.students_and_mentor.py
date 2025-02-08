class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lect(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'


class Mentor:
    """
    Mentor. Parent class for Lecturer and Reviewer.
    """
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    """
    Lecturer, role - gives lectures.
    """
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}


class Reviewer(Mentor):
    """
    Reviewer, role - check homeworks.
    """
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


#
lecturer = Lecturer(name='Rich', surname='Hoster')
lecturer.courses_attached += ['Python']

#
student = Student(name='Alex', surname='Bykov', gender='male')
student.courses_in_progress += ['Python', 'C++']
student.rate_lect(lecturer=lecturer, course='Java', grade='10')
student.rate_lect(lecturer=lecturer, course='Python', grade='10')
student.rate_lect(lecturer=lecturer, course='Python', grade='8')
print(lecturer.grades['Python'])

#
reviewer = Reviewer(name='Rost', surname='Lister')
reviewer.courses_attached += ['Python']
reviewer.rate_hw(student=student, course='Python', grade='9')
reviewer.rate_hw(student=student, course='Python', grade='10')
print(student.grades.get('Python'))
