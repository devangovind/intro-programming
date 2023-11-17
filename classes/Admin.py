# Admin Class File
import csv
import pandas as pd


class Admin:
  # add functions here
  # remember for functions added the first parameter has to be a self
    def create_humanitarian_plan(self):
        pass

    def __init__(self):
        self.login_file = '..file/logindetails.csv'
        self.users = pd.read_csv(self.login_file)

    def save_changes(self):
        self.users.to_csv(self.login_file)

    def activate_account(self, username):
        if username in self.users['Username'].values:
            self.users.loc[self.users['Username'] == username, 'Active'] = True
            self.save_changes()
            return 'Account has been activated'
        else:
            return "Account doesn't exist"

    def deactivate_account(self, username):
        if username in self.users['Username'].values:
            if self.users.loc[self.users['Username'] == username, 'Active'] == True:
                self.users.loc[self.users['Username'] == username, 'Active'] = False
                self.save_changes()
            return "Your account has been deactivated, contact the administator."
        else:
            return "Account doesn't exist"
        
    def delete_account(self, username):
        if username in self.users['Username'].values:
            self.users = self.users[self.users['Username'] == None]
            self.save_changes()
            return 
        else:
            return "Account doesn't exist"