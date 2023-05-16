import csv
import tkinter as tk


class ScheduleViewer(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Weekly Schedule Viewer")

        self.filename = "schedules/schedule.csv"

        # Create a list to store the class schedule data
        self.schedule_data = []

        # Create a dictionary to store the colors for each program
        self.program_colors = {}

        # Read the class schedule data from the CSV file
        self.read_schedule_data(self.filename)

        # Initialize the GUI
        self.create_widgets()

    def read_schedule_data(self, filename):
        """Read the class schedule data from the CSV file."""
        with open(filename, "r") as f:
            reader = csv.reader(f)
            # Skip the header row
            next(reader)
            for row in reader:
                # Parse the row data
                day, start_time, end_time, program, course_code, course_title, class_nbr, section, room, instructor, actual_class_duration = row
                # Store the class schedule data in a list
                self.schedule_data.append({
                    "day": day,
                    "start_time": start_time,
                    "end_time": end_time,
                    "program": program,
                    "course_code": course_code,
                    "course_title": course_title,
                    "class_nbr": class_nbr,
                    "section": section,
                    "room": room,
                    "instructor": instructor,
                    "actual_class_duration": actual_class_duration
                })
                # Generate a color for the program if it does not exist
                if program not in self.program_colors:
                    self.program_colors[program] = "#" + format(
                        hash(program) % 0xffffff, "06x")

    def create_widgets(self):
        """Create the GUI widgets."""
        # Create the canvas to display the class schedule
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create the headers for the days of the week
        days_of_week = [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
            "Sunday"
        ]
        for i, day in enumerate(days_of_week):
            self.canvas.create_text(i * 110 + 100,
                                    50,
                                    text=day,
                                    font=("Arial", 16, "bold"))

        # Create the time slots for each hour of the day
        for i in range(24):
            time = "{:02d}:00".format(i)
            self.canvas.create_text(50,
                                    i * 25 + 100,
                                    text=time,
                                    font=("Arial", 10))

        # Draw the class schedule
        for class_data in self.schedule_data:
            day = class_data["day"]
            start_time = class_data["start_time"]
            end_time = class_data["end_time"]
            program = class_data["program"]
            course_code = class_data["course_code"]
            course_title = class_data["course_title"]
            class_nbr = class_data["class_nbr"]
            section = class_data["section"]
            room = class_data["room"]
            instructor = class_data["instructor"]
            actual_class_duration = class_data["actual_class_duration"]

            # Calculate the position and size of the class rectangle
            day_index = days_of_week.index(day)
            start_hour, start_minute = map(int, start_time.split(":"))
            start_y = start_hour * 25 + start_minute / 60 * 25
            # Calculate the end time of the class
            end_hour, end_minute = map(int, end_time.split(":"))
            end_y = end_hour * 25 + end_minute / 60 * 25

            # Calculate the width of the class rectangle
            width = 100 / len(days_of_week)

            # Create the class rectangle
            x0 = day_index * width + 20
            y0 = start_y + 100
            x1 = x0 + width - 40
            y1 = end_y + 100
            color = self.program_colors[program]
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

            # Create the class label
            label_text = "{}\n{}\n{}\n{}\n{}".format(course_code, course_title,
                                                     class_nbr, section,
                                                     instructor)
            label_x = x0 + 10
            label_y = y0 + 10
            label_width = x1 - x0 - 20
            label_height = y1 - y0 - 20
            label = tk.Label(self.canvas,
                             text=label_text,
                             font=("Arial", 10),
                             wraplength=label_width,
                             justify="left",
                             anchor="nw")
            label.place(x=label_x,
                        y=label_y,
                        width=label_width,
                        height=label_height)

            # Create the actual class duration label
            actual_class_duration_label_text = "({})".format(
                actual_class_duration)
            actual_class_duration_label_x = x0 + label_width - 50
            actual_class_duration_label_y = y1 - 20
            actual_class_duration_label = tk.Label(
                self.canvas,
                text=actual_class_duration_label_text,
                font=("Arial", 8),
                anchor="ne")
            actual_class_duration_label.place(x=actual_class_duration_label_x,
                                              y=actual_class_duration_label_y)


# filename = 'schedules/schedule.csv'
# gui = ScheduleViewer(filename)

root = tk.Tk()
app = ScheduleViewer(root)
app.mainloop()
