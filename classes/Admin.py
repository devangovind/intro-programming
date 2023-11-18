# Admin Class File
from Plans import humanitarian_plan
import csv


class Admin:
  # add functions here
  # remember for functions added the first parameter has to be a self
    def __init__(self, filename = "humanitarian_plans.csv"):
        self.filename = filename

    def save_plan_to_csv(self, plan):
        fieldnames = ["Description", "Geographical Location", "Start Date"]

        with open(self.filename, mode = 'a', newline = '') as file:
            writer = csv.DictWriter(file, fieldnames = fieldnames)

            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(plan.display_plan())
        print(f"The newly humanitarian plan saved successfully in {self.filename}")

    def display_plans(self):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
    
    
    def create_humanitarian_plan(self):
        description = input("Enter the description of the plan: ")
        geographical_location = input("Enter the geographical location of the plan: ")
        start_date = input("Enter the start date of the plan (YYYY/MM/DD): ")
    
        plan = humanitarian_plan(description, geographical_location, start_date)
    
        self.save_plan_to_csv(plan)

    def menu(self):
        while True:
            print("1. Create a new humanitarian plan")
            print("2. Display the humanitarian plans")

            a = int(input("Please enter your requirement: "))

            if a == 1:
                self.create_humanitarian_plan()
            elif a == 2:
                self.display_plans()
            else:
                print("Please enter the valid number again!")

if __name__ == "__main__":
    test = Admin()
    test.menu()
  
