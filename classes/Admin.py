# Admin Class File
import datetime
import csv
import pandas as pd
from datetime import date
from datetime import datetime

class Admin:
  # add functions here
  # remember for functions added the first parameter has to be a self
  def create_humanitarian_plan(self):
    pass

  def __init__(self):
      self.camps_file = '../files/camps_file.csv'
      self.plans_file = '../files/plans_file.csv'


  def check_event_ended(self, plan_id):
     plans = pd.read_csv(self.plans_file)
     plan_details = plans[plans["Plan_ID"]== plan_id]
     plan_end_date_str = plan_details.iloc[0,-1]
     today = date.today()
     plan_end_date = datetime.strptime(plan_end_date_str, "%d/%m/%Y").date()
     #returns True if end date has occured and False if end date has not
     return today > plan_end_date 
     

  def display_plan(self, plan_id):
     camps = pd.read_csv(self.camps_file)
     plans = pd.read_csv(self.plans_file)

     if self.check_event_ended(plan_id):
        return "This humanitarian plan has ended."
     else:
        plan_details = camps[camps['Plan_ID']== plan_id]
        if plan_details.empty:
           return "This humanitarian plan does not exist."
        else:
           return plan_details[["Camp_ID","Num_Of_Refugees","Num_Of_Volunteers"]]

     
