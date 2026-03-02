from pydantic import BaseModel, Field
from typing import List
import pandas as pd
import os

# Define a model for individual course details
class Course (BaseModel):
    Course_code: str = Field(..., description="Course code")  # Unique identifier for the course
    course_name: str = Field(..., description="Course name")  # Name of the course
    credits: str = Field(..., description="Number of credits")  # Credit hours for the course
    instructor: str = Field(..., description="Name of the instructor")  # Instructor's name
    room: str = Field(..., description="Room")  # Room where the course is held
    days: str = Field(..., description="Days when course is taken")  # Days of the week for the course
    start_time: str = Field(..., description="When the course starts")  # Start time of the course
    end_time: str = Field(..., description="When the course ends")  # End time of the course
    max_enrollment: str = Field(..., description="Maximum enrollment")  # Maximum number of students allowed
    total_enrollment: str = Field(..., description="Total enrollment")  # Current number of enrolled students

# Define a model for a collection of courses
class Offerings(BaseModel):
    courses: List[Course] = Field(..., description="List of course offerings")  # List of all courses

# Function to save course data to a CSV file
def SaveReadContents(Course: Offerings):
    # Convert the list of courses to a DataFrame
    Frame = pd.DataFrame([course.model_dump() for course in Course.courses])
    result_path = os.getcwd()  # Get the current working directory
    
    # Define the path to save the CSV file
    csv_saving_path = os.path.join(result_path, "Final_Results.csv")
    Frame.to_csv(csv_saving_path)  # Save the DataFrame to a CSV file
    excel_saving_path= os.path.join(result_path, "Final_Results.xlsx")
    Frame.to_excel(excel_saving_path)