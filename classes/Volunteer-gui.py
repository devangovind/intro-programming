import tkinter as tk
from tkinter import messagebox
from Volunteer import Volunteer
from Camps import Camps

class VolunteerGui:
    def __init__(self, volunteer):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Volunteer View")
        self.volunteer = volunteer
        self.volunteer_data = self.volunteer.get_volunteer_data()
        self.create_nav_bar()
        self.welcome_message()
        # self.edit_details_button = tk.Button(self.root, text="Edit personal details", font=('Arial', 20))
    def create_nav_bar(self):
        self.headerarea = tk.Frame(self.root)
        self.headerarea.columnconfigure(0, weight=1)
        self.headerarea.columnconfigure(1, weight=1)
        self.headerarea.columnconfigure(2, weight=1)
        self.headerarea.columnconfigure(3, weight=1)
        self.headerarea.columnconfigure(4, weight=1)
        self.headerarea.columnconfigure(5, weight=1)
        self.home_btn = tk.Button(self.headerarea, text="Home", font=('Arial', 16), command=self.welcome_message)
        self.home_btn.grid(row=0, column=0)
        self.edit_details_btn = tk.Button(self.headerarea, text="Edit Personal Details", font=('Arial', 16), command=self.edit_details)
        self.edit_details_btn.grid(row=0, column=1)
        self.edit_camp_btn = tk.Button(self.headerarea, text="Edit Camp Details", font=('Arial', 16), command=self.edit_camp)
        self.edit_camp_btn.grid(row=0, column=2)
        self.view_camp_btn = tk.Button(self.headerarea, text="View Camp Details", font=('Arial', 16))
        self.view_camp_btn.grid(row=0, column=3)
        self.add_refugee_btn = tk.Button(self.headerarea, text="Create Refugee Profile", font=('Arial', 16), command=self.add_refugee)
        self.add_refugee_btn.grid(row=0, column=4)
        self.logout_btn = tk.Button(self.headerarea, text="Logout", font=('Arial', 16))
        self.logout_btn.grid(row=0, column=5)
        self.headerarea.pack(padx=20)
        self.nav_bar = [self.headerarea, self.home_btn,self.edit_camp_btn, self.edit_details_btn, self.view_camp_btn, self.add_refugee_btn, self.logout_btn]
    def welcome_message(self):
        self.clear_content()
        welcome_back = f'Welcome Back, {self.volunteer.username}'
        label = tk.Label(self.root, text=welcome_back, font=('Arial', 24))
        label.pack(pady=100)
    def edit_details(self):
        self.clear_content()
        title = tk.Label(self.root, text="Edit Details", font=('Arial', 24))
        title.pack(pady=20)
        
        first_name_lbl = tk.Label(self.root, text="Edit First Name:", font=('Arial', 18))
        first_name_inp = tk.Entry(self.root)
        first_name_inp.insert(0, self.volunteer_data['First Name'].values[0])
        self.first_name_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
        first_name_lbl.pack(pady=10)
        first_name_inp.pack()
        self.first_name_error.pack()
        last_name_lbl = tk.Label(self.root, text="Edit Last Name:", font=('Arial', 18))
        last_name_inp = tk.Entry(self.root)
        last_name_inp.insert(0, self.volunteer_data['Last Name'].values[0])
        self.last_name_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
        last_name_lbl.pack()
        last_name_inp.pack()
        self.last_name_error.pack()
        phone_lbl = tk.Label(self.root, text="Edit Phone Number:", font=('Arial', 18))
        phone_inp = tk.Entry(self.root)
        phone_inp.insert(0, self.volunteer_data['Phone'].values[0])
        self.phone_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
        phone_lbl.pack()
        phone_inp.pack()
        self.phone_error.pack()
        age_lbl = tk.Label(self.root, text="Edit Age:", font=('Arial', 18))
        age_inp = tk.Entry(self.root)
        age_inp.insert(0, self.volunteer_data['Age'].values[0])
        self.age_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
        age_lbl.pack()
        age_inp.pack()
        self.age_error.pack()
        cancel_btn = tk.Button(self.root, text="Cancel", font=('Arial', 20), command=self.welcome_message)
        cancel_btn.pack(pady=30)
        submit_btn = tk.Button(self.root, text="Submit", font=('Arial', 20), command=lambda: self.submit_details(first_name_inp.get(), last_name_inp.get(), phone_inp.get(), age_inp.get()))
        submit_btn.pack()
    def submit_details(self, fname, lname, phone, age):
        res = self.volunteer.edit_volunteer_details(fname,lname,phone,age, "camp_01", "00000")
        if res == True:
            self.first_name_error.config(text="First Name Saved", fg="green")
            self.last_name_error.config(text="Last Name Saved", fg="green")
            self.phone_error.config(text="Phone Number Saved", fg="green")
            self.age_error.config(text="Age Saved", fg="green")
            self.root.update_idletasks() 
            messagebox.showinfo("Success", "Details successfully updated!")
            self.welcome_message()
            
        else:
            self.first_name_error.config(text=res[0])
            self.last_name_error.config(text=res[1])
            self.phone_error.config(text=res[2])
            self.age_error.config(text=res[3])
    def edit_camp(self):
        self.clear_content()
        title = tk.Label(self.root, text="Edit Camp Details", font=('Arial', 24))
        title.pack(pady=20)
        camps = Camps()
        camps_data = camps.get_data()
        camps_ids = []
        i = 0
        for val in camps_data['camp_id']:
            if val in camps_ids:
                continue
            else:
                if val == self.volunteer_data['CampID'].values[0]:
                    saved_idx= i
                camps_ids.append(val)
                i += 1
        selected_camp = tk.StringVar(self.root)
        selected_camp.set(camps_ids[saved_idx])
        camps_menu_lbl = tk.Label(self.root, text="Edit Camp:", font=('Arial', 18))
        camps_menu = tk.OptionMenu(self.root, selected_camp, *camps_ids)
        camps_menu_lbl.pack()
        camps_menu.pack()
        availability_lbl = tk.Label(self.root, text="Edit Availability:", font=('Arial', 18))
        availability_lbl.pack(pady=10)
        volunteer_availability = str(self.volunteer_data['Availability'].values[0]).zfill(7)
        availability_array = []
        print(volunteer_availability)
        for c in volunteer_availability:
            if c == "1":
                availability_array.append(True)
            else:
                availability_array.append(False)
        self.mon_var = tk.BooleanVar(value=availability_array[0])
        self.tue_var = tk.BooleanVar(value=availability_array[1])
        self.wed_var = tk.BooleanVar(value=availability_array[2])
        self.thu_var = tk.BooleanVar(value=availability_array[3])
        self.fri_var = tk.BooleanVar(value=availability_array[4])
        self.sat_var = tk.BooleanVar(value=availability_array[5])
        self.sun_var = tk.BooleanVar(value=availability_array[6])
        self.availability_variables = [self.mon_var, self.tue_var, self.wed_var, self.thu_var, self.fri_var, self.sat_var, self.sun_var]
        availability_frame = tk.Frame(self.root)
        availability_frame.columnconfigure(0, weight=1)
        availability_frame.columnconfigure(1, weight=1)
        availability_frame.columnconfigure(2, weight=1)
        mon_box = tk.Checkbutton(availability_frame, text="Monday", variable=self.mon_var)
        tue_box = tk.Checkbutton(availability_frame, text="Tuesday", variable=self.tue_var)
        wed_box = tk.Checkbutton(availability_frame, text="Wednesday", variable=self.wed_var)
        thu_box = tk.Checkbutton(availability_frame, text="Thursday", variable=self.thu_var)
        fri_box = tk.Checkbutton(availability_frame, text="Friday", variable=self.fri_var)
        sat_box = tk.Checkbutton(availability_frame, text="Saturday", variable=self.sat_var)
        sun_box = tk.Checkbutton(availability_frame, text="Sunday", variable=self.sun_var)
        mon_box.grid(row=0, column=0)
        tue_box.grid(row=1, column=0)
        wed_box.grid(row=0, column=1)
        thu_box.grid(row=1, column=1)
        fri_box.grid(row=0, column=2)
        sat_box.grid(row=1, column=2)
        sun_box.grid(row=2, column=2)
        availability_frame.pack()
        current_capacity = camps_data.loc[camps_data['camp_id'] == camps_ids[saved_idx], 'population'].iloc[0]
        capacity_string = f'Edit Current Camp ({camps_ids[saved_idx]}) Capacity:'
        capacity_lbl = tk.Label(self.root, text=capacity_string, font=('Arial', 18))
        capacity_lbl.pack()
        capacity_inp = tk.Entry(self.root)
        capacity_inp.insert(0, current_capacity)
        capacity_inp.pack()
        self.capacity_error = tk.Label(self.root, text="", fg="red", font=('Arial', 16))
        self.capacity_error.pack()
        

        cancel_btn = tk.Button(self.root, text="Cancel", font=('Arial', 20), command=self.welcome_message)
        cancel_btn.pack(pady=30)
        submit_btn = tk.Button(self.root, text="Submit", font=('Arial', 20), command=lambda: self.submit_camp(selected_camp.get(), capacity_inp.get()))
        submit_btn.pack()

    def submit_camp(self, camp_id, capacity):
        new_availability = ""
        for i in range(len(self.availability_variables)):
            if self.availability_variables[i].get() == True: new_availability += "1"
            else: new_availability += "0"
        res = self.volunteer.edit_camp_details(camp_id, new_availability, capacity)
        if res == True:
            self.capacity_error.config(text="Capacity Saved", fg="green")
            self.root.update_idletasks()
            messagebox.showinfo("Success", "Camp details successfully updated!")
            self.welcome_message()
        else:
            self.capacity_error.config(text=res[0])
    
    def add_refugee(self):
        self.clear_content()
        
        # Create labels and entry widgets for refugee details
        refugee_id_lbl = tk.Label(self.root, text="Refugee ID:", font=('Arial', 18))
        refugee_id_inp = tk.Entry(self.root)
        camp_id_lbl = tk.Label(self.root, text="Camp ID:", font=('Arial', 18))
        camp_id_inp = tk.Entry(self.root)
        medical_condition_lbl = tk.Label(self.root, text="Medical Condition:", font=('Arial', 18))
        medical_condition_inp = tk.Entry(self.root)
        num_relatives_lbl = tk.Label(self.root, text="Number of Relatives:", font=('Arial', 18))
        num_relatives_inp = tk.Entry(self.root)

        # Packing the labels and entry widgets
        refugee_id_lbl.pack(pady=10)
        refugee_id_inp.pack()
        camp_id_lbl.pack(pady=10)
        camp_id_inp.pack()
        medical_condition_lbl.pack(pady=10)
        medical_condition_inp.pack()
        num_relatives_lbl.pack(pady=10)
        num_relatives_inp.pack()

        # Submit Button
        submit_btn = tk.Button(self.root, text="Create Refugee Profile", font=('Arial', 20), 
                            command=lambda: self.submit_refugee_profile(refugee_id_inp.get(), 
                                                                        camp_id_inp.get(), 
                                                                        medical_condition_inp.get(), 
                                                                        num_relatives_inp.get()))
        submit_btn.pack(pady=20)


    def submit_refugee_profile(self, refugee_id, camp_id, medical_condition, num_relatives):
        result = self.volunteer.create_refugee_profile(refugee_id, camp_id, medical_condition, num_relatives)
        messagebox.showinfo("Result", result)
        if result == "Refugee profile created successfully":
            self.welcome_message()

    def clear_content(self):
        for widget in self.root.winfo_children():
            if widget not in self.nav_bar:
                widget.destroy()
    def run(self):
    
        self.root.mainloop()

dummy = Volunteer("volunteer1")
VGui = VolunteerGui(dummy)
VGui.run()