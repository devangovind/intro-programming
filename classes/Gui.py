import tkinter as tk
from tkinter import ttk, messagebox
import csv
import re

# Filepath for MAC
logindetails_filepath = "intro-programming/files/logindetails.csv"
camps_filepath = "intro-programming/files/camps_file.csv"
volunteers_filepath = "intro-programming/files/volunteers.csv" 

class Volunteer_Register:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Volunteer Registration")
        self.root.geometry("950x500")

        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        self.username_label = tk.Label(self.scrollable_frame, text = "\nUsername:\nYour username should be between 8 and 16 characters long and only consist of letters a-z and numbers 0-9")
        self.username_entry = tk.Entry(self.scrollable_frame, validate="key", validatecommand=(self.root.register(self.validate_username_entry), "%P"))
        self.username_status = tk.Label(self.scrollable_frame, text="")

        self.first_name_label = tk.Label(self.scrollable_frame, text = "First Name:\nYour first name should be between 0 and 20 letters long and the first letter should be capitalized ")
        self.first_name_entry = tk.Entry(self.scrollable_frame, validate="key", validatecommand=(self.root.register(self.validate_first_name_entry), "%P"))
        self.first_name_status = tk.Label(self.scrollable_frame, text="")

        self.last_name_label = tk.Label(self.scrollable_frame, text = "Last Name:\nYour last name should be between 0 and 20 letters long and the first letter should be capitalized")
        self.last_name_entry = tk.Entry(self.scrollable_frame, validate="key", validatecommand=(self.root.register(self.validate_last_name_entry), "%P"))
        self.last_name_status = tk.Label(self.scrollable_frame, text="")

        self.phone_label = tk.Label(self.scrollable_frame, text = "Phone:\nYour phone should be between 6 and 15 numbers long")
        self.phone_entry = tk.Entry(self.scrollable_frame, validate="key", validatecommand=(self.root.register(self.validate_phone_entry), "%P"))
        self.phone_status = tk.Label(self.scrollable_frame, text="")

        self.age_label = tk.Label(self.scrollable_frame, text = "Age:\nYour age should be numbers between 0 and 140")
        self.age_entry = tk.Entry(self.scrollable_frame, validate="key", validatecommand=(self.root.register(self.validate_age_entry), "%P"))
        self.age_status = tk.Label(self.scrollable_frame, text="")

        self.camp_id_label = tk.Label(self.scrollable_frame, text = "Camp_ID:\nChoose you Camp ID")
        self.camp_id_values = self.read_camp_id_values_from_csv()  
        self.selected_camp_id = tk.StringVar()
        self.camp_id_dropdown = ttk.Combobox(self.scrollable_frame, textvariable=self.selected_camp_id, values=self.camp_id_values)

        self.availability_label = tk.Label(self.scrollable_frame, text="\nAvailability:")
        self.availability_variables = [tk.IntVar() for _ in range(7)]
        self.availability_checkboxes = [
            tk.Checkbutton(self.scrollable_frame, text=day, variable=self.availability_variables[i])
            for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        ]

        self.password_label = tk.Label(self.scrollable_frame, text = "\nPassword:\nYour password should contain at least one capital letter, at least one of '?' or '!', letters a-z and numbers 0-9 and be between 8 and 16 characters long")
        self.password_entry = tk.Entry(self.scrollable_frame, show = "*",validate="key", validatecommand=(self.root.register(self.validate_password_entry), "%P"))
        self.password_status = tk.Label(self.scrollable_frame, text="")

        self.confirm_password_label = tk.Label(self.scrollable_frame, text="Confirm your password:")
        self.confirm_password_entry = tk.Entry(self.scrollable_frame, show="*", validate="key", validatecommand=(self.root.register(self.validate_confirm_password_entry), "%P"))
        self.confirm_password_status = tk.Label(self.scrollable_frame, text="")

        self.register_button = tk.Button(self.scrollable_frame, text = "Register", command=self.register)

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

        self.password_label.pack()
        self.password_entry.pack()
        self.password_status.pack()

        self.confirm_password_label.pack()
        self.confirm_password_entry.pack()
        self.confirm_password_status.pack()

        self.register_button.pack()

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        #self.center_window()

        self.root.mainloop()

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

  #  def center_window(self):
  #      screen_width = self.root.winfo_screenwidth()
  #      screen_height = self.root.winfo_screenheight()

  #      window_width = 505
  #      window_height = 600 

  #      x = (screen_width - window_width) // 2
  #      y = (screen_height - window_height) // 2

  #      self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def register (self):
        username = self.username_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        age = self.age_entry.get()
        camp_id = self.selected_camp_id.get()
        availability_binary = "".join(str(var.get()) for var in self.availability_variables)
        password = self.password_entry.get()
        account_type = "Volunteer"

        try:
            self.validate_username(username)
            self.validate_first_name(first_name)
            self.validate_last_name(last_name)
            self.validate_phone(phone)
            self.validate_age(age)
            self.validate_password(password)
            
            # update logindetails file
            with open (logindetails_filepath, "a") as file:
                file.write(f"{username},{password},{True},{account_type}\n")

            # update volunteers file
            with open (volunteers_filepath, "a") as file:
                file.write(f"{username},{first_name},{last_name},{phone},{age},{camp_id},{availability_binary}\n")

            # update camps file
            camp_data = []
            with open(camps_filepath, "r") as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if row[0] == camp_id:
                        row[2] = str(int(row[2]) + 1)  # Increment the number of volunteers by 1
                    camp_data.append(row)

            with open(camps_filepath, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(camp_data)
        
            messagebox.showinfo("Success", "Registration successful!")
            self.root.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

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
            raise ValueError ("Age must be numbers")
        
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
    
    def validate_confirm_password_entry(self, value):
        try:
            password = self.password_entry.get()
            self.validate_confirm_password(password, value)
            self.confirm_password_status.config(text="Passwords match", fg="green")
        except ValueError as e:
            self.confirm_password_status.config(text=str(e), fg="red")
        return True

if __name__ == "__main__":
    registration = Volunteer_Register()

