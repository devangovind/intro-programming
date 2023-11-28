import pandas as pd
class Resource_requests:
    def __init__(self):
        self.resource_requests_file = './files/resource_request.csv'
        self.request_data = pd.read_csv(self.resource_requests_file)
    def get_data(self):
        self.request_data = pd.read_csv(self.resource_requests_file)
        return self.request_data
    def get_unresolved(self):
        self.request_data = pd.read_csv(self.resource_requests_file)
        return self.request_data[self.request_data['Resolved'] == False]
    def get_resolved(self):
        self.request_data = pd.read_csv(self.resource_requests_file)
        return self.request_data[self.request_data['Resolved'] == True]
    def write_data(self, request_id, new_row):
        self.request_data = pd.read_csv(self.resource_requests_file)
        request_index = self.request_data.index[self.request_data['camp_id'] == request_id]
        self.request_data.iloc[request_index, :] = new_row
        self.request_data.to_csv(self.resource_requests_file, index=False)
        return True
    def write_all(self):
        self.request_data = pd.read_csv(self.resource_requests_file)
        self.request_data.loc[self.request_data['Resolved'] == False, 'Resolved'] = True
        self.request_data.to_csv(self.resource_requests_file, index=False)
   
