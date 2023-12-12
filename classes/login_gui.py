import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# import ttkbootstrap as tb
import csv
import re
from volunteer_gui import VolunteerGui
from Volunteer import Volunteer
from Admin_gui import AdminGui
from Admin import Admin
from Camps import Camps
import pandas as pd
import os
import sys
from FileManager import FileManager

# these functions are NOT in class because they are used in different classes to validate admin and volunteers

# Filepaths for MAC
# logindetails_filepath = "files\\logindetails.csv"
# camps_filepath = "files\\camps_file.csv"  
# volunteers_filepath = "files\\volunteers.csv" 

# Filepaths for windows
# logindetails_filepath = "../files/logindetails.csv"  
# camps_filepath = "../files/camps_file.csv"  
# volunteers_filepath = "../files/volunteers.csv" 

# logindetails_filepath = "logindetails.csv"  
# camps_filepath = "camps_file.csv"  
# volunteers_filepath = "volunteers.csv" 
csv_manager = FileManager()
logindetails_filepath = csv_manager.get_file_path("logindetails.csv")
camps_filepath = csv_manager.get_file_path("camps_file.csv")  
volunteers_filepath = csv_manager.get_file_path("volunteers.csv")


# print("Current working directory:", os.getcwd())
# print("sys._MEIPASS:", sys._MEIPASS)


# csv_path = os.path.join(sys._MEIPASS, logindetails_filepath)

# print("Constructed CSV path:", csv_path)


def user_valid(username, acct_type):
    login_details = pd.read_csv(logindetails_filepath)
    matching_row = login_details.loc[(login_details['Username'] == username)]

    if not matching_row.empty:
        if matching_row["Active"].iloc[0] == False:
            return "Account Inactive"
        elif matching_row["Active"].iloc[0] == True and matching_row["Account Type"].iloc[0] == acct_type:
            return matching_row.values.tolist()[0]
        else:
            return ""
    else:
        return "Account does not exist"

    
def password_valid(password, credentials):
    if str(credentials[1]) == password:
        return True
    else:
        return False
    

# class Login for Login page
class Login:
    # Login page configuration
    def __init__(self, master):
        self.root = master
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.minsize(1000,600)


        width_to_use = int(0.85*screen_width)
        height_to_use = int(0.9*screen_height)
        positioning_width = int(0.05*screen_width)
        positioning_height = int(0.01*screen_width)
        self.root.geometry(f"{width_to_use}x{height_to_use}+{positioning_width}+{positioning_height}")
        self.root.title("Welcome to the Humanitarian Management System")
        


        #each tab is in a notebook and each tab is its own frame
        self.notebook = ttk.Notebook(master)
        self.notebook.pack()

        # Admin Tab
        self.admin_frame = Frame(self.notebook, pady=150, padx=200)
        self.admin_frame.pack(fill="both", expand=1)
        self.notebook.add(self.admin_frame, text="Admin")
        self.admin_caption = Label(self.admin_frame, text="Welcome to the Humanitarian Management System Portal", font=("Arial",16))
        self.admin_caption.config(fg="medium slate blue")
        self.admin_caption.pack()
        self.admin_caption2 = Label(self.admin_frame, text="Sign in as Admin. Please enter your username and password.", font=("Arial",14))
        self.admin_caption2.pack(pady=5)

             # Admin - username
        self.admin_username = Label(self.admin_frame, text="Admin Username:", font=("Arial",14))
        self.admin_username.pack()
        self.username_entry = ttk.Entry(self.admin_frame, width= 30)
        self.username_entry.pack()

             # Admin - password
        # style = ttk.Style()
        # style.configure('show_pw', font='underline', bg='grey')
        self.admin_password = Label(self.admin_frame, text="Admin Password:", font=("Arial",14))
        self.admin_password.pack()
        self.password_entry = ttk.Entry(self.admin_frame, width= 30, show="*")
        self.password_entry.pack()
        # Hide/ show pw
        self.password_show_admin = ttk.Button(self.admin_frame, text="Show Password", command=self.show_pw)
        self.password_show_admin.pack(pady=5)
        self.password_hide_admin = ttk.Button(self.admin_frame, text="Hide Password", command=self.hide_pw)
        self.password_hide_admin.pack(pady=5)

        self.admin_sign_in = ttk.Button(self.admin_frame, text="Sign In", command=self.admin_validate)
        self.admin_sign_in.pack(pady=5)

        # Volunteer Tab
        self.volunteer_frame = Frame(self.notebook, pady=150, padx=200)
        self.volunteer_frame.pack(fill="both", expand=1)
        self.notebook.add(self.volunteer_frame, text="Volunteer")
        self.volunteer_caption = Label(self.volunteer_frame, text="Welcome to the Humanitarian Management System Portal", font=("Arial",16))
        self.volunteer_caption.config(fg="medium slate blue")
        self.volunteer_caption.pack()
        self.volunteer_caption2 = Label(self.volunteer_frame, text="Sign in as a Volunteer, or register your details if you do not have an account yet.", font=("Arial",14))
        self.volunteer_caption2.pack(pady=5)

        self.vol_username = Label(self.volunteer_frame, text="Volunteer Username:", font=("Arial",14))
        self.vol_username.pack()
        self.vol_username_entry = ttk.Entry(self.volunteer_frame, width= 30)
        self.vol_username_entry.pack()
        self.vol_password = Label(self.volunteer_frame, text="Volunteer Password:", font=("Arial",14))
        self.vol_password.pack()
        self.vol_password_entry = ttk.Entry(self.volunteer_frame, width= 30, show='*')
        self.vol_password_entry.pack()

        self.password_show_volunteer = ttk.Button(self.volunteer_frame, text="Show Password", command=self.show_pw)
        self.password_show_volunteer.pack(pady=5)
        self.password_hide_volunteer = ttk.Button(self.volunteer_frame, text="Hide Password", command=self.hide_pw)
        self.password_hide_volunteer.pack(pady=5)

        vol_sign_in = ttk.Button(self.volunteer_frame, text="Sign In", command= self.volunteer_validate)
        vol_sign_in.pack(pady=5)

        # self.volunteer_sign_in = ttk.Button(self.volunteer_frame, text="Sign In", command=self.volunteer_login_page, width=20)
        # self.volunteer_sign_in.pack(pady=10)
        self.volunteer_register = ttk.Button(self.volunteer_frame, text="Register as Volunteer", command=self.volunteer_register_page, width=20)
        self.volunteer_register.pack(pady=5)


    def show_pw(self):
        self.password_entry.configure(show='')
        self.vol_password_entry.configure(show='')
        
    def hide_pw(self):
        self.password_entry.configure(show='*')
        self.vol_password_entry.configure(show='*')
         
    # Validate if admin username and pw is correct
    def admin_validate(self):
        user_type = 'Admin'
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if entered_username != "" and entered_password != "":

            if user_valid(entered_username, user_type) == "Account Inactive":
                messagebox.showerror("Error", "User is inactive! Your account has been deactivated, contact the administrator!")
            elif user_valid(entered_username, user_type) == "Account does not exist":
                messagebox.showerror("Error", "Account doesn't exist!")
            elif user_valid(entered_username, user_type) != "":
                correct_credentials = user_valid(entered_username, user_type) 
                if password_valid(entered_password, correct_credentials): # shows admin menu if login is valid
                    # Admin_Menu()
                    # self.root.iconify() #minimises general login GUI when sign in successful
                    self.username_entry.delete(0, tk.END)
                    self.password_entry.delete(0, tk.END)
                    
                    self.root.iconify()
                    create_admin = Admin(entered_username)
                    AdminGui(create_admin, self.root)
                    # self.root.withdraw()
                else:
                    messagebox.showerror("Error", "Password is incorrect!")
            else:
                messagebox.showerror("Error", "Username is invalid!")
        else:
            messagebox.showerror("Error", "You have not entered a username or password!")


    # Validate if volunteer username and pw is correct
    def volunteer_validate(self): 
        user_type = "Volunteer"

        entered_username = self.vol_username_entry.get()
        entered_password = self.vol_password_entry.get()
        if entered_username != "" and entered_password != "":

            if user_valid(entered_username, user_type) == "Account Inactive":
                messagebox.showerror("Error", "User is inactive! Your account has been deactivated, contact the administrator!")
            elif user_valid(entered_username, user_type) == "Account does not exist":
                messagebox.showerror("Error", "Account doesn't exist!")
            elif user_valid(entered_username, user_type) != "":
                correct_credentials = user_valid(entered_username, user_type) 
                if password_valid(entered_password, correct_credentials): 
                    #if login is valid, display volunteer menu
                    # self.log_in_window.destroy() #destroys volunteer login pop up
                    self.vol_username_entry.delete(0, tk.END)
                    self.vol_password_entry.delete(0, tk.END)
                    self.root.iconify() #minimises general login GUI when sign in successful

                    create_volunteer = Volunteer(entered_username)
                    VolunteerGui(create_volunteer, self.root)
                else:
                    messagebox.showerror("Error", "Password is incorrect!")
                    
            else:
                messagebox.showerror("Error", "Username is invalid!")
                
        else:
            messagebox.showerror("Error", "You have not entered a username or password!")
            

    # display volunteer registration window
    def volunteer_register_page(self):
        Volunteer_Register()

    
# class Volunteer_Register for volunteer registration page when they select register
class Volunteer_Register: 
    def __init__(self):
        self.register_window = tk.Tk()
        self.register_window.geometry("1000x700")
        self.register_window.title("Volunteer Registration")
        self.camps = Camps()
        self.register_window.minsize(1000, 700)
        self.register_window.columnconfigure(0, weight=1, minsize=500)
        self.register_window.columnconfigure(1, weight=1, minsize=500)
        self.register_label= tk.Label(self.register_window, text = "Register as a Volunteer", fg="medium slate blue", font=('Arial', 18))
        self.username_label = tk.Label(self.register_window, text = "Username:\nYour username should be between 8 and 16 characters long\nand only consist of letters a-z and numbers 0-9")
        self.username_entry = ttk.Entry(self.register_window, validate="key", validatecommand=(self.register_window.register(self.validate_username_entry), "%P"))
        self.username_status = tk.Label(self.register_window, text="")
        self.first_name_label = tk.Label(self.register_window, text = "First Name:\nYour first name should be between 0 and 20 letters long\nand the first letter should be capitalized ")
        self.first_name_entry = ttk.Entry(self.register_window, validate="key", validatecommand=(self.register_window.register(self.validate_first_name_entry), "%P"))
        self.first_name_status = tk.Label(self.register_window, text="")
        self.last_name_label = tk.Label(self.register_window, text = "Last Name:\nYour last name should be between 0 and 20 letters long\nand the first letter should be capitalized")
        self.last_name_entry = ttk.Entry(self.register_window, validate="key", validatecommand=(self.register_window.register(self.validate_last_name_entry), "%P"))
        self.last_name_status = tk.Label(self.register_window, text="")
        self.phone_label = tk.Label(self.register_window, text = "Phone Number:\nYour phone number should be between 6 and 15 numbers long")
        self.phone_entry = ttk.Entry(self.register_window, validate="key", validatecommand=(self.register_window.register(self.validate_phone_entry), "%P"))
        self.phone_status = tk.Label(self.register_window, text="")
        self.age_label = tk.Label(self.register_window, text = "Age:\nYour age should be a number between 0 and 140")
        self.age_entry = ttk.Entry(self.register_window, validate="key", validatecommand=(self.register_window.register(self.validate_age_entry), "%P"))
        self.age_status = tk.Label(self.register_window, text="")
        self.camp_id_label = tk.Label(self.register_window, text = "Camp_ID:\nChoose your Camp ID")
        self.camp_id_values = self.read_camp_id_values_from_csv()  
        self.selected_camp_id = tk.StringVar()
        self.selected_camp_id.set('')
        self.camp_id_dropdown = ttk.Combobox(self.register_window, textvariable=self.selected_camp_id, values=self.camp_id_values)
        self.camp_id_dropdown.config(state="readonly")

        self.availability_label = tk.Label(self.register_window, text="\nAvailability:")
        availability_frame = Frame(self.register_window)
        self.mon_var = tk.IntVar(value=0)
        self.tue_var = tk.IntVar(value=0)
        self.wed_var = tk.IntVar(value=0)
        self.thu_var = tk.IntVar(value=0)
        self.fri_var = tk.IntVar(value=0)
        self.sat_var = tk.IntVar(value=0)
        self.sun_var = tk.IntVar(value=0)
        self.availability_variables = [self.mon_var, self.tue_var, self.wed_var, self.thu_var, self.fri_var, self.sat_var, self.sun_var]
        mon_box = tk.Checkbutton(availability_frame, text="Monday", variable=self.mon_var, command=lambda: self.mon_var.set(1) if self.mon_var.get() == False else self.mon_var.set(0))
        tue_box = tk.Checkbutton(availability_frame, text="Tuesday", variable=self.tue_var, command=lambda: self.tue_var.set(1) if self.tue_var.get() == False else self.tue_var.set(0))
        wed_box = tk.Checkbutton(availability_frame, text="Wednesday", variable=self.wed_var, command=lambda: self.wed_var.set(1) if self.wed_var.get() == False else self.wed_var.set(0))
        thu_box = tk.Checkbutton(availability_frame, text="Thursday", variable=self.thu_var, command=lambda: self.thu_var.set(1) if self.thu_var.get() == False else self.thu_var.set(0))
        fri_box = tk.Checkbutton(availability_frame, text="Friday", variable=self.fri_var, command=lambda: self.fri_var.set(1) if self.fri_var.get() == False else self.fri_var.set(0))
        sat_box = tk.Checkbutton(availability_frame, text="Saturday", variable=self.sat_var, command=lambda: self.sat_var.set(1) if self.sat_var.get() == False else self.sat_var.set(0))
        sun_box = tk.Checkbutton(availability_frame, text="Sunday", variable=self.sun_var, command=lambda: self.sun_var.set(1) if self.sun_var.get() == False else self.sun_var.set(0))
        mon_box.grid(row=0, column=0, sticky='w')
        tue_box.grid(row=0, column=1, sticky='w')
        wed_box.grid(row=0, column=2, sticky='w')
        thu_box.grid(row=0, column=3, sticky='w')
        fri_box.grid(row=1, column=0, sticky='w')
        sat_box.grid(row=1, column=1, sticky='w')
        sun_box.grid(row=1, column=2, sticky='w')
        self.availability_checkboxes = [
            mon_box, tue_box, wed_box, thu_box, fri_box, sat_box, sun_box ]
        
        self.password_label = tk.Label(self.register_window, text = "Password:\nYour password should contain at least one capital letter,\nat least one of '?' or '!', letters a-z and numbers 0-9\nand be between 8 and 16 characters long", anchor="w")
        self.password_entry = ttk.Entry(self.register_window, show = "*",validate="key", validatecommand=(self.register_window.register(self.validate_password_entry), "%P"))
        
        self.password_entry.bind("<KeyRelease>", self.on_password_change) 
        self.password_status = tk.Label(self.register_window, text="")
        self.confirm_password_label = tk.Label(self.register_window, text="Confirm your password:")
        self.confirm_password_entry = ttk.Entry(self.register_window, show="*", validate="key", validatecommand=(self.register_window.register(self.validate_confirm_password_entry), "%P"))
        self.confirm_password_status = tk.Label(self.register_window, text="")
        self.register_button = ttk.Button(self.register_window, text = "Register", command=self.register)
        self.register_label.grid(row=0, column=0, columnspan=2)
        self.username_label.grid(row=1, column=0, sticky="nsew")
        self.username_entry.grid(row=2, column=0)
        self.username_status.grid(row=3, column=0, sticky="nsew")
        
        self.first_name_label.grid(row=4, column=0)
        self.first_name_entry.grid(row=5, column=0)
        self.first_name_status.grid(row=6, column=0)

        self.last_name_label.grid(row=7, column=0)
        self.last_name_entry.grid(row=8, column=0)
        self.last_name_status.grid(row=9, column=0)

        self.phone_label.grid(row=10, column=0, padx=10)
        self.phone_entry.grid(row=11, column=0)
        self.phone_status.grid(row=12, column=0)

        self.age_label.grid(row=7, column=1)
        self.age_entry.grid(row=8, column=1)
        self.age_status.grid(row=9, column=1)

        self.camp_id_label.grid(row=10, column=1)
        self.camp_id_dropdown.grid(row=11, column=1)


        self.availability_label.grid(row=12, column=0, columnspan=2)
        availability_frame.grid(row=13, column=0, columnspan=2,pady=5)

        self.password_label.grid(row=1, column=1)
        self.password_entry.grid(row=2, column=1)
        self.password_status.grid(row=3, column=1)

        self.confirm_password_label.grid(row=4, column=1)
        self.confirm_password_entry.grid(row=5, column=1)
        self.confirm_password_status.grid(row=6, column=1)

        self.register_button.grid(row=22, column=0, columnspan=2, pady=10)
        
        self.register_window.mainloop()

    def register(self):

        username = self.username_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        age = self.age_entry.get()
        camp_id = str(self.camp_id_dropdown.get())
        availability_var = self.availability_variables

        availability_bin = ""
        for var in availability_var:

            if var.get():
                availability_bin += "1"
            else:
                availability_bin += "0"

        password = self.password_entry.get()
        account_type = "Volunteer"

        try:
            self.validate_username(username)
            self.validate_first_name(first_name)
            self.validate_last_name(last_name)
            self.validate_phone(phone)
            self.validate_age(age)
            self.validate_availability(availability_bin) 
            self.validate_password(password)

   
            new_row_login = pd.DataFrame({'Username': [username], 'Password': [password], 'Active': [True], 'Account Type': [account_type]})
            new_row_login.to_csv(logindetails_filepath, mode="a", header=False, index=False)

            new_row_volun = pd.DataFrame({"Username": [username], "First Name": [first_name], "Last Name": [last_name], "Phone": [phone], "Age": [age], "CampID": [camp_id], "Availability": [availability_bin]})
            new_row_volun.to_csv(volunteers_filepath, mode="a", header=False, index=False)
            # update camps_file.csv
            self.camp_df = pd.read_csv(camps_filepath)
            self.camp_data = self.camp_df[self.camp_df['Camp_ID'] == camp_id].copy()
            self.camp_index = self.camp_data.index
            self.camp_data['Num_Of_Volunteers'] += 1
            self.camp_df.iloc[self.camp_index, :] = self.camp_data
            self.camp_df.to_csv(camps_filepath, index=False)
        
            messagebox.showinfo("Success", "Registration successful!")
            self.register_window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.register_window.lift()

    def validate_username(self, username):
        login_details = pd.read_csv(logindetails_filepath)
        matching_row = login_details.loc[(login_details['Username'] == username)]
        if not matching_row.empty:
            raise ValueError("This username already exists. Please try an alternative username.")
            
        if " " in username:
            raise ValueError("Do not enter spaces in your username.")
        elif len(username) < 8 or len(username) > 16:
            raise ValueError("Please ensure that your username is between 8 and 16 characters long.")
        elif username.isalnum() == False:
            raise ValueError("Please ensure that your username contains only numbers and letters.")
    
    def validate_first_name(self, first_name):
        alphabet = r"^[a-zA-Z\s]+$"
        if not bool(re.match(alphabet,first_name)):
                raise ValueError ("Name can only be letters")
        elif " " in first_name:
                raise ValueError ("Do not enter spaces in name")
        
        first_name_stripped = first_name.strip()
        first_letter = first_name_stripped[0]

        if len(first_name)>20 or len(first_name) <=0:
            raise ValueError ("Name has to be between 0-20 letters")
        elif not first_letter.isupper():
            raise ValueError("The first letter of the name should be capitalized")
        elif not first_name_stripped.istitle():
            raise ValueError("Only the first letter of the name should be capitalized")
                

    def validate_last_name(self, last_name):
        alphabet = r"^[a-zA-Z\s]+$"
        if not bool(re.match(alphabet, last_name)):
            raise ValueError ("Name can only be letters")
        elif " " in last_name:
            raise ValueError ("Do not enter spaces in name")
        
        last_name_stripped = last_name.strip()
        first_letter = last_name_stripped[0]

        if len(last_name)>20 or len(last_name) <=0:
            raise ValueError    ("Name has to be between 0-20 letters")
        elif not first_letter.isupper():
            raise ValueError("The first letter of the name should be capitalized")
        elif not last_name_stripped.istitle():
            raise ValueError("Only the first letter of the name should be capitalized")

    def validate_phone(self, phone):
        if phone.isdigit():
            if 6>len(phone) or len(phone)>15:
                raise ValueError("Phone number must be between 6-15 digits")
        elif " " in phone:
            raise ValueError ("Do not enter spaces in phone")
        else:
            raise ValueError ("Phone number must be only numbers")

    def validate_age(self, age):
        if age.isdigit():
            if int(age) > 140:
                raise ValueError ("Age too high")
            elif int(age) <= 0:
                raise ValueError ("Age must be positive")
        elif " " in age:
            raise ValueError ("Do not enter spaces in age")
        else:
            raise ValueError ("Age must be number")
    
    def validate_availability(self, availability_bin):
        if availability_bin == "0000000":
            raise ValueError("Please select at least one day of the week.")

    def read_camp_id_values_from_csv(self):
        camp_id_values = []
        try:
            camp_id_values = self.camps.valid_camps_ids()
        except FileNotFoundError:
            messagebox.showerror("Error", "Camps file not found.")
        return camp_id_values

    def validate_password(self, password):
        pw_chars = r'^[A-Za-z0-9!?]+$'
        punc_chars = r'[!?]'
        if " " in password:
            raise ValueError("Do not enter spaces in your password.")
        elif len(password) < 8 or len(password) > 16:
            raise ValueError("Please ensure that your password is between 8 and 16 characters long.")
        elif not any(c.isupper() for c in password):
            raise ValueError("Please ensure that your password contains at least one capital letter.")
        elif not re.match(pw_chars, password) or not re.search(punc_chars, password):
            raise ValueError("Please ensure that your password contains only letters a-z,\nnumbers 0-9, and at least one of '!' or '?'.")
    
    def validate_confirm_password(self, password, confirm_password):
        if password != confirm_password:
            raise ValueError("Passwords do not match. Please enter the same password in both fields.")
    
    def validate_username_entry(self, value):
        try:
            self.validate_username(value)
            self.username_status.config(text="Username is valid", fg="green")
        except ValueError as e:
            self.username_status.config(text=str(e), fg="red")
        return True
    
    def validate_first_name_entry(self, value):
        try:
            self.validate_first_name(value)
            self.first_name_status.config(text="First Name is valid", fg="green")
        except ValueError as e:
            self.first_name_status.config(text=str(e), fg="red")
        return True
    
    def validate_last_name_entry(self, value):
        try:
            self.validate_last_name(value)
            self.last_name_status.config(text="Last Name is valid", fg="green")
        except ValueError as e:
            self.last_name_status.config(text=str(e), fg="red")
        return True
    
    def validate_phone_entry(self, value):
        try:
            self.validate_phone(value)
            self.phone_status.config(text="Phone number is valid", fg="green")
        except ValueError as e:
            self.phone_status.config(text=str(e), fg="red")
        return True
    
    def validate_age_entry(self, value):
        try:
            self.validate_age(value)
            self.age_status.config(text="Age is valid", fg="green")
        except ValueError as e:
            self.age_status.config(text=str(e), fg="red")
        return True

    def validate_password_entry(self, value):
        try:
            self.validate_password(value)
            self.password_status.config(text="Password is valid", fg="green")
        except ValueError as e:
            self.password_status.config(text=str(e), fg="red")
        return True
    
    def on_password_change(self, *args):
        self.validate_confirm_password_entry(self.confirm_password_entry.get())
    
    def validate_confirm_password_entry(self, value):
        try:
            password = self.password_entry.get()
            self.validate_confirm_password(password, value)
            self.confirm_password_status.config(text="Passwords match", fg="green")
        except ValueError as e:
            self.confirm_password_status.config(text=str(e), fg="red")
        return True


if __name__ == '__main__':
    root = Tk()
    login_menu = Login(root)
    root.mainloop()
