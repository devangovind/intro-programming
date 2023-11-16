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


def save_plan_to_csv(plan, filename = "humanitarian plans.csv"):
    fieldnames = ["Description", "Geographical Location", "Start Date"]
    
    with open(filename, mode = 'a', newline = '') as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames)

        if file.tell() == 0:
            writer.writeheader()

            writer.writerow(plan.display_plan())
    print(f"The new humanitarian plan saved successfully to {filename}")


def display_plans(filename = "humanitarian plans.csv"):
    with open (filename, mode = 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)


def create_plan():
    description = input("Enter the description of the plan: ")
    geographical_location = input("Enter the geograpgical location of the plan: ")
    start_date = input("Enter the start date of the plan (YYYY/MM/DD): ")
    
    plan = humanitarian_plan(description, geographical_location, start_date)
    
    save_plan_to_csv(plan)


def menu():
    while True:
        print("1. Create a new humanitarian plan")
        print("2. Display all the existing humanitarian plans")

        a = input("Please enter your requirement: ")

        if a == '1':
            create_plan()
        elif a == '2':
            display_plans()
        else:
            print("Invalid number! Please enter it again.")


if __name__ == "__main__":
     menu()

