import pandas as pd
class Camps:
    def __init__(self):
        self.camps_data = pd.read_csv('./files/camps.csv')
    def get_data(self):
        return self.camps_data
    def write_data(self, camp_id, new_row):
        camp_index = self.camps_data.index[self.camps_data['camp_id'] == camp_id]
        self.camps_data.iloc[camp_index, :] = new_row
        self.camps_data.to_csv('./files/camps.csv', index=False)
        return True