import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# import ttkbootstrap as tb
import csv
import re
from volunteer_gui import VolunteerGui
from Volunteer import Volunteer
from Camps import Camps
import pandas as pd

# these functions are NOT in class because they are used in different classes to validate admin and volunteers

# Filepaths for MAC
# logindetails_filepath = "files\\logindetails.csv"
# camps_filepath = "files\\camps_file.csv"  
# volunteers_filepath = "files\\volunteers.csv" 

# Filepaths for windows
logindetails_filepath = "../files/logindetails.csv"  
camps_filepath = "../files/camps_file.csv"  
volunteers_filepath = "../files/volunteers.csv" 

def user_valid(username, acct_type):
    with open(logindetails_filepath, "r") as file:
        file_reader = csv.reader(file)
        for row in file_reader:
            if username == row[0]:
                # check if account is active first and is of correct account type
                if row[2] == 'TRUE' and row[3] == acct_type:
                    return row
                else:
                    return ""
            else:
                continue
        return ""
    
def password_valid(password, credentials):
    if credentials[1] == password:
        return True
    else:
        return False
    

# class Login for Login page
class Login:
    # Login page configuration
    def __init__(self, master):
        self.root = master
        self.root.geometry("1000x600")
        self.root.title("Welcome to the Humanitarian Management System")

        #each tab is in a notebook and each tab is its own frame
        self.notebook = ttk.Notebook(master)
        self.notebook.pack()

        # Admin Tab
        self.admin_frame = Frame(self.notebook, pady=150, padx=200)
        self.admin_frame.pack(fill="both", expand=1)
        self.notebook.add(self.admin_frame, text="Admin")
        self.admin_caption = Label(self.admin_frame, text="Welcome to the Humanitarian Management System Portal", font=20)
        self.admin_caption.grid(row=0, column=0)
        self.admin_caption2 = Label(self.admin_frame, text="Login as Admin. Please enter your username and password.")
        self.admin_caption2.grid(row=1, column=0, pady=20)

             # Admin - username
        self.admin_username = Label(self.admin_frame, text="Admin Username:")
        self.admin_username.grid(row=2, column=0)
        self.username_entry = Entry(self.admin_frame, width= 30)
        self.username_entry.grid(row=3, column=0)

             # Admin - password
        # style = ttk.Style()
        # style.configure('show_pw', font='underline', bg='grey')
        self.admin_password = Label(self.admin_frame, text="Admin Password:")
        self.admin_password.grid(row=4, column=0)
        self.password_entry = Entry(self.admin_frame, width= 30, show="*")
        self.password_entry.grid(row=5, column=0)
        # Hide/ show pw
        self.password_show_admin = Button(self.admin_frame, text="Show Password", command=self.show_pw)
        self.password_show_admin.grid(row=6, column=0, pady=10)
        self.password_hide_admin = Button(self.admin_frame, text="Hide Password", command=self.hide_pw)
        self.password_hide_admin.grid(row=7, column=0, pady=5)

        self.admin_sign_in = Button(self.admin_frame, text="Sign In", command=self.admin_validate)
        self.admin_sign_in.grid(row=8, column=0, pady=10)

        # Volunteer Tab
        self.volunteer_frame = Frame(self.notebook, pady=150, padx=200)
        self.volunteer_frame.pack(fill="both", expand=1)
        self.notebook.add(self.volunteer_frame, text="Volunteer")
        self.volunteer_caption = Label(self.volunteer_frame, text="Welcome to the Humanitarian Management System Portal", font=20)
        self.volunteer_caption.grid(row=0, column=0)
        self.volunteer_caption2 = Label(self.volunteer_frame, text="Sign in as a Volunteer, or register your details if you do not have an account yet.")
        self.volunteer_caption2.grid(row=1, column=0, pady=20)
        self.volunteer_sign_in = Button(self.volunteer_frame, text="Sign In", command=self.volunteer_login_page, width=20)
        self.volunteer_sign_in.grid(row=2, column=0, pady=10)
        self.volunteer_register = Button(self.volunteer_frame, text="Register as Volunteer", command=self.volunteer_register_page, width=20)
        self.volunteer_register.grid(row=3, column=0, pady=10)

    def show_pw(self):
        self.password_entry.configure(show='')
        
    def hide_pw(self):
        self.password_entry.configure(show='*')
         
    # Validate if admin username and pw is correct
    def admin_validate(self):
        user_type = 'Admin'
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
        if entered_username != "" and entered_password != "":
            if user_valid(entered_username, user_type) != "":
                correct_credentials = user_valid(entered_username, user_type) 
                if password_valid(entered_password, correct_credentials): # shows admin menu if login is valid
                    Admin_Menu()
                else:
                    messagebox.showerror("Error", "Password is incorrect!")
            else:
                messagebox.showerror("Error", "Username is invalid or User is inactive!")
        else:
            messagebox.showerror("Error", "You have not entered a username or password!")

    # display volunteer log in window
    def volunteer_login_page(self):
        self.log_in_window = Toplevel()
        self.log_in_window.geometry("500x275+300+300")
        self.log_in_window.resizable(False, False)
        self.log_in_window.title("Login to your Volunteer account")
        self.caption = Label(self.log_in_window, text="Login as Volunteer. Please enter your username and password.")
        self.caption.pack(pady=10)
        self.username = Label(self.log_in_window, text="Volunteer Username:")
        self.username.pack()
        self.username_entry = Entry(self.log_in_window, width= 30)
        self.username_entry.pack()
        self.password = Label(self.log_in_window, text="Volunteer Password:")
        self.password.pack()
        self.password_entry = Entry(self.log_in_window, width= 30, show='*')
        self.password_entry.pack()

        self.password_show_volunteer = Button(self.log_in_window, text="Show Password", command=self.show_pw)
        self.password_show_volunteer.pack(pady=10)
        self.password_hide_volunteer = Button(self.log_in_window, text="Hide Password", command=self.hide_pw)
        self.password_hide_volunteer.pack(pady=5)

        sign_in = Button(self.log_in_window, text="Sign In", command= self.volunteer_validate)
        sign_in.pack(pady=20)

    # Validate if volunteer username and pw is correct
    def volunteer_validate(self): 
        user_type = "Volunteer"
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
        if entered_username != "" and entered_password != "":
            if user_valid(entered_username, user_type) != "":
                correct_credentials = user_valid(entered_username, user_type) 
                if password_valid(entered_password, correct_credentials): 
                    #if login is valid, display volunteer menu
                    self.log_in_window.destroy() #destroys volunteer login pop up
                    self.root.iconify() #minimises general login GUI when sign in successful
                    create_volunteer = Volunteer(entered_username)
                    VolunteerGui(create_volunteer, self.root)
                else:
                    messagebox.showerror("Error", "Password is incorrect!")
                    self.log_in_window.lift()
            else:
                messagebox.showerror("Error", "Username is invalid or User is inactive!")
                self.log_in_window.lift()
        else:
            messagebox.showerror("Error", "You have not entered a username or password!")
            self.log_in_window.lift()

    # display volunteer registration window
    def volunteer_register_page(self):
        Volunteer_Register()

# class Admin_Menu for Admin page after successful login
class Admin_Menu:
    # Yan's portion
    def __init__(self):
        print("Test admin sign in button")
    
# class Volunteer_Register for volunteer registration page when they select register
class Volunteer_Register: 
    def __init__(self):
        self.register_window = tk.Tk()
        self.register_window.geometry("1000x500")
        self.register_window.title("Volunteer Registration")

        # Create a Main Frame
        main_frame = Frame(self.register_window)
        main_frame.pack(fill="both", expand=1)

        # Create a Canvas
        my_canvas = Canvas(main_frame)
        my_canvas.pack(side=LEFT, fill="both", expand=1)

        # Add scrollbar to canvas
        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        # configure the canvas
        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=(0,0,900,900)))
        
        # create another frame inside the canvas
        second_frame = Frame(my_canvas)

        # add that new frame to a window in the canvas
        my_canvas.create_window((100,50),window=second_frame, anchor="nw")

        self.username_label = tk.Label(second_frame, text = "Username:\nYour username should be between 8 and 16 characters long and only consist of letters a-z and numbers 0-9")
        self.username_entry = tk.Entry(second_frame, validate="key", validatecommand=(self.register_window.register(self.validate_username_entry), "%P"))
        self.username_status = tk.Label(second_frame, text="")

        self.first_name_label = tk.Label(second_frame, text = "First Name:\nYour first name should be between 0 and 20 letters long and the first letter should be capitalized ")
        self.first_name_entry = tk.Entry(second_frame, validate="key", validatecommand=(self.register_window.register(self.validate_first_name_entry), "%P"))
        self.first_name_status = tk.Label(second_frame, text="")

        self.last_name_label = tk.Label(second_frame, text = "Last Name:\nYour last name should be between 0 and 20 letters long and the first letter should be capitalized")
        self.last_name_entry = tk.Entry(second_frame, validate="key", validatecommand=(self.register_window.register(self.validate_last_name_entry), "%P"))
        self.last_name_status = tk.Label(second_frame, text="")

        self.phone_label = tk.Label(second_frame, text = "Phone Number:\nYour phone should be between 6 and 15 numbers long")
        self.phone_entry = tk.Entry(second_frame, validate="key", validatecommand=(self.register_window.register(self.validate_phone_entry), "%P"))
        self.phone_status = tk.Label(second_frame, text="")

        self.age_label = tk.Label(second_frame, text = "Age:\nYour age should be numbers between 0 and 140")
        self.age_entry = tk.Entry(second_frame, validate="key", validatecommand=(self.register_window.register(self.validate_age_entry), "%P"))
        self.age_status = tk.Label(second_frame, text="")

        self.camp_id_label = tk.Label(second_frame, text = "Camp_ID:\nChoose your Camp ID")
        self.camp_id_values = self.read_camp_id_values_from_csv()  
        self.selected_camp_id = tk.StringVar()
        self.selected_camp_id.set('')
        self.camp_id_dropdown = ttk.Combobox(second_frame, textvariable=self.selected_camp_id, values=self.camp_id_values)

        self.availability_label = tk.Label(second_frame, text="\nAvailability:")
        self.mon_var = tk.IntVar(value=0)
        self.tue_var = tk.IntVar(value=0)
        self.wed_var = tk.IntVar(value=0)
        self.thu_var = tk.IntVar(value=0)
        self.fri_var = tk.IntVar(value=0)
        self.sat_var = tk.IntVar(value=0)
        self.sun_var = tk.IntVar(value=0)
        self.availability_variables = [self.mon_var, self.tue_var, self.wed_var, self.thu_var, self.fri_var, self.sat_var, self.sun_var]
        mon_box = tk.Checkbutton(second_frame, text="Monday", variable=self.mon_var, command=lambda: self.mon_var.set(1) if self.mon_var.get() == False else self.mon_var.set(0))
        tue_box = tk.Checkbutton(second_frame, text="Tuesday", variable=self.tue_var, command=lambda: self.tue_var.set(1) if self.tue_var.get() == False else self.tue_var.set(0))
        wed_box = tk.Checkbutton(second_frame, text="Wednesday", variable=self.wed_var, command=lambda: self.wed_var.set(1) if self.wed_var.get() == False else self.wed_var.set(0))
        thu_box = tk.Checkbutton(second_frame, text="Thursday", variable=self.thu_var, command=lambda: self.thu_var.set(1) if self.thu_var.get() == False else self.thu_var.set(0))
        fri_box = tk.Checkbutton(second_frame, text="Friday", variable=self.fri_var, command=lambda: self.fri_var.set(1) if self.fri_var.get() == False else self.fri_var.set(0))
        sat_box = tk.Checkbutton(second_frame, text="Saturday", variable=self.sat_var, command=lambda: self.sat_var.set(1) if self.sat_var.get() == False else self.sat_var.set(0))
        sun_box = tk.Checkbutton(second_frame, text="Sunday", variable=self.sun_var, command=lambda: self.sun_var.set(1) if self.sun_var.get() == False else self.sun_var.set(0))
        self.availability_checkboxes = [
            mon_box, tue_box, wed_box, thu_box, fri_box, sat_box, sun_box ]
    
        self.password_label = tk.Label(second_frame, text = "\nPassword:\nYour password should contain at least one capital letter, at least one of '?' or '!', letters a-z and numbers 0-9 and be between 8 and 16 characters long")
        self.password_entry = tk.Entry(second_frame, show = "*",validate="key", validatecommand=(self.register_window.register(self.validate_password_entry), "%P"))
        self.password_status = tk.Label(second_frame, text="")

        self.confirm_password_label = tk.Label(second_frame, text="Confirm your password:")
        self.confirm_password_entry = tk.Entry(second_frame, show="*", validate="key", validatecommand=(self.register_window.register(self.validate_confirm_password_entry), "%P"))
        self.confirm_password_status = tk.Label(second_frame, text="")

        self.register_button = tk.Button(second_frame, text = "Register", command=self.register)

        self.username_label.pack()
        self.username_entry.pack()
        self.username_status.pack()

        self.first_name_label.pack()
        self.first_name_entry.pack()
        self.first_name_status.pack()

        self.last_name_label.pack()
        self.last_name_entry.pack()
        self.last_name_status.pack()

        self.phone_label.pack()
        self.phone_entry.pack()
        self.phone_status.pack()

        self.age_label.pack()
        self.age_entry.pack()
        self.age_status.pack() 

        self.camp_id_label.pack()
        self.camp_id_dropdown.pack()


        self.availability_label.pack()
        for checkbox in self.availability_checkboxes:
            checkbox.pack()
        # self.avail_status.pack()

        self.password_label.pack()
        self.password_entry.pack()
        self.password_status.pack()

        self.confirm_password_label.pack()
        self.confirm_password_entry.pack()
        self.confirm_password_status.pack()

        self.register_button.pack()
        
        self.register_window.mainloop()

    def register (self):
        username = self.username_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        age = self.age_entry.get()
        camp_id = str(self.camp_id_dropdown.get())
        availability_var = self.availability_variables
        print(availability_var)
        availability_bin = ""
        for var in availability_var:
            print(var.get())
            if var.get():
                availability_bin += "1"
            else:
                availability_bin += "0"
        print(availability_bin)
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

            with open (logindetails_filepath, "a") as file:
                file.write(f"{username},{password},{True},{account_type}\n")

            with open (volunteers_filepath, "a") as file:
                file.write(f"{username},{first_name},{last_name},{phone},{age},{camp_id},{availability_bin}\n")

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
        with open(logindetails_filepath, "r") as file:
            file_reader = csv.reader(file)
            next(file_reader)
            for row in file_reader:
                if username == row[0]:
                    raise ValueError("This username already exists. Please try an alternative username.")
                else:
                    continue
            
        if " " in username:
            raise ValueError("Do not enter spaces in your username.")
        elif len(username) < 8 or len(username) > 16:
            raise ValueError("Please ensure that your username is between 8 and 16 characters long.")
        elif username.isalnum() == False:
            raise ValueError("Please ensure that your username contains only numbers and letters.")
    
    def validate_first_name(self, first_name):
        alphabet = "^[a-zA-Z\s]+$"
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
        alphabet = "^[a-zA-Z\s]+$"
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
            with open(camps_filepath, "r") as file:
                reader = csv.reader(file)
                next(reader)  
                for row in reader:
                    camp_id_values.append(row[0])  
        except FileNotFoundError:
            messagebox.showerror("Error", "Camp ID CSV file not found.")
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
            raise ValueError("Please ensure that your password contains only letters a-z, numbers 0-9, and at least one of '!' or '?'.")
    
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