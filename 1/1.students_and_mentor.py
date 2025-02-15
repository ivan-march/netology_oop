import random


class Gradeable:
    """
    Parent class for Student and Lector to calculate avarage grade and
    compare instances.
    """
    def average_grade(self):
        grades_list = sum(self.grades.values(), [])
        return round(sum(grades_list) / len(grades_list), 2) if grades_list else 0.0

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.average_grade() == other.average_grade()

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.average_grade() > other.average_grade()


class Student(Gradeable):
    """
    Student, role - study courses.
    """
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lect(self, lecturer, course, grade):
        if not (1 <= grade <= 10):
            return 'Ошибка: оценка должна быть от 1 до 10'

        if (
            isinstance(lecturer, Lecturer) and
            course in lecturer.courses_attached and
            course in self.courses_in_progress
        ):
            lecturer.grades.setdefault(course, []).append(grade)
        else:
            return 'Ошибка'

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self.average_grade()}\n'
            f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
            f'Завершенные курсы: {", ".join(self.finished_courses)}'
        )


class Mentor:
    """
    Mentor. Parent class for Lecturer and Reviewer.
    """
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'


class Lecturer(Mentor, Gradeable):
    """
    Lecturer, role - gives lectures.
    """
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return super().__str__() + f'\nСредняя оценка за лекции: {self.average_grade():.2f}'


class Reviewer(Mentor):
    """
    Reviewer, role - check homeworks.
    """
    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student) and
            course in self.courses_attached and
            course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def calc_average_hw_grade(students, course) -> float:
    total_grades = []
    total_grades = [grade for student in students if course in student.grades for grade in student.grades[course]]
    return round(sum(total_grades) / len(total_grades), 2) if total_grades else 0.0

def calc_average_lecturer_grade(lecturers, course) -> float:
    total_grades = []
    total_grades = [grade for lecturer in lecturers if course in lecturer.grades for grade in lecturer.grades[course]]
    return round(sum(total_grades) / len(total_grades), 2) if total_grades else 0.0


# набор данных для иницилазиации объектов
courses = ['Python', 'Git', 'Java', 'Введение в программирование']
names = ['Sam', 'Petr', 'Jack', 'Den', 'Rome', 'Michel']
genders = ['male', 'female']
surnames = ['Maikov', 'Nosov', 'Reactov', 'Nedrov', 'Mausovich']
grades = range(1, 11)

# создаём проверяющего
reviewer = Reviewer(name=random.choice(names), surname=random.choice(surnames))
reviewer.courses_attached += courses
print('1. Проверяющий:')
print(reviewer)

# создаём лекторов
lecturers = {}
for i in range(10):
    lecturers[i] = Lecturer(
        name=random.choice(names),
        surname=random.choice(surnames)
    )
    lecturers[i].courses_attached += courses
print('2. Случайный лектор из списка:')
print(random.choice(list(lecturers.values())))

# создаём студентов
students = {}
for i in range(100):
    students[i] = Student(
        name=random.choice(names),
        surname=random.choice(surnames),
        gender=random.choice(genders)
    )
    students[i].finished_courses += [random.choice(courses)]
    actual_courses = [course for course in courses if course not in students[i].finished_courses]
    students[i].courses_in_progress += actual_courses
    # оцениваем студента
    for course in students[i].courses_in_progress:
        reviewer.rate_hw(
            student=students[i],
            course=course,
            grade=random.choice(grades)
        )
print('3. Случайный студент из списка:')
print(random.choice(list(students.values())))

# оцениваем лекторов
for lecturer in lecturers.values():
    for course in lecturer.courses_attached:
        for student in students.values():
            student.rate_lect(
                lecturer=lecturer,
                course=course,
                grade=random.choice(grades)
            )

print('4. Сравниваем средниие оценки за домашние задания студентов:')
student1 = students[0]
student2 = students[1]
print(
    f'{student1.name} {student1.surname} ({student1.average_grade()}) и',
    f'{student2.name} {student2.surname} ({student2.average_grade()})'
)
print(
    f'{student1.average_grade()} == {student2.average_grade()}:',
    student1 == student2
)
print(
    f'{student1.average_grade()} > {student2.average_grade()}:',
    student1 > student2
)
print(
    f'{student1.average_grade()} < {student2.average_grade()}:',
    student1 < student2
)

print('5. Сравниваем средниие оценки за лекции лекторов:')
lecturer1 = lecturers[0]
lecturer2 = lecturers[1]
print(
    f'{lecturer1.name} {lecturer1.surname} ({lecturer1.average_grade()}) и',
    f'{lecturer2.name} {lecturer2.surname} ({lecturer2.average_grade()})'
)
print(
    f'{lecturer1.average_grade()} == {lecturer2.average_grade()}:',
    lecturer1 == lecturer2
)
print(
    f'{lecturer1.average_grade()} > {lecturer2.average_grade()}:',
    lecturer1 > lecturer2
)
print(
    f'{lecturer1.average_grade()} < {lecturer2.average_grade()}:',
    lecturer1 < lecturer2
)

course = random.choice(courses)
print(
    f'6. Средняя оценка за домашние задания по всем студентам в рамках курса {course}:',
    calc_average_hw_grade(students=students.values(), course=course)
)

course = random.choice(courses)
print(
    f'7. Cредняя оценка за лекции всех лекторов в рамках {course}:',
    calc_average_lecturer_grade(lecturers=lecturers.values(), course=course)
)
