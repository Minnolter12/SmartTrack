class AttendanceNotValidError(Exception): pass

class Course:

    __max_credits: int = 6

    def __init__(
        self,
        name: str,
        credits: int,
        classes_attended: int,
        total_classes: int,
        min_attendance: int | None = None,
    ) -> None:
        self.name = name
        self.credits = credits
        self.min_attendance = min_attendance

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
            raise ValueError("Credits cannot be greater than 6 nor can it be less than")

    @property
    def classes_attended(self) -> int:
        return self.__classes_attended

    @classes_attended.setter
    def classes_attended(self, value: int) -> None:
        if value < 0 or value > self.total_classes:
            raise ValueError("Attended classes cannot be more than number of classes attended")
        Course.__classes_attended = value




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


sem1 = Semester(1, 75)

electrical_enginerring = Course(
    "Electrical Engineering", 4, 4, 10, 75
)

sem1.add_course(electrical_enginerring)

