# Plans Class File
import pandas as pd
class Plans:
    def __init__(self):
        self.plans_data = pd.read_csv('./files/plans_file.csv')
    def get_data(self):
        return self.plans_data
    def write_data(self, plan_id, new_row):
        camp_index = self.plans_data.index[self.plans_data['plan_id'] == plan_id]
        self.plans_data.iloc[camp_index, :] = new_row
        self.plans_data.to_csv('./files/plans_file.csv', index=False)
        return True