import pandas as pd


class DataCleaning:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.class_nbr_dict = {}
        self.df = pd.read_csv(self.filename)
        self.numclasses_multipleinstances = 0
        self.extractingFromDataset()
        self.getnumclasses()

    def extractingFromDataset(self):
        # Extract the unique values of "Class nbr" and "Instructor and store them in a list
        self.room_list = self.df["Room"].unique().tolist()
        self.instructor_list = self.df["Instructor"].unique().tolist()
        for instructorName in self.instructor_list:
            if "\n" in instructorName:
                splittedInstructorName = instructorName.split("\n")
                firstInstructorName = splittedInstructorName[0]
                self.instructor_list.remove(instructorName)
                if firstInstructorName not in self.instructor_list:
                    self.instructor_list.append(firstInstructorName)

        # Count the frequency of each Class nbr and store it in a dictionary
        class_nbr_freq = self.df["Class nbr"].value_counts().to_dict()

        # Loop through each row in the DataFrame and add the "Class nbr" and relevant values to the dictionary
        for index, row in self.df.iterrows():
            class_nbr = row["Class nbr"]
            title = row["Course title"]
            duration = row["Actual Class Duration"]
            instructor = row["Instructor"]
            if "\n" in instructor:
                instructor = instructor.split("\n")
                instructor = instructor[0]
            self.class_nbr_dict[class_nbr] = {"Course title": title, "Instructor": instructor,
                                              "Actual Class Duration": duration, "Frequency": class_nbr_freq[class_nbr]}

    def getnumclasses(self):
        for class_number, info in self.class_nbr_dict.items():
            freq = info["Frequency"]
            if freq > 1:
                self.numclasses_multipleinstances += 1


dc = DataCleaning("Spring 2023 Schedule.csv")

# print("-------- Statistics--------")
# print("Number of classrooms: ",len(dc.room_list))
# print("Number of Classes (no. of unique class br) at Habib: ",len(dc.class_nbr_dict))
# print("Dictionary storing all data")
# print(len(dc.class_nbr_dict))


# print(dc.room_list)
