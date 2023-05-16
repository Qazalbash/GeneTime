import pandas as pd

from primitives import *


class Data:
    """class to load data from csv file and extract information from it"""

    def __init__(self, filename: str) -> None:
        self.multiple_section_classes = 0
        self.classes = []
        self.classrooms = []
        self.instructors = []
        self.df = pd.read_csv(filename)
        self.TOTAL_CLASSES = 0

    def extraction(self) -> None:
        class_number_freq = self.df["Class nbr"].value_counts().to_dict()

        for index, row in self.df.iterrows():
            classNumber = row["Class nbr"]
            title = row["Course title"]
            duration = row["Actual Class Duration"]

            instructor = row["Instructor"]
            instructor = instructor.strip()

            if "\n" in instructor:
                instructor = instructor.split("\n")
                instructor = instructor[0]

            instructor = Instructor(instructor)
            if instructor not in self.instructors:
                self.instructors.append(instructor)

            classroom = Classroom(row["Room"])
            if classroom not in self.classrooms:
                self.classrooms.append(classroom)

            if class_number_freq[classNumber] > 1:
                self.multiple_section_classes += 1

            for _ in range(class_number_freq[classNumber]):
                self.classes.append(Class(title, instructor, duration))
                self.TOTAL_CLASSES += 1
