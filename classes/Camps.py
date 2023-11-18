import pandas as pd
class Camps:
    def __init__(self):
        pass
    def get_data(self):
        camps_data = pd.read_csv('./files/camps.csv')
        return camps_data