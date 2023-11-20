# Admin Class File
from Plans import humanitarian_plan
import csv


class Admin:
  # add functions here
  # remember for functions added the first parameter has to be a self
    def __init__(self):
        self.plans_file = '/Users/geruiyi/Desktop/Python project/intro-programming/files/plans.csv'

    
    def read_csv(self, filepath):
        try:
            with open(filepath, mode='r', encoding='utf-8-sig') as file:  
                return list(csv.DictReader(file))
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return []

    
    def write_csv(self, filepath, data):
        try:
            with open(filepath, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())

                if file.tell() == 0:
                    writer.writeheader()
                
                writer.writerows(data)
        except Exception as e:
            print(f"Error writing file {filepath}: {e}")


    def create_humanitarian_plan(self):
        description = input("Enter the description of the plan: ")
        geographical_location = input("Enter the geographical location of the plan: ")
        start_date = input("Enter the start date of the plan (YYYY/MM/DD): ")
        
        plan = humanitarian_plan(description, geographical_location, start_date)
        plan_data = plan.display_plan()
    
        self.write_csv(self.plans_file, plan_data)

    
    def display_plans(self):
        existing_data = self.read_csv(self.plans_file)

        for row in existing_data:
            print(row)


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
  
