# Plans Class File
import csv

class humanitarian_plan:
    def __init__(self, description, geographical_location, start_date):
        self.description = description
        self.geographical_location = geographical_location
        self.start_date = start_date
    
    def display_plan(self):
        return{
        "Description": self.description,
        "Geographical Location": self.geographical_location,
        "Start Date": self.start_date
        }




       
