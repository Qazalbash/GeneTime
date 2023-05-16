from numba import njit


@njit(cache=True, fastmath=True)
def convertTime(minutes: int) -> tuple[int, int, bool]:
    """
    Convert minutes into 12-hour time format
    :param minutes:
    :return:
    """
    hours = minutes // 60
    minute = minutes % 60
    AM = hours < 12
    if hours > 12:
        hours -= 12
    return hours, minute, AM


DAY_START = 510  # 08:30 AM
DAY_END = 1110  # 06:30 PM


class Day:
    """enum type class for Days"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Classroom:
    """class for Classroom"""

    def __init__(self, name: str) -> None:
        self.id = hash(name)
        self.name = name

    def __hash__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return f"Classroom<<<{self.name}>>>"

    def __repr__(self) -> str:
        return f"Classroom<<<{self.name}>>>"

    def __eq__(self, other) -> bool:
        return self.id == other.id


class Instructor:

    def __init__(self, name: str) -> None:
        self.id = hash(name)
        self.name = name
        self.office_hours = []

    def __str__(self) -> str:
        return f"Instructor<<<{self.name}>>>"

    def __repr__(self) -> str:
        return f"Instructor<<<{self.name}>>>"

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other: "Instructor") -> bool:
        return self.id == other.id

    def __ne__(self, other: "Instructor") -> bool:
        return self.id != other.id


class Class:
    """class for Class"""
    COUNTER: int = 0

    def __init__(self, name: str, instructor: Instructor, duration: int) -> None:
        self.id = hash(name + str(duration) + str(Class.COUNTER))
        self.name = name
        self.instructor = instructor
        self.start_time = None
        self.duration = duration
        self.day = None
        Class.COUNTER += 1

    def __hash__(self) -> int:
        return self.id

    def __str__(self) -> str:
        representation = f"Class<<<{self.name}, {self.instructor}"
        if self.start_time:
            hours, minute, AM = convertTime(self.start_time)
            AM = "A" * AM + "P" * (not AM) + "M"
            representation += f", {hours}:{minute} {AM}"
        representation += f", {self.duration}"
        if self.day:
            representation += f", {self.day}"
        representation += f">>>"
        return representation

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: "Class") -> bool:
        return self.id == other.id and self.name == other.name

    def __ne__(self, other: "Class") -> bool:
        return self.start_time != other.start_time or self.name != other.name

    def __lt__(self, other: "Class") -> bool:
        return self.start_time < other.start_time

    def __le__(self, other: "Class") -> bool:
        return self.start_time < other.start_time

    def __gt__(self, other: "Class") -> bool:
        return self.start_time > other.start_time

    def __ge__(self, other: "Class") -> bool:
        return self.start_time >= other.start_time
