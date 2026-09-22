import functools

DEV_MODE: bool = True

def debug_mode(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if DEV_MODE:
            return func(*args, **kwargs)
        else:
            return None
    return wrapper

class AttendanceNotValidError(Exception):
    pass

class Course:

    __max_credits: int = 6

    def __init__(
        self,
        name: str,
        credits: int,
        classes_attended: int = 0, 
        classes_happened: int = 0, # used to calculate percentages
        total_classes: int = 0, # used during prediction
        min_attendance: int | None = None,
    ) -> None:
        self.name = name
        self.credits = credits
        self.min_attendance = min_attendance
        self.classes_happened = classes_happened

        self.total_classes = total_classes
        self.classes_attended = classes_attended

    @property
    def total_classes(self) -> int:
        return self.__total_classes

    @total_classes.setter
    def total_classes(self, value: int) -> None:
        if value < 0:
            raise ValueError("Total classes cannot be negative.")
        self.__total_classes = value

    @property
    def max_credits(self) -> int:
        return self.__max_credits


    @max_credits.setter
    def max_credits(self, credits) -> None:
        if credits >= 0 and credits <= 6:
            self.__max_credits = credits
        else:
            raise ValueError("Credits cannot be greater than 6 nor can it be less than 0!")

    @property
    def classes_attended(self) -> int:
        return self.__classes_attended


    @classes_attended.setter
    def classes_attended(self, value: int) -> None:
        if value < 0 or value > self.total_classes:
            raise ValueError("Attended classes cannot be more than total classes.")
        
        self.__classes_attended = value

    def log_attendance(self, class_attended: bool) -> None:
        if self.classes_attended > self.classes_happened:
            raise AttendanceNotValidError()
        
        if class_attended:
            self.classes_happened += 1
            self.classes_attended += 1

        else: self.classes_happened += 1

    def calculate_total_classes(self, months: int = 0, weeks: int = 0) -> None:
        if months < 0 or weeks < 0:
            raise ValueError("Months and weeks cannot be lesser than 0")

        self.total_classes = (months * 4 * self.credits) + (weeks * self.credits)

    def attendance_percentage(self, format: type = float) -> int | float:
        if self.classes_happened == 0:
            raise ZeroDivisionError("Classes havent happened yet cannot divide by 0")
        
        if format is int:
            return int((self.classes_attended / self.classes_happened) * 100)
        else: 
            return float(f"{(self.classes_attended / self.classes_happened) * 100:.2f}")



class Semester:

    def __init__(self, sem_number: int, min_attendance: int = 75) -> None:
        self.sem_number = sem_number
        self.min_attendance = min_attendance
        self.courses: list[Course] = []

    @property
    def min_attendance(self) -> int:
        return self.__min_attendance

    @min_attendance.setter
    def min_attendance(self, attendance: int) -> None:
        if attendance > 100 or attendance < 0:
            raise AttendanceNotValidError("Attendance must behave like percentages")

        self.__min_attendance = attendance

    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    @debug_mode
    def print_course(self) -> None:
        for course in self.courses:
            print(f"Course: {course.name}")
            print(f"Credits: {course.credits}")
            print(f"Attendance: {course.classes_attended}/{course.total_classes}")
            print("--------------------------------------")


semester_one = Semester(1, 75)

semester_one.add_course(
    course=Course(
        "Signals and Systems", 4, min_attendance=75
    )
)

course = semester_one.courses[0]
course.calculate_total_classes(5, 2)

course.log_attendance(True)
course.log_attendance(True)

print(course.attendance_percentage())

course.log_attendance(False)
print(course.attendance_percentage())
