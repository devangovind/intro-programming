import csv
import pandas as pd
from datetime import date
from datetime import datetime


def read_csv(filepath):
    with open(filepath, mode='r') as file:
        return list(csv.DictReader(file))

def write_csv(filepath, data):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)



data = pd.read_csv("./files/camps_file.csv")
print(data)

plan_details = data[data['Plan_ID']== "P54321"]
print(type(plan_details))
if plan_details.empty:
    print("dont exist")
else:
    print(plan_details[["Camp_ID","Num_Of_Refugees","Num_Of_Volunteers"]])

print("-------------------------------------------")
plans = pd.read_csv("./files/plans_file.csv")
plan_details = plans[plans["Plan_ID"]== "P54321"]
# plan_end = plan_details[["End Date"]].values[0]
plan_end = plan_details.iloc[0,-1]
print(plan_end)
print(type(plan_end))
print(date.today())
today = date.today()
format = "%d%m%Y"
# print(datetime.datetime.strptime(plan_end, format))
date_object = datetime.strptime(plan_end, "%d/%m/%Y").date()
print(date_object)
print(today > date_object)
# print(type(date_object))
# print(type(today))
test_date = datetime.strptime("18/11/2023", "%d/%m/%Y").date()
print(today > test_date)