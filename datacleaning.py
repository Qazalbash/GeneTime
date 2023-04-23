import pandas as pd


class DataCleaning:
    """Class to clean the data from the dataset"""

    def __init__(self, filename: str) -> None:
        """Initialize the class and extract the data from the dataset"""
        self.class_nbr_dict = {}
        self.df = pd.read_csv(filename)
        self.extractingFromDataset()

    def extractingFromDataset(self) -> None:
        """Extract the data from the dataset and store it in a dictionary"""
        # Extract the unique values of "Class nbr" and store them in a list
        self.room_list = self.df["Room"].unique().tolist()

        # Count the frequency of each Class nbr and store it in a dictionary
        class_nbr_freq = self.df["Class nbr"].value_counts().to_dict()

        # Loop through each row in the DataFrame and add the "Class nbr" and relevant values to the dictionary
        for index, row in self.df.iterrows():
            class_nbr = row["Class nbr"]
            title = row["Course title"]
            instructor = row["Instructor"]
            if "\n" in instructor:
                instructor = instructor.split("\n")
            duration = row["Actual Class Duration"]
            self.class_nbr_dict[class_nbr] = {
                "Course title": title,
                "Instructor": instructor,
                "Actual Class Duration": duration,
                "Frequency": class_nbr_freq[class_nbr],
            }
