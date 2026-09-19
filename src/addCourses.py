class Semester:

    def __init__(self, sem_number: int, min_attendance_req: int = 75) -> None:
        self.sem_number = sem_number
        self.min_attendance_req = min_attendance_req

        self.courses = []


    @property
    def min_attendance(self) -> int:
        return self.__attendance_requirement

    @min_attendance.setter
    def min_attendance(self, attendance_req) -> None:
        self.__attendance_requirement = attendance_req        


class Course(Semester):

    def __init__(
        self, sem_number: int, name: str, 
        credits: int, attendance: int, 
        classes_attended: int, 
        total_classes: int,
    ): 
        super().__init__(self, sem_number=sem_number)

        self.name = name
        self.credits = credits
        self.attendance = attendance
        self.classes_attended = classes_attended,
        self.total_classes = total_classes
