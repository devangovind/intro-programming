# Plans Class File
import pandas as pd
import csv
class Plans:
    def __init__(self):
        # for Mac
        self.plans_file = 'plans_file.csv'
        self.plans_data = pd.read_csv(self.plans_file)
        
        # for windows:
        # self.plans_file = 'files\\plan_file.csv'
        # self.plans_filepath = '../files/plans_file.csv'
        # self.plans_data = pd.read_csv(self.plans_filepath)
    def get_data(self):
        self.plans_data = pd.read_csv(self.plans_file)
        return self.plans_data
    def get_plan_ids(self):
        self.plans_data = pd.read_csv(self.plans_file)
        return self.plans_data['Plan_ID'].tolist()
    def write_data(self, plan_id, new_row):
        camp_index = self.plans_data.index[self.plans_data['plan_id'] == plan_id]
        self.plans_data.iloc[camp_index, :] = new_row
        
        # for mac
        self.plans_data.to_csv(self.plans_file, index=False)
        

        return True
    def write_entire_dataframe(self, df):
        df.to_csv(self.plans_file, index=False)
    def append_dateframe(self, df):
        df.to_csv(self.plans_file, mode="a", header=False, index=False)


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




       