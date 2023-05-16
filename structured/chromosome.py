from primitives import *


class Chromosome:
    """class for chromosome"""

    def __init__(self, classrooms: list[Classroom], instructors: list[Instructor]) -> None:
        self.instructors = instructors
        self.fitness = None
        self.schedule = {day: {room: [] for room in classrooms} for day in
                         [Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]}
        self.instructors_schedule = {instructor: [] for instructor in instructors}

    def __str__(self) -> str:
        return str(self.schedule)

    def __repr__(self) -> str:
        return str(self.schedule)
