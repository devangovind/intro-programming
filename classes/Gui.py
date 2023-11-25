import tkinter as tk
from tkinter import ttk, messagebox
import csv
import re

class UserRegistration:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("User Registration")

        self.username_label = tk.Label(self.root, text = "Username:\nYour username should be between 8 and 16 characters long and only consist of letters a-z and numbers 0-9")
        self.username_entry = tk.Entry(self.root, validate="key", validatecommand=(self.root.register(self.validate_username_entry), "%P"))
        self.username_status = tk.Label(self.root, text="")

        self.first_name_label = tk.Label(self.root, text = "First Name:\nYour first name should be between 0 and 20 letters long and the first letter should be capitalized ")
        self.first_name_entry = tk.Entry(self.root, validate="key", validatecommand=(self.root.register(self.validate_first_name_entry), "%P"))
        self.first_name_status = tk.Label(self.root, text="")

        self.last_name_label = tk.Label(self.root, text = "Last Name:\nYour last name should be between 0 and 20 letters long and the first letter should be capitalized")
        self.last_name_entry = tk.Entry(self.root, validate="key", validatecommand=(self.root.register(self.validate_last_name_entry), "%P"))
        self.last_name_status = tk.Label(self.root, text="")

        self.phone_label = tk.Label(self.root, text = "Phone:\nYour phone should be between 6 and 15 numbers long")
        self.phone_entry = tk.Entry(self.root, validate="key", validatecommand=(self.root.register(self.validate_phone_entry), "%P"))
        self.phone_status = tk.Label(self.root, text="")

        self.age_label = tk.Label(self.root, text = "Age:\nYour age should be numbers between 0 and 140")
        self.age_entry = tk.Entry(self.root, validate="key", validatecommand=(self.root.register(self.validate_age_entry), "%P"))
        self.age_status = tk.Label(self.root, text="")

        self.camp_id_label = tk.Label(self.root, text = "Camp_ID:\nChoose you Camp ID")
        self.camp_id_values = self.read_camp_id_values_from_csv()  
        self.selected_camp_id = tk.StringVar()
        self.camp_id_dropdown = ttk.Combobox(self.root, textvariable=self.selected_camp_id, values=self.camp_id_values)

        self.availability_label = tk.Label(self.root, text = "\nAvailability:\nSet 0000000 to the default value")
        self.availability_entry = tk.Entry(self.root)
        self.availability_entry.insert(0, "0000000")

    
        self.password_label = tk.Label(self.root, text = "\nPassword:\nYour password should contain at least one capital letter, at least one of '?' or '!', letters a-z and numbers 0-9 and be between 8 and 16 characters long")
        self.password_entry = tk.Entry(self.root, show = "*",validate="key", validatecommand=(self.root.register(self.validate_password_entry), "%P"))
        self.password_status = tk.Label(self.root, text="")

        self.confirm_password_label = tk.Label(self.root, text="Confirm your password:")
        self.confirm_password_entry = tk.Entry(self.root, show="*", validate="key", validatecommand=(self.root.register(self.validate_confirm_password_entry), "%P"))
        self.confirm_password_status = tk.Label(self.root, text="")

        self.register_button = tk.Button(self.root, text = "Register", command=self.register)

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
        self.availability_entry.pack()

        self.password_label.pack()
        self.password_entry.pack()
        self.password_status.pack()

        self.confirm_password_label.pack()
        self.confirm_password_entry.pack()
        self.confirm_password_status.pack()

        self.register_button.pack()

        self.center_window()

        self.root.mainloop()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 1000  
        window_height = 800 

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def register (self):
        username = self.username_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        age = self.age_entry.get()
        camp_id = self.selected_camp_id.get()
        availability = self.availability_entry.get()
        password = self.password_entry.get()

        try:
            self.validate_username(username)
            self.validate_first_name(first_name)
            self.validate_last_name(last_name)
            self.validate_phone(phone)
            self.validate_age(age)
            self.validate_password(password)

            with open ("intro-programming/files/logindetails.csv", "a") as file:
                file.write(f"{username},{password},{True}\n")

            with open ("intro-programming/files/volunteers.csv", "a") as file:
                file.write(f"{username},{first_name},{last_name},{phone},{age},{camp_id},{availability}\n")
        
            messagebox.showinfo("Success", "Registration successful!")
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def validate_username(self, username):
        with open("intro-programming/files/logindetails.csv", "r") as file:
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

        if len(first_name)>20 or len(first_name) <0:
            raise ValueError ("Name has to be between 0-20 letters")
        elif not first_name_stripped.istitle():
            raise ValueError("The first letter of the name should be capitalized")
                

    def validate_last_name(self, last_name):
        alphabet = "^[a-zA-Z\s]+$"
        if not bool(re.match(alphabet, last_name)):
            raise ValueError ("Name can only be letters")
        elif " " in last_name:
            raise ValueError ("Do not enter spaces in name")
        
        last_name_stripped = last_name.strip()
           
        if len(last_name)>20 or len(last_name) <0:
            raise ValueError    ("Name has to be between 0-20 letters")
        elif not last_name_stripped.istitle():
            raise ValueError("The first letter of the name should be capitalized")

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
        
    def read_camp_id_values_from_csv(self):
        camp_id_values = []
        try:
            with open("intro-programming/files/camps_file.csv", "r") as file:
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

if __name__ == "__main__":
    registration = UserRegistration()

