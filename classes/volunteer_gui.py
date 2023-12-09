import tkinter as tk
from tkinter import ttk
# import ttkbootstrap as tb
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import messagebox
from Volunteer import Volunteer
from Camps import Camps
from Refugee import Refugee
from Messages import Messages
import datetime
# from main_gui import run
from Data_visualisation import create_pie_chart
import matplotlib.pyplot as plt
import pandas as pd


class VolunteerGui:
    def __init__(self, volunteer, loginwindow):
        self.root = tk.Tk()
        # self.root = tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.minsize(1200,600)

        #Print the screen size
        print("Screen width:", screen_width)
        print("Screen height:", screen_height)

        width_to_use = int(0.85*screen_width)
        height_to_use = int(0.95*screen_height)
        self.root.geometry(f"{width_to_use}x{height_to_use}")

        # self.root.geometry("990x660")
        self.root.title("Volunteer View")
        self.volunteer = volunteer
        # self.volunteer = Volunteer(volunteer)
        self.camps = Camps()
        self.refugee = Refugee()
        self.messages = Messages()
        self.volunteer_data = self.volunteer.get_volunteer_data()
        self.create_nav_bar() # Creates the navigation bar at the top
        self.create_content_frame()  # Creates the content frame below the navigation bar
        self.welcome_message() # Adds the welcome message to the content frame
        self.tree_view = None
        self.loginwindow = loginwindow
        
        
    
    def create_nav_bar(self):
        self.headerarea = tk.Frame(self.root)
        self.headerarea.columnconfigure(0, weight=1)
        self.headerarea.columnconfigure(1, weight=1)
        self.headerarea.columnconfigure(2, weight=1)
        self.headerarea.columnconfigure(3, weight=1)
        self.headerarea.columnconfigure(4, weight=1)
        self.headerarea.columnconfigure(5, weight=1)
        self.headerarea.columnconfigure(6, weight=1)
        s = ttk.Style()
        s.configure('Nav.TButton', font=('Arial',11))

        # self.home_btn = tk.Button(self.headerarea, text="Home", font=('Arial', 11), command=self.welcome_message)
        self.home_btn = ttk.Button(self.headerarea, text="Home", style='Nav.TButton', command=self.welcome_message)
        self.home_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # self.edit_details_btn = tk.Button(self.headerarea, text="Edit Personal Details", font=('Arial', 11), command=self.edit_details)
        self.edit_details_btn = ttk.Button(self.headerarea, text="Edit Personal Details", style='Nav.TButton', command=self.edit_details)
        self.edit_details_btn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # self.edit_camp_btn = tk.Button(self.headerarea, text="Edit Camp Details", font=('Arial', 11), command=self.edit_camp)
        self.edit_camp_btn = ttk.Button(self.headerarea, text="Edit Camp Details", style='Nav.TButton', command=self.edit_camp)
        self.edit_camp_btn.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # self.view_camp_btn = tk.Button(self.headerarea, text="View Camp Details", font=('Arial', 11), command=self.display_resources)
        self.view_camp_btn = ttk.Button(self.headerarea, text="View Camp Details", style='Nav.TButton', command=self.display_resources)
        self.view_camp_btn.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        # self.add_refugee_btn = tk.Button(self.headerarea, text="Create Refugee Profile", font=('Arial', 11), command=self.add_refugee) 
        self.add_refugee_btn = ttk.Button(self.headerarea, text="Create Refugee Profile", style='Nav.TButton', command=self.add_refugee) 
        self.add_refugee_btn.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        # self.view_refugees_btn = tk.Button(self.headerarea, text="View Refugees", font=('Arial', 11), command=self.view_refugee) 
        self.view_refugees_btn = ttk.Button(self.headerarea, text="View Refugees", style='Nav.TButton', command=self.view_refugee) 
        self.view_refugees_btn.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")

        self.chat_btn = ttk.Button(self.headerarea, text="Chat", style='Nav.TButton', command=self.chat) 
        self.chat_btn.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")

        # self.logout_btn = tk.Button(self.headerarea, text="Logout", font=('Arial', 11), command=self.logout)
        self.logout_btn = ttk.Button(self.headerarea, text="Logout", style='Nav.TButton', command=self.logout)
        self.logout_btn.grid(row=0, column=7, padx=10, pady=10, sticky="nsew")

        self.headerarea.pack(fill ="both", padx=20)
        self.nav_bar = [self.headerarea, self.home_btn,self.edit_camp_btn, self.edit_details_btn, self.view_camp_btn, self.add_refugee_btn, self.view_refugees_btn, self.logout_btn]

        # def resize(e):
        #     size = e.width / 1000
        #     s.configure('Nav.TButton', font=('Arial', 3))
        # #     self.home_btn.config(font=('Arial', int(size)))
        # #     self.edit_camp_btn.config(font=('Arial', int(size)))
        # #     self.edit_details_btn.config(font=('Arial', int(size)))
        # #     self.view_camp_btn.config(font=('Arial', int(size)))
        # #     self.add_refugee_btn.config(font=('Arial', int(size)))
        #     #   self.view_refugees_btn.config(font=('Arial', int(size)))
        # #     self.logout_btn.config(font=('Arial', int(size)))

        # self.headerarea.bind('<Configure>', resize)
        # self.root.bind('<Configure>', resize)

    def create_content_frame(self):
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill='both', expand=True, pady=10)

    def welcome_message(self):
        self.clear_content()
        welcome_back = f'Welcome Back, {self.volunteer.username}'
        label = tk.Label(self.content_frame, text=welcome_back, font=('Arial', 24))
        label.config(fg="medium slate blue")
        label.pack(pady=120)
        option_label_text = 'Please choose an option in the navigation bar above to begin'
        label_option = tk.Label(self.content_frame, text=option_label_text, font=('Arial', 18))
        label_option.config(fg="medium slate blue")
        label_option.pack(pady=50)

        # option_label_text = 'Please choose an option in the navigation bar above to begin'
        # label_option = tk.Label(self.root, text=option_label_text, font=('Arial', 18))
        # label_option.config(fg="medium slate blue")
        # label_option.pack(pady=50)

    def edit_details(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="Edit Personal Details", font=('Arial', 16))
        title.config(fg="medium slate blue")
        title.pack(pady=9)        
        first_name_lbl = tk.Label(self.content_frame, text="Edit First Name:", font=('Arial', 14))
        first_name_inp = ttk.Entry(self.content_frame)
        first_name_inp.insert(0, self.volunteer_data['First Name'].values[0])
        self.first_name_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.first_name_error.config(fg="red")
        first_name_lbl.pack()
        first_name_inp.pack()
        self.first_name_error.pack()
        last_name_lbl = tk.Label(self.content_frame, text="Edit Last Name:", font=('Arial', 14))
        last_name_inp = ttk.Entry(self.content_frame)
        last_name_inp.insert(0, self.volunteer_data['Last Name'].values[0])
        self.last_name_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.last_name_error.config(fg="red")
        last_name_lbl.pack()
        last_name_inp.pack()
        self.last_name_error.pack()
        phone_lbl = tk.Label(self.content_frame, text="Edit Phone Number:", font=('Arial', 14))
        phone_inp = ttk.Entry(self.content_frame)
        phone_inp.insert(0, self.volunteer_data['Phone'].values[0])
        self.phone_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.phone_error.config(fg="red")
        phone_lbl.pack()
        phone_inp.pack()
        self.phone_error.pack()
        age_lbl = tk.Label(self.content_frame, text="Edit Age:", font=('Arial', 14))
        age_inp = ttk.Entry(self.content_frame)
        age_inp.insert(0, self.volunteer_data['Age'].values[0])
        self.age_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.age_error.config(fg="red")
        age_lbl.pack()
        age_inp.pack()
        self.age_error.pack()

                
        # Availability section 
        availability_lbl = tk.Label(self.content_frame, text="Edit Availability:", font=('Arial', 14))
        availability_lbl.pack(pady=10)
        volunteer_availability = str(self.volunteer_data['Availability'].values[0]).zfill(7)
        print(volunteer_availability)
        print(type(volunteer_availability))
        availability_array = []
        for c in volunteer_availability:
            if c == "1":
                availability_array.append(True) #True
            else:
                availability_array.append(False) #False
        print(availability_array)

        self.mon_var = tk.IntVar(value=availability_array[0])
        self.tue_var = tk.IntVar(value=availability_array[1])
        self.wed_var = tk.IntVar(value=availability_array[2])
        self.thu_var = tk.IntVar(value=availability_array[3])
        self.fri_var = tk.IntVar(value=availability_array[4])
        self.sat_var = tk.IntVar(value=availability_array[5])
        self.sun_var = tk.IntVar(value=availability_array[6])

        self.availability_variables = [self.mon_var, self.tue_var, self.wed_var, self.thu_var, self.fri_var, self.sat_var, self.sun_var]
        availability_frame = tk.Frame(self.content_frame)
        availability_frame.columnconfigure(0, weight=1)
        availability_frame.columnconfigure(1, weight=1)
        availability_frame.columnconfigure(2, weight=1)
        mon_box = tk.Checkbutton(availability_frame, text="Monday", variable=self.mon_var, command=lambda: self.mon_var.set(1) if self.mon_var.get() == False else self.mon_var.set(0))
        tue_box = tk.Checkbutton(availability_frame, text="Tuesday", variable=self.tue_var, command=lambda: self.tue_var.set(1) if self.tue_var.get() == False else self.tue_var.set(0))
        wed_box = tk.Checkbutton(availability_frame, text="Wednesday", variable=self.wed_var, command=lambda: self.wed_var.set(1) if self.wed_var.get() == False else self.wed_var.set(0))
        thu_box = tk.Checkbutton(availability_frame, text="Thursday", variable=self.thu_var, command=lambda: self.thu_var.set(1) if self.thu_var.get() == False else self.thu_var.set(0))
        fri_box = tk.Checkbutton(availability_frame, text="Friday", variable=self.fri_var, command=lambda: self.fri_var.set(1) if self.fri_var.get() == False else self.fri_var.set(0))
        sat_box = tk.Checkbutton(availability_frame, text="Saturday", variable=self.sat_var, command=lambda: self.sat_var.set(1) if self.sat_var.get() == False else self.sat_var.set(0))
        sun_box = tk.Checkbutton(availability_frame, text="Sunday", variable=self.sun_var, command=lambda: self.sun_var.set(1) if self.sun_var.get() == False else self.sun_var.set(0))

        #to show volunteer's current selection of availability
        for i in range(len(availability_array)):
            to_change_dict = {0: mon_box, 1: tue_box, 2: wed_box, 3: thu_box, 4: fri_box, 5:sat_box, 6: sun_box}
            if availability_array[i] == True:
                var_to_change = to_change_dict[i]
                var_to_change.select()

        mon_box.grid(row=0, column=0, sticky='w')
        tue_box.grid(row=0, column=1, sticky='w')
        wed_box.grid(row=0, column=2, sticky='w')
        thu_box.grid(row=0, column=3, sticky='w')
        fri_box.grid(row=1, column=0, sticky='w')
        sat_box.grid(row=1, column=1, sticky='w')
        sun_box.grid(row=1, column=2, sticky='w')
        availability_frame.pack()
        self.avail_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.avail_error.config(fg="red")
        self.avail_error.pack()

        s = ttk.Style()
        s.configure('EditPersonalDetails.TButton', font=('Arial',13))
        # cancel_btn = tk.Button(self.content_frame, text="Cancel", font=('Arial', 13), command=self.welcome_message)
        cancel_btn = ttk.Button(self.content_frame, text="Cancel", style= 'EditPersonalDetails.TButton', command=self.welcome_message)
        cancel_btn.pack(pady=20)
        # submit_btn = tk.Button(self.content_frame, text="Submit", font=('Arial', 13), command=lambda: self.submit_details(first_name_inp.get(), last_name_inp.get(), phone_inp.get(), age_inp.get()))
        submit_btn = ttk.Button(self.content_frame, text="Submit", style= 'EditPersonalDetails.TButton', command=lambda: self.submit_details(first_name_inp.get(), last_name_inp.get(), phone_inp.get(), age_inp.get()))
        submit_btn.pack()
        
        # def resize(e):
        #     size = e.width / 70
        #     cancel_btn.config(font=('Arial', int(size)))
        #     submit_btn.config(font=('Arial', int(size)))
            
        # self.content_frame.bind('<Configure>', resize)

    def submit_details(self, fname, lname, phone, age):
        availability = ""
        for var in self.availability_variables:
            if var.get():
                availability += "1"
            else:
                availability += "0"
        print(availability)
        res = self.volunteer.edit_volunteer_details(fname,lname,phone,age,availability)
        if res == True:
            self.first_name_error.config(text="First Name Saved", fg="green")
            self.last_name_error.config(text="Last Name Saved", fg="green")
            self.phone_error.config(text="Phone Number Saved", fg="green")
            self.age_error.config(text="Age Saved", fg="green")
            self.avail_error.config(text="Availability Saved", fg="green")
            self.root.update_idletasks() 
            messagebox.showinfo("Success", "Details successfully updated!")
            self.welcome_message()
            
        else:
            self.first_name_error.config(text=res[0])
            self.last_name_error.config(text=res[1])
            self.phone_error.config(text=res[2])
            self.age_error.config(text=res[3])
            self.avail_error.config(text=res[4])

    def edit_camp(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="Edit Camp Details", font=('Arial', 16))
        title.config(fg="medium slate blue")
        title.pack(pady=9)
        s = ttk.Style()
        s.configure('EditCamp.TButton', font=('Arial',13))

        camps = Camps()
        camps_data = camps.get_data()
        camps_ids = []
        i = 0
        saved_idx = 0
        for val in camps_data['Camp_ID']:
            if val in camps_ids:
                continue
            else:
                if val == self.volunteer_data['CampID'].values[0]:
                    saved_idx= i
                camps_ids.append(val)
                i += 1

        # Change current camp section
        self.selected_camp_change_camp = tk.StringVar(self.content_frame)
        self.selected_camp_change_camp.set(camps_ids[saved_idx])
        str_out_change_camp = tk.StringVar(self.content_frame)
        str_out_change_camp.set('Output')

        curr_volunteer = self.volunteer.username
        volunteer_curr_camp = self.volunteer_data.loc[self.volunteer_data['Username']==curr_volunteer, 'CampID'].values[0]
        self.new_options_list = []
        for id in camps_ids:
            if id != volunteer_curr_camp:
                self.new_options_list.append(id)
        self.change_camp_menu = f'Change your Camp from {volunteer_curr_camp} (current) to:'
        self.change_camp_menu_lbl = tk.Label(self.content_frame, text=self.change_camp_menu, font=('Arial', 14))
        # in options, show all camps except current one because if volunteer were to change camps, cannot change to their current camp
        change_camps_menu = tk.OptionMenu(self.content_frame, self.selected_camp_change_camp, *self.new_options_list) 
        self.change_camp_menu_lbl.pack()
        change_camps_menu.pack()

    
        # cancel_btn = tk.Button(self.content_frame, text="Cancel", font=('Arial', 13), command=self.welcome_message)
        cancel_btn = ttk.Button(self.content_frame, text="Cancel", style='EditCamp.TButton', command=self.welcome_message)
        cancel_btn.pack(pady=5)
        # submit_btn = tk.Button(self.content_frame, text="Submit", font=('Arial', 13), command=lambda: self.submit_switch_camp())
        submit_btn = ttk.Button(self.content_frame, text="Submit",style='EditCamp.TButton', command=lambda: self.submit_switch_camp())
        submit_btn.pack()

        section_line_txt = "--------------------------------------------------------------------------------"
        section_line = tk.Label(self.content_frame, text=section_line_txt, font=('Arial', 10))
        section_line.config(fg="medium slate blue")
        section_line.pack()

        # Edit Camps capacity section
        selected_camp = tk.StringVar(self.content_frame)
        selected_camp.set(camps_ids[saved_idx])
        str_out = tk.StringVar(self.content_frame)
        str_out.set('Output')

        def my_show(*args):
            # dynamically updates string display of camp_id according to optionmenu selection
            str_out.set(selected_camp.get())
            capacity_string = f'Edit Current Camp ({selected_camp.get()}) Capacity:'
            capacity_lbl["text"] = capacity_string

            #dynamically changes entry default to displayed camp_id 
            capacity_inp.delete(0, "end")
            current_capacity = camps_data.loc[camps_data['Camp_ID'] == str(selected_camp.get()), 'Capacity'].iloc[0]
            capacity_inp.insert(0, current_capacity)
            
        selected_camp.trace('w', my_show)

        camps_menu_lbl = tk.Label(self.content_frame, text="Edit Camp:", font=('Arial', 14))
        camps_menu = tk.OptionMenu(self.content_frame, selected_camp, *camps_ids)
        camps_menu_lbl.pack()
        camps_menu.pack(pady=3)

        current_capacity = camps_data.loc[camps_data['Camp_ID'] == volunteer_curr_camp, 'Capacity'].iloc[0]
        capacity_string = f'Edit Current Camp ({camps_ids[saved_idx]}) Capacity:'
        capacity_lbl = tk.Label(self.content_frame, text=capacity_string, font=('Arial', 14))
        capacity_lbl.pack()
        
        capacity_inp = ttk.Entry(self.content_frame)
        capacity_inp.insert(0, current_capacity)
        capacity_inp.pack()
        self.capacity_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.capacity_error.config(fg="red")
        self.capacity_error.pack()
        
        # cancel_btn2 = tk.Button(self.content_frame, text="Cancel", font=('Arial', 13), command=self.welcome_message)
        cancel_btn2 = ttk.Button(self.content_frame, text="Cancel", style='EditCamp.TButton', command=self.welcome_message)
        cancel_btn2.pack()
        # submit_btn2 = tk.Button(self.content_frame, text="Submit", font=('Arial', 13), command=lambda: self.submit_camp(selected_camp.get(), capacity_inp.get()))
        submit_btn2 = ttk.Button(self.content_frame, text="Submit", style='EditCamp.TButton', command=lambda: self.submit_camp(selected_camp.get(), capacity_inp.get()))
        submit_btn2.pack(pady=5)

        section_line2 = tk.Label(self.content_frame, text=section_line_txt, font=('Arial', 10))
        section_line2.config(fg="medium slate blue")
        section_line2.pack()

        # Submit resource request section-------------------------------------
        resource_request_frame = tk.Frame(self.content_frame)
        resource_request_frame.pack(padx=60)


        curr_volunteer = self.volunteer.username
        volunteer_curr_camp = self.volunteer_data.loc[self.volunteer_data['Username']==curr_volunteer, 'CampID'].values[0]
        request_label = tk.Label(resource_request_frame, text=f'Submit Resource Request for {volunteer_curr_camp} (your current camp):', font=('Arial', 14))
        request_label.grid(row = 0, column= 1, pady=2)
 
        food_request = tk.Label(resource_request_frame, text=f'Food: ', font=('Arial', 14))
        food_request.grid(row = 1, column= 0, pady=5)
        food_entry = ttk.Entry(resource_request_frame)
        food_entry.grid(row=2, column=0)
        self.food_error = tk.Label(resource_request_frame, text="", fg="red", font=('Arial', 10))
        self.food_error.config(fg="red")
        self.food_error.grid(row=3, column=0)

        medical_sup_request = tk.Label(resource_request_frame, text=f'Medical Supplies: ', font=('Arial', 14))
        medical_sup_request.grid(row = 1, column= 1)
        medical_sup_entry = ttk.Entry(resource_request_frame)
        medical_sup_entry.grid(row=2, column=1)
        self.medical_sup_error = tk.Label(resource_request_frame, text="", fg="red", font=('Arial', 10))
        self.medical_sup_error.config(fg="red")
        self.medical_sup_error.grid(row=3, column=1)

        tents_request = tk.Label(resource_request_frame, text=f'Tents: ', font=('Arial', 14))
        tents_request.grid(row = 1, column= 2, pady=5)
        tents_entry = ttk.Entry(resource_request_frame)
        tents_entry.grid(row=2, column=2)
        self.tents_error = tk.Label(resource_request_frame, text="", fg="red", font=('Arial', 10))
        self.tents_error.config(fg="red")
        self.tents_error.grid(row=3, column=2)

        # submit_request_btn = tk.Button(resource_request_frame, text="Submit Request", font=('Arial', 13), command=lambda: self.submit_resource_request(curr_volunteer, volunteer_curr_camp, food_entry.get(), medical_sup_entry.get(), tents_entry.get()))
        submit_request_btn = ttk.Button(resource_request_frame, text="Submit Request", style='EditCamp.TButton', command=lambda: self.submit_resource_request(curr_volunteer, volunteer_curr_camp, food_entry.get(), medical_sup_entry.get(), tents_entry.get()))
        submit_request_btn.grid(row=4, column=1)

        # def resize(e):
        #     size = e.width / 70
        #     cancel_btn.config(font=('Arial', int(size)))
        #     cancel_btn2.config(font=('Arial', int(size)))
        #     submit_btn.config(font=('Arial', int(size)))
        #     submit_btn2.config(font=('Arial', int(size)))
        #     submit_request_btn.config(font=('Arial', int(size)))
            
        # self.content_frame.bind('<Configure>', resize)

    def submit_switch_camp(self):
        # Obtain the new camp ID from the OptionMenu widget
        new_camp_id = self.selected_camp_change_camp.get()

        # Get the current volunteer's username and their current camp ID
        curr_volunteer = self.volunteer.username
        volunteer_curr_camp = self.volunteer_data.loc[self.volunteer_data['Username'] == curr_volunteer, 'CampID'].values[0]

        # Ensure that the new camp ID is different from the current one
        if new_camp_id != volunteer_curr_camp:
            # Call the switch_volunteer_camp method from the Volunteer class instance
            success = self.volunteer.switch_volunteer_camp(new_camp_id)
            
            if success:
                # Update the volunteer_data DataFrame with the new camp ID
                self.volunteer_data.loc[self.volunteer_data['Username'] == curr_volunteer, 'CampID'] = new_camp_id

                # Provide feedback to the user
                messagebox.showinfo("Success", "Your current camp has been successfully updated!")
                self.welcome_message()
                # self.str_out_change_camp.set(f"Camp changed successfully to {new_camp_id}.")
                # self.change_camps_error.config(text="Camp changed successfully", fg="green")
                # self.change_camp_menu_lbl.config(text=f"Your camp has been changed to {new_camp_id}.")
                
                # Reset the OptionMenu to the new camp ID or update the camp list
                # You'll need to update the 'camps_ids' list and then reset the OptionMenu
                # This is an example and may need adjustment based on your actual UI setup
                # self.camps_ids = [camp_id for camp_id in self.camps_ids if camp_id != new_camp_id]
                # self.change_camps_menu['menu'].delete(0, 'end')
                # for camp_id in self.camps_ids:
                #     self.change_camps_menu['menu'].add_command(label=camp_id, 
                #                                             command=lambda value=camp_id: self.selected_camp_change_camp.set(value))
                # self.selected_camp_change_camp.set(new_camp_id)
    
            else:
                # Provide feedback about the failure
                # self.str_out_change_camp.set("Failed to change camp. Please try again.")
                messagebox.showerror("Error", "Failed to change camp. Please try again.")
        else:
            # Provide feedback if the selected camp is the same as the current camp
            # self.str_out_change_camp.set("You are already in this camp.")
            messagebox.showerror("Error", "You are already in this camp.")
            

    def submit_camp(self, Camp_ID, capacity):
        res = self.volunteer.edit_camp_details(Camp_ID, capacity)
        if res == True:
            self.capacity_error.config(text="Capacity Saved", fg="green")
            self.content_frame.update_idletasks()
            messagebox.showinfo("Success", "Camp details successfully updated!")
            self.welcome_message()
        else:
            self.capacity_error.config(text=res[0])

    def submit_resource_request(self, username, camp_id, food, medical_supplies, tents):
        res = self.volunteer.edit_resources_req_details(username, camp_id, food, medical_supplies, tents)
        if res == True:
            print("request was success")
            self.food_error.config(text="Food request Saved", fg="green")
            self.medical_sup_error.config(text="Medical Supplies request Saved", fg="green")
            self.tents_error.config(text="Tents request Saved", fg="green")
            messagebox.showinfo("Success", "Request successfully submitted!")
            self.welcome_message()
        else:
            print("request failed")
            self.food_error.config(text=res[0])
            self.medical_sup_error.config(text=res[1])
            self.tents_error.config(text=res[2])

    def display_resources(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="View Camp Details", font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=(20, 10))
        # Add the explanation label here, right below the title
        explanation_label = tk.Label(self.content_frame, text="Your camp is highlighted. Select it and use 'Show Pie Chart' to view its resources in pie chart.",
                                     font=('Arial', 10), fg='grey')
        explanation_label.pack(pady=(5, 10))

        curr_volunteer = self.volunteer.username
        self.volunteer_camp_id = str(self.volunteer_data.loc[self.volunteer_data['Username'] == curr_volunteer, 'CampID'].values[0])

        if self.tree_view is None:
            self.tree_view_frame = tk.Frame(self.content_frame)
            self.tree_view_frame.pack(fill='both', expand=True, pady=10)

            tree_scroll = tk.Scrollbar(self.tree_view_frame)
            tree_scroll.pack(side='right', fill='y')
            tree_xscroll = tk.Scrollbar(self.tree_view_frame, orient='horizontal')
            tree_xscroll.pack(side='bottom', fill='x')

            self.tree_view = ttk.Treeview(self.tree_view_frame, yscrollcommand=tree_scroll.set, 
                                        xscrollcommand=tree_xscroll.set, selectmode='browse', show='headings')
            self.tree_view.pack(side='left', fill='both', expand=True)

            tree_scroll.config(command=self.tree_view.yview)
            tree_xscroll.config(command=self.tree_view.xview)

            columns = ['Camp_ID', 'Num_Of_Refugees', 'Num_Of_Volunteers', 'Plan_ID', 'Capacity', 'food_pac', 'medical_sup', 'tents']
            self.tree_view['columns'] = columns

            for col in columns:
                self.tree_view.heading(col, text=col, anchor='center')
                self.tree_view.column(col, anchor='center', width=tkFont.Font().measure(col) + 20)

            
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        try:
            all_camps_df = self.camps.display_all_camp_resources()  # Adjust this line to fetch data for all camps

            for index, row in all_camps_df.iterrows():
                camp_id = row['Camp_ID']
                inserted = self.tree_view.insert("", 'end', values=list(row))
                if camp_id == self.volunteer_camp_id:
                    self.tree_view.item(inserted, tags=('current_camp',))

            self.tree_view.tag_configure('current_camp', background='#007bff')

            def is_current_camp_selected(event):
                selected_item = self.tree_view.focus()
                return self.tree_view.item(selected_item, 'tags') == ('current_camp',)

            show_chart_btn = ttk.Button(self.content_frame, text="Show Pie Chart",
                                    command=lambda: self.show_pie_chart_of_resources(self.volunteer_camp_id),
                                    state='disabled')
            show_chart_btn.pack(pady=10)

            def on_treeview_select(event):
                show_chart_btn['state'] = 'normal' if is_current_camp_selected(event) else 'disabled'

            self.tree_view.bind('<<TreeviewSelect>>', on_treeview_select)

            # def resize(e):
            #     size = e.width / 70
            #     show_chart_btn.config(font=('Arial', int(size)))

            # self.content_frame.bind('<Configure>', resize)

        except Exception as e:
            print("Failed to display camp resources:", e)
            error_label = tk.Label(self.content_frame, text="Error displaying camp resources.", background='#f0f0f0', font=('Arial', 10))
            error_label.pack(pady=10)


    def show_pie_chart_of_resources(self,volunteer_camp_id):
        print("Create Pie Chart")
        # Retrieve values for food_pac, medical_sup, tents from the Treeview
        # Assume the Treeview has one row with these values at indices 4, 5, 6
        item = self.tree_view.get_children()[0]  # Get the first (and only) row in Treeview
        row = self.tree_view.item(item, 'values')
        resource_values = [int(row[5]), int(row[6]), int(row[7])]  # Convert to int
        resource_labels = ['food_pac', 'medical_sup', 'tents']

        # Call the create_pie_chart function
        create_pie_chart(resource_values, resource_labels, 'Camp Resource Distribution')


    def add_refugee(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="Create Refugee Profile", font=('Arial', 16))
        title.config(fg="medium slate blue")
        title.pack(pady=15)
        
        # Generate and suggest a Refugee ID
        suggested_refugee_id = self.refugee.generate_refugee_id()
        
        # Dropdown for Camp ID
        Camp_ID_lbl = tk.Label(self.content_frame, text="Camp ID:*", font=('Arial', 14))
        Camp_IDs = self.camps.get_camp_ids()  # Get the list of camp IDs
        camp_df = self.camps.get_data()
        # get list of camp IDs that have yet to reach capacity; user can only select from these camps
        avail_Camp_IDs = []
        for camp in Camp_IDs:
            camp_info = camp_df.loc[camp_df['Camp_ID'] == camp]
            camp_capacity = camp_info['Capacity'].values[0]
            current_num_refugees = camp_info['Num_Of_Refugees'].values[0]
            if camp_capacity > current_num_refugees:
                avail_Camp_IDs.append(camp)
            else:
                continue

        Camp_ID_var = tk.StringVar(self.content_frame)
        Camp_ID_var.set(avail_Camp_IDs[0])  # Set default value
        Camp_ID_dropdown = tk.OptionMenu(self.content_frame, Camp_ID_var, *avail_Camp_IDs)
        Camp_ID_dropdown.config(width=10)
        

        self.Camp_ID_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.Camp_ID_error.config(fg="red")
        Camp_ID_lbl.pack(pady=3)
        Camp_ID_dropdown.pack()
        self.Camp_ID_error.pack()

        # Create input fields for Refugee ID, Medical Condition, and Number of Relatives
        refugee_id_lbl = tk.Label(self.content_frame, text="[Do not change] Refugee ID:*", font=('Arial', 14))
        refugee_id_inp = ttk.Entry(self.content_frame)
        refugee_id_inp.insert(0, suggested_refugee_id)

        # Dropdown for Medical Status
        medical_status_lbl = tk.Label(self.content_frame, 
                                      text="Medical status:*", 
                                      font=('Arial', 14))
        medical_status = ['Choose health status',
                          'Healthy', 
                          'Needs attention', 
                          'Critical']
        medical_status_var = tk.StringVar(self.content_frame)
        medical_status_var.set(medical_status[0])
        medical_status_dropdown = tk.OptionMenu(self.content_frame, 
                                                medical_status_var, 
                                                *medical_status)
        # medical_status_inp = tk.Entry(self.content_frame)
        medical_status_dropdown.config(width=17)
        self.med_status_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.med_status_error.config(fg="red")
        
        # Dropdown for Medical Condition
        medical_condition_lbl = tk.Label(self.content_frame,
                  text="Primary Medical Condition (if applicable):",
                  font=('Arial', 16))
        medical_conditions = ["No Condition", "Diabetes", "Heart Attack", "Physical Trauma", "Sepsis", "Haemorrhage", "Stroke",
                                  "Seizure/Epilepsy", "Dengue", "Malaria", "Tuberculosis", "AIDS/HIV", "COVID-19", 
                                  "Starvation", "Hypothermia", "Major injuries", "Minor injuries", "Others"]
        medical_conditions_var = tk.StringVar(self.content_frame)
        medical_conditions_var.set(medical_conditions[0])
        medical_condition_dropdown = tk.OptionMenu(self.content_frame, 
                                                medical_conditions_var, 
                                                *medical_conditions)
    

        # Input field for Medical Description
        medical_description_lbl = tk.Label(self.content_frame, 
                                           text="Medical Description (Provide more details on Medical Condition):",
                                           font=('Arial', 14))
        medical_description_inp = ttk.Entry(self.content_frame, width=100)

        # Input field for Number of Relatives
        num_relatives_lbl = tk.Label(self.content_frame, 
                                     text="Number of Relatives:*", 
                                     font=('Arial', 14))
        num_relatives_inp = ttk.Entry(self.content_frame)
        self.num_relatives_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.num_relatives_error.config(fg="red")

        # Pack the widgets
        refugee_id_lbl.pack()
        refugee_id_inp.pack(pady=10)

        medical_status_lbl.pack()
        medical_status_dropdown.pack()
        self.med_status_error.pack()

        medical_condition_lbl.pack()
        # medical_condition_inp.pack()
        medical_condition_dropdown.pack(pady=10)

        medical_description_lbl.pack()
        medical_description_inp.pack(pady=15)
        
        num_relatives_lbl.pack()
        num_relatives_inp.pack()
        self.num_relatives_error.pack(pady=3)

        # Submit Button
        # submit_btn = tk.Button(self.content_frame, text="Submit", font=('Arial', 12), 
        #                     command=lambda: self.submit_refugee_profile(
        #                         refugee_id_inp.get(),
        #                         Camp_ID_var.get(),
        #                         medical_status_var.get(),
        #                         medical_conditions_var.get(),
        #                         medical_description_inp.get(),
        #                         num_relatives_inp.get()))
        submit_btn = ttk.Button(self.content_frame, text="Submit", 
                            command=lambda: self.submit_refugee_profile(
                                refugee_id_inp.get(),
                                Camp_ID_var.get(),
                                medical_status_var.get(),
                                medical_conditions_var.get(),
                                medical_description_inp.get(),
                                num_relatives_inp.get()))
        submit_btn.pack(pady=10)

        # def resize(e):
        #     size = e.width / 70
        #     submit_btn.config(font=('Arial', int(size)))
            
        # self.content_frame.bind('<Configure>', resize)
                    

    def submit_refugee_profile(self, refugee_id, Camp_ID, medical_status, medical_condition, medical_description, num_relatives):
        # Call create_refugee_profile from Refugee class
        result = self.refugee.create_refugee_profile(Camp_ID, 
                                                     medical_status, 
                                                     medical_condition, 
                                                     medical_description,
                                                     num_relatives, 
                                                     refugee_id)
        if result == "Refugee profile created successfully":
            self.Camp_ID_error.config(text="Camp ID Saved Successfully", fg="green")
            self.med_status_error.config(text="Medical Status Saved Successfully", fg="green")
            self.num_relatives_error.config(text="Number of Relatives Saved Successfully", fg="green")
            messagebox.showinfo("Result", result)
            self.welcome_message()
        elif result == "Failed to write refugee profile to CSV":
            messagebox.showerror("Error", "Failed to create refugee profile. Please try again.")
        elif result == "Refugee already exists":
            messagebox.showerror("Error", "Refugee already exists in our records.")
        else:
            self.Camp_ID_error.config(text=result[0])
            self.med_status_error.config(text=result[1])
            self.num_relatives_error.config(text=result[2])

    def view_refugee(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="View Refugee Details", font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=(20, 10))

        # self.headerarea.pack(fill ="both", padx=20)

        if self.tree_view is None:
            self.tree_view_frame = tk.Frame(self.content_frame)
            self.tree_view_frame.pack(fill='both', expand=True, pady=10)

            tree_scroll = tk.Scrollbar(self.tree_view_frame)
            tree_scroll.pack(side='right', fill='y')
            tree_xscroll = tk.Scrollbar(self.tree_view_frame, orient='horizontal')
            tree_xscroll.pack(side='bottom', fill='x')

            self.tree_view = ttk.Treeview(self.tree_view_frame, yscrollcommand=tree_scroll.set, 
                                        xscrollcommand=tree_xscroll.set, selectmode='browse', show='headings')
            self.tree_view.pack(side='left', fill='both', expand=True)

            tree_scroll.config(command=self.tree_view.yview)
            tree_xscroll.config(command=self.tree_view.xview)

            columns = ['Refugee_ID', 'Camp_ID', 'Medical Status', 'Medical Condition', 'Medical Description', 'Number of Relatives']
            self.tree_view['columns'] = columns

            for col in columns:
                self.tree_view.heading(col, text=col, anchor='center')
                self.tree_view.column(col, anchor='center', width=tkFont.Font().measure(col) + 20)


        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        try:
            refugee_data = self.refugee.display_all_refugees()  # Call the function to get refugee data

            for index, row in refugee_data.iterrows():
                self.tree_view.insert("", 'end', values=list(row))

        except Exception as e:
            print("Failed to display refugee data:", e)
            error_label = tk.Label(self.content_frame, text="Error displaying refugee data.", background='#f0f0f0', font=('Arial', 10))
            error_label.pack(pady=10)


    def chat(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="Volunteer Chat", font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=(20, 10))
        tk.Label(self.content_frame, text="Select another active volunteer to chat to", font=('Arial', 14)).pack()
        # self.all_messages = self.messages.get_all()
        self.all_users = self.volunteer.get_other_volunteers()
        

        volunteers_array = []
        for volun in self.all_users['Username']:
            volunteers_array.append(volun)
        self.selected_volunteer = tk.StringVar(self.content_frame)
        self.selected_volunteer.set(volunteers_array[0])
        receipiant_drop_down = tk.OptionMenu(self.content_frame, self.selected_volunteer, *volunteers_array, command=self.filter_chats)
        receipiant_drop_down.pack()
        ttk.Button(self.content_frame, text="Refresh", command=self.filter_chats).pack()
        self.chat_frame = tk.Frame(self.content_frame)
        
        
        self.message_box = tk.Text(self.content_frame, wrap=tk.WORD, font=('Courier New', 16))
        self.message_box.tag_config('sent', foreground="green")
        self.message_box.pack(fill=tk.BOTH, expand=True, padx=200, pady=20)
        self.message_box.config(state=tk.DISABLED)
        scroll_message_box = ttk.Scrollbar(self.message_box, orient="vertical", command=self.message_box.yview)
        self.message_box.configure(yscrollcommand=scroll_message_box.set)
        scroll_message_box.pack(side="right", fill="y")
        self.chat_frame.pack()
        self.message_entry = ttk.Entry(self.chat_frame, width=50)
        self.message_entry.grid(row=1, column=0)
        self.message_entry.bind('<Return>', self.send_message)
        send_button = ttk.Button(self.chat_frame, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1)
        tk.Label(self.content_frame, text="").pack(pady=40) ##stops table going all the way to bottom
        self.filter_chats()


    def filter_chats(self, event=None):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.delete('1.0', tk.END)
        self.receipiant = self.selected_volunteer.get()
        all_messages = self.messages.get_all_sender_receiver(self.volunteer.username, self.receipiant)
        for index, row in all_messages.iterrows():
            timestamp = row['timestamp']
            if row['volunteer_sender'] == self.volunteer.username:
                self.message_box.insert(tk.END, f"You ({timestamp}): {row['message']}\n", "sent")
            else:
                self.message_box.insert(tk.END, f"{self.receipiant} ({timestamp}): {row['message']}\n")
            self.message_box.insert(tk.END, "\n")
        self.message_box.config(state=tk.DISABLED)
        self.message_box.see("end")

    def send_message(self, event=None):
        self.message_box.config(state=tk.NORMAL)
        curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        message = self.message_entry.get()
        if message:
            self.message_box.insert(tk.END, f"You ({curr_time}): {message} \n", "sent")
            self.message_box.insert(tk.END, "\n")
            self.message_entry.delete(0, tk.END)
            self.messages.send_message(self.volunteer.username, self.receipiant, curr_time, message)
        self.message_box.config(state=tk.DISABLED)
        self.message_box.see("end")



    # When click logout button, destory volunteer menu
    def logout(self):
        self.root.destroy()
        self.loginwindow.deiconify() 

    def clear_content(self):
        # Destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Reset the tree_view to None to allow re-creation
        self.tree_view = None


