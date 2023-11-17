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
        self.volunteer_account = None

    def activate_account(self, volunteer):
        users = pd.read_csv(self.login_file)
        for volunteer in users:
            pass
        return self.volunteer_account == True

    def deactivate_account(self):
        if self.volunteer_account == False:
            return print("Your account has been deactivated, contact the administator.")
        pass

    def delete_account(self):
        if self.volunteer == None:
            print("Account doesn't exist")
        pass