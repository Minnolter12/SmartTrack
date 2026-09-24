import functools
import math

DEV_MODE: bool = True

def debug_mode(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if DEV_MODE:
            return func(*args, **kwargs)
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
        periods: int = 1,  
        classes_attended: int = 0, 
        classes_happened: int = 0, 
        total_classes: int = 0, 
        min_attendance: int | None = 75,
    ) -> None:
        self.name = name
        self.periods = periods
        self.credits = credits
        self.min_attendance = min_attendance
        
        self._classes_happened = classes_happened
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
    def classes_happened(self) -> int:
        return self._classes_happened

    @classes_happened.setter
    def classes_happened(self, value: int) -> None:
        if value < 0:
            raise ValueError("Classes happened cannot be negative.")
        self._classes_happened = value

    @property
    def classes_attended(self) -> int:
        return self.__classes_attended

    @classes_attended.setter
    def classes_attended(self, value: int) -> None:
        if value < 0 or value > self.classes_happened:
            raise ValueError("Attended periods cannot exceed total happened periods.")
        self.__classes_attended = value

    def log_attendance(self, class_attended: bool) -> None:
        if not isinstance(class_attended, bool):
            raise TypeError("Attendance must be a strict boolean value (True/False).")
            
        if class_attended:
            self.classes_happened += self.periods
            self.classes_attended += self.periods
        else: 
            self.classes_happened += self.periods

    def calculate_total_classes(self, months: int = 0, weeks: int = 0) -> None:
        if months < 0 or weeks < 0:
            raise ValueError("Months and weeks cannot be lesser than 0")
        self.total_classes = (months * 4 * self.credits) + (weeks * self.credits)

    def attendance_percentage(self, format: type = float) -> int | float:
        if self.classes_happened == 0:
            raise ZeroDivisionError("No periods have occurred yet; cannot calculate percentage.")

        percentage = (self.classes_attended / self.classes_happened) * 100
        if format is int:
            return int(percentage)
        elif format is float:
            return float(f"{percentage:.2f}")
        else: 
            raise TypeError("Invalid format type requested.")

    def calculate_safe_leaves(self) -> int:
        if self.classes_happened == 0:
            return 0
        target = self.min_attendance if self.min_attendance is not None else 75
        target_fraction = target / 100
        

        max_total_absences = math.floor(self.classes_attended / target_fraction) - self.classes_happened
        if max_total_absences <= 0:
            return 0
        return max_total_absences // self.periods  

    def regain_min_attendance(self) -> int | bool:
        target = self.min_attendance if self.min_attendance is not None else 75
        target_fraction = target / 100
        
        current_pct = (self.classes_attended / self.classes_happened) * 100 if self.classes_happened > 0 else 0
        if current_pct >= target:
            return 0
            
        if target_fraction >= 1.0:
            return False  
            
        required_periods = math.ceil((target_fraction * self.classes_happened - self.classes_attended) / (1 - target_fraction))
        required_classes = math.ceil(required_periods / self.periods)
        
        remaining_classes = self.total_classes - (self.classes_happened // self.periods)
        if required_classes <= remaining_classes:
            return required_classes
        return False


class TheoryCourses(Course):
    def __init__(self, name: str, credits: int, periods_per_theory_class: int = 1, **kwargs) -> None:
        super().__init__(name=name, credits=credits, periods=periods_per_theory_class, **kwargs)


class LabCourses(Course):
    def __init__(self, name: str, credits: int, periods_per_lab: int = 3, **kwargs) -> None:
        super().__init__(name=name, credits=credits, periods=periods_per_lab, **kwargs)


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
        self.__none_or_val = attendance

    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    @debug_mode
    def print_course(self) -> None:
        for course in self.courses:
            print(f"Course: {course.name} ({type(course).__name__})")
            print(f"Credits: {course.credits} | Periods/Slot: {course.periods}")
            print(f"Attendance: {course.classes_attended}/{course.classes_happened} periods")
            try:
                print(f"Percentage: {course.attendance_percentage()}%")
                print(f"Safe Leaves Remaining: {course.calculate_safe_leaves()} slots")
            except ZeroDivisionError:
                print("Percentage: N/A")
            print("--------------------------------------")
