import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from tkinter import messagebox
import tkinter.font as tkFont
from tkinter import messagebox
from Volunteer import Volunteer
from Camps import Camps
from Refugee import Refugee
# from main_gui import run
from Data_visualisation import create_pie_chart
import matplotlib.pyplot as plt

class VolunteerGui:
    def __init__(self, volunteer, loginwindow):
        self.root = tk.Tk()
        self.root.geometry("990x600")
        self.root.title("Volunteer View")
        self.volunteer = volunteer
        self.camps = Camps()
        self.refugee = Refugee()
        self.volunteer_data = self.volunteer.get_volunteer_data()
        self.create_nav_bar() # Creates the navigation bar at the top
        self.create_content_frame()  # Creates the content frame below the navigation bar
        self.welcome_message() # Adds the welcome message to the content frame
        self.tree_view = None
        self.loginwindow = loginwindow
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
        self.home_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.edit_details_btn = tk.Button(self.headerarea, text="Edit Personal Details", font=('Arial', 16), command=self.edit_details)
        self.edit_details_btn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.edit_camp_btn = tk.Button(self.headerarea, text="Edit Camp Details", font=('Arial', 16), command=self.edit_camp)
        self.edit_camp_btn.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.view_camp_btn = tk.Button(self.headerarea, text="View Camp Details", font=('Arial', 16), command=self.display_resources)
        self.view_camp_btn.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
        self.add_refugee_btn = tk.Button(self.headerarea, text="Create Refugee Profile", font=('Arial', 16), command=self.add_refugee) 
        self.add_refugee_btn.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")
        self.logout_btn = tk.Button(self.headerarea, text="Logout", font=('Arial', 16), command=self.logout)
        self.logout_btn.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")
        self.headerarea.pack(fill ="both", padx=20)
        self.nav_bar = [self.headerarea, self.home_btn,self.edit_camp_btn, self.edit_details_btn, self.view_camp_btn, self.add_refugee_btn, self.logout_btn]

        def resize(e):
            size = e.width / 70
            self.home_btn.config(font=('Arial', int(size)))
            self.edit_camp_btn.config(font=('Arial', int(size)))
            self.edit_details_btn.config(font=('Arial', int(size)))
            self.view_camp_btn.config(font=('Arial', int(size)))
            self.add_refugee_btn.config(font=('Arial', int(size)))
            self.logout_btn.config(font=('Arial', int(size)))

        self.headerarea.bind('<Configure>', resize)

    def create_content_frame(self):
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(fill='both', expand=True, pady=10)

    def welcome_message(self):
        self.clear_content()
        welcome_back = f'Welcome Back, {self.volunteer.username}'
        label = tk.Label(self.content_frame, text=welcome_back, font=('Arial', 24))
        label.pack(pady=120)

    def edit_details(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="Edit Personal Details", font=('Arial', 16))
        title.config(fg="medium slate blue")
        title.pack(pady=15)        
        first_name_lbl = tk.Label(self.content_frame, text="Edit First Name:", font=('Arial', 16))
        first_name_inp = tk.Entry(self.content_frame)
        first_name_inp.insert(0, self.volunteer_data['First Name'].values[0])
        self.first_name_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.first_name_error.config(fg="red")
        first_name_lbl.pack(pady=10)
        first_name_inp.pack()
        self.first_name_error.pack()
        last_name_lbl = tk.Label(self.content_frame, text="Edit Last Name:", font=('Arial', 16))
        last_name_inp = tk.Entry(self.content_frame)
        last_name_inp.insert(0, self.volunteer_data['Last Name'].values[0])
        self.last_name_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.last_name_error.config(fg="red")
        last_name_lbl.pack()
        last_name_inp.pack()
        self.last_name_error.pack()
        phone_lbl = tk.Label(self.content_frame, text="Edit Phone Number:", font=('Arial', 16))
        phone_inp = tk.Entry(self.content_frame)
        phone_inp.insert(0, self.volunteer_data['Phone'].values[0])
        self.phone_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.phone_error.config(fg="red")
        phone_lbl.pack()
        phone_inp.pack()
        self.phone_error.pack()
        age_lbl = tk.Label(self.content_frame, text="Edit Age:", font=('Arial', 16))
        age_inp = tk.Entry(self.content_frame)
        age_inp.insert(0, self.volunteer_data['Age'].values[0])
        self.age_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.age_error.config(fg="red")
        age_lbl.pack()
        age_inp.pack()
        self.age_error.pack()
        cancel_btn = tk.Button(self.content_frame, text="Cancel", font=('Arial', 14), command=self.welcome_message)
        cancel_btn.pack(pady=20)
        submit_btn = tk.Button(self.content_frame, text="Submit", font=('Arial', 14), command=lambda: self.submit_details(first_name_inp.get(), last_name_inp.get(), phone_inp.get(), age_inp.get()))
        submit_btn.pack()
        
        def resize(e):
            size = e.width / 70
            cancel_btn.config(font=('Arial', int(size)))
            submit_btn.config(font=('Arial', int(size)))
            
        self.content_frame.bind('<Configure>', resize)

    def submit_details(self, fname, lname, phone, age):
        res = self.volunteer.edit_volunteer_details(fname,lname,phone,age)
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
        title = tk.Label(self.content_frame, text="Edit Camp Details", font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=15)
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
        selected_camp = tk.StringVar(self.content_frame)
        selected_camp.set(camps_ids[saved_idx])
        str_out = tk.StringVar(self.content_frame)
        str_out.set('Output')

        camps_menu_lbl = tk.Label(self.content_frame, text="Edit Camp:", font=('Arial', 16))
        camps_menu = tk.OptionMenu(self.content_frame, selected_camp, *camps_ids)
        camps_menu_lbl.pack()
        camps_menu.pack()

        # Availability section - to move to edit personal details
        # availability_lbl = tk.Label(self.content_frame, text="Edit Availability:", font=('Arial', 16))
        # availability_lbl.pack(pady=10)
        # volunteer_availability = str(self.volunteer_data['Availability'].values[0]).zfill(7)
        # availability_array = []
        # print(volunteer_availability)
        # for c in volunteer_availability:
        #     if c == "1":
        #         availability_array.append(True)
        #     else:
        #         availability_array.append(False)
        # self.mon_var = tk.BooleanVar(value=availability_array[0])
        # self.tue_var = tk.BooleanVar(value=availability_array[1])
        # self.wed_var = tk.BooleanVar(value=availability_array[2])
        # self.thu_var = tk.BooleanVar(value=availability_array[3])
        # self.fri_var = tk.BooleanVar(value=availability_array[4])
        # self.sat_var = tk.BooleanVar(value=availability_array[5])
        # self.sun_var = tk.BooleanVar(value=availability_array[6])
        # self.availability_variables = [self.mon_var, self.tue_var, self.wed_var, self.thu_var, self.fri_var, self.sat_var, self.sun_var]
        # availability_frame = tk.Frame(self.content_frame)
        # availability_frame.columnconfigure(0, weight=1)
        # availability_frame.columnconfigure(1, weight=1)
        # availability_frame.columnconfigure(2, weight=1)
        # mon_box = tk.Checkbutton(availability_frame, text="Monday", variable=self.mon_var)
        # tue_box = tk.Checkbutton(availability_frame, text="Tuesday", variable=self.tue_var)
        # wed_box = tk.Checkbutton(availability_frame, text="Wednesday", variable=self.wed_var)
        # thu_box = tk.Checkbutton(availability_frame, text="Thursday", variable=self.thu_var)
        # fri_box = tk.Checkbutton(availability_frame, text="Friday", variable=self.fri_var)
        # sat_box = tk.Checkbutton(availability_frame, text="Saturday", variable=self.sat_var)
        # sun_box = tk.Checkbutton(availability_frame, text="Sunday", variable=self.sun_var)
        # mon_box.grid(row=0, column=0)
        # tue_box.grid(row=1, column=0)
        # wed_box.grid(row=0, column=1)
        # thu_box.grid(row=1, column=1)
        # fri_box.grid(row=0, column=2)
        # sat_box.grid(row=1, column=2)
        # sun_box.grid(row=2, column=2)
        # availability_frame.pack()

        current_capacity = camps_data.loc[camps_data['Camp_ID'] == camps_ids[saved_idx], 'Num_Of_Refugees'].iloc[0]
        capacity_string = f'Edit Current Camp ({camps_ids[saved_idx]}) Capacity:'
        capacity_lbl = tk.Label(self.content_frame, text=capacity_string, font=('Arial', 16))
        capacity_lbl.pack()
        def my_show(*args):
            # dynamically updates string display of camp_id according to optionmenu selection
            str_out.set(selected_camp.get())
            capacity_string = f'Edit Current Camp ({selected_camp.get()}) Capacity:'
            capacity_lbl["text"] = capacity_string
        selected_camp.trace('w', my_show)
        
        capacity_inp = tk.Entry(self.content_frame)
        capacity_inp.insert(0, current_capacity)
        capacity_inp.pack()
        self.capacity_error = tk.Label(self.content_frame, text="", fg="red", font=('Arial', 10))
        self.capacity_error.pack()
        

        cancel_btn = tk.Button(self.content_frame, text="Cancel", font=('Arial', 14), command=self.welcome_message)
        cancel_btn.pack(pady=5)
        submit_btn = tk.Button(self.content_frame, text="Submit", font=('Arial', 14), command=lambda: self.submit_camp(selected_camp.get(), capacity_inp.get()))
        submit_btn.pack()

        # Submit resource request section-------------------------------------
        resource_request_frame = tk.Frame(self.content_frame)
        resource_request_frame.pack(fill='both', expand=True, padx=100, pady=20)

        def submit_resource_request():
            pass

        curr_volunteer = self.volunteer.username
        volunteer_curr_camp = self.volunteer_data.loc[self.volunteer_data['Username']==curr_volunteer, 'CampID'].values[0]
        request_label = tk.Label(resource_request_frame, text=f'Submit Resource Request for {volunteer_curr_camp} (your current camp):', font=('Arial', 15))
        request_label.grid(row = 0, column= 1, pady=10)

        food_request = tk.Label(resource_request_frame, text=f'Food: ', font=('Arial', 16))
        food_request.grid(row = 1, column= 0, pady=5)
        food_entry = tk.Entry(resource_request_frame)
        food_entry.grid(row=2, column=0)

        medical_sup_request = tk.Label(resource_request_frame, text=f'Medical Supplies: ', font=('Arial', 16))
        medical_sup_request.grid(row = 1, column= 1)
        medical_sup_entry = tk.Entry(resource_request_frame)
        medical_sup_entry.grid(row=2, column=1)

        tents_request = tk.Label(resource_request_frame, text=f'Tents: ', font=('Arial', 16))
        tents_request.grid(row = 1, column= 2, pady=5)
        tents_entry = tk.Entry(resource_request_frame)
        tents_entry.grid(row=2, column=2)

        submit_request_btn = tk.Button(resource_request_frame, text="Submit Request", font=('Arial', 14), command= submit_resource_request())
        submit_request_btn.grid(row=3, column=1, pady=15)

        def resize(e):
            size = e.width / 70
            cancel_btn.config(font=('Arial', int(size)))
            submit_btn.config(font=('Arial', int(size)))
            submit_request_btn.config(font=('Arial', int(size)))
            
        self.content_frame.bind('<Configure>', resize)


    def submit_camp(self, Camp_ID, capacity):
        new_availability = ""
        for i in range(len(self.availability_variables)):
            if self.availability_variables[i].get() == True: new_availability += "1"
            else: new_availability += "0"
        res = self.volunteer.edit_camp_details(Camp_ID, new_availability, capacity)
        if res == True:
            self.capacity_error.config(text="Capacity Saved", fg="green")
            self.content_frame.update_idletasks()
            messagebox.showinfo("Success", "Camp details successfully updated!")
            self.welcome_message()
        else:
            self.capacity_error.config(text=res[0])

    def display_resources(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="View Camp Details", font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=(20, 10))

        # Assuming 'volunteer_camp_id' is set elsewhere after login
        curr_volunteer = self.volunteer.username
        # volunteer_data = self.volunteer.get_volunteer_data()
        self.volunteer_camp_id = str(self.volunteer_data.loc[self.volunteer_data['Username']==curr_volunteer, 'CampID'].values[0])
        # self.volunteer_camp_id = "C12345"  # Replace with dynamic retrieval of the volunteer's camp ID

        # Create Treeview widget if it does not exist
        if self.tree_view is None:
            self.tree_view_frame = tk.Frame(self.content_frame)
            self.tree_view_frame.pack(fill='both', expand=True, pady=10)
            
            # Scrollbars for the Treeview
            tree_scroll = tk.Scrollbar(self.tree_view_frame)
            tree_scroll.pack(side='right', fill='y')
            tree_xscroll = tk.Scrollbar(self.tree_view_frame, orient='horizontal')
            tree_xscroll.pack(side='bottom', fill='x')

            # Create the Treeview widget
            self.tree_view = ttk.Treeview(self.tree_view_frame, yscrollcommand=tree_scroll.set, 
                                          xscrollcommand=tree_xscroll.set, show='headings')
            self.tree_view.pack(side='left', fill='both', expand=True)

            # Configure the scrollbars
            tree_scroll.config(command=self.tree_view.yview)
            tree_xscroll.config(command=self.tree_view.xview)

            # Define columns
            columns = ['Camp_ID', 'Num_Of_Refugees', 'Num_Of_Volunteers', 'Plan_ID', 'food_pac', 'medical_sup', 'tents']
            self.tree_view['columns'] = columns

            # Create column headings
            for col in columns:
                self.tree_view.heading(col, text=col, anchor='center')
                self.tree_view.column(col, anchor='center', width=tkFont.Font().measure(col) + 20)

            # Style configuration
            style = ttk.Style(self.content_frame)
            style.theme_use("default")
            style.configure("Treeview",
                            background="#D3D3D3",
                            foreground="black",
                            rowheight=25,
                            fieldbackground="#D3D3D3")
            style.map('Treeview', background=[('selected', '#347083')])

        # Clear the existing entries in the Treeview, if any
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        try:
            # Retrieve the camp resources
            df_output = self.camps.display_camp_resources(self.volunteer_camp_id)  # Assume this returns a DataFrame

            # Add data to the treeview
            for index, row in df_output.iterrows():
                self.tree_view.insert("", 'end', values=list(row))

            # Show 'Show Pie Chart' button only if camp details are successfully displayed
            show_chart_btn = tk.Button(self.content_frame, text="Show Pie Chart", command=self.show_pie_chart_of_resources)
            show_chart_btn.pack(pady=10)

            def resize(e):
                size = e.width / 70
                show_chart_btn.config(font=('Arial', int(size)))
            
            self.content_frame.bind('<Configure>', resize)

        except Exception as e:
            print("Failed to display camp resources:", e)
            error_label = tk.Label(self.content_frame, text="Error displaying camp resources.", background='#f0f0f0', font=('Arial', 10))
            error_label.pack(pady=10)

    def show_pie_chart_of_resources(self):
        # Retrieve values for food_pac, medical_sup, tents from the Treeview
        # Assume the Treeview has one row with these values at indices 4, 5, 6
        item = self.tree_view.get_children()[0]  # Get the first (and only) row in Treeview
        row = self.tree_view.item(item, 'values')
        resource_values = [int(row[4]), int(row[5]), int(row[6])]  # Convert to int
        resource_labels = ['food_pac', 'medical_sup', 'tents']

        # Call the create_pie_chart function
        create_pie_chart(resource_values, resource_labels, 'Camp Resource Distribution')

    def add_refugee(self):
        self.clear_content()
        title = tk.Label(self.content_frame, text="Create Refugee Profile", font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=15)
        
        # Generate and suggest a Refugee ID
        suggested_refugee_id = self.refugee.generate_refugee_id()
        
        # Dropdown for Camp ID
        Camp_ID_lbl = tk.Label(self.content_frame, text="Camp ID:", font=('Arial', 16))
        Camp_IDs = self.camps.get_camp_ids()  # Get the list of camp IDs
        Camp_ID_var = tk.StringVar(self.content_frame)
        Camp_ID_var.set(Camp_IDs[0])  # Set default value
        Camp_ID_dropdown = tk.OptionMenu(self.content_frame, Camp_ID_var, *Camp_IDs)
        Camp_ID_dropdown.config(width=17)
        Camp_ID_lbl.pack(pady=10)
        Camp_ID_dropdown.pack()

        # Create input fields for Refugee ID, Medical Condition, and Number of Relatives
        refugee_id_lbl = tk.Label(self.content_frame, text="Refugee ID:", font=('Arial', 16))
        refugee_id_inp = tk.Entry(self.content_frame)
        refugee_id_inp.insert(0, suggested_refugee_id)
        medical_condition_lbl = tk.Label(self.content_frame, text="Medical Condition:", font=('Arial', 16))
        medical_condition_inp = tk.Entry(self.content_frame)
        num_relatives_lbl = tk.Label(self.content_frame, text="Number of Relatives:", font=('Arial', 16))
        num_relatives_inp = tk.Entry(self.content_frame)

        # Pack the new widgets
        refugee_id_lbl.pack(pady=10)
        refugee_id_inp.pack()
        medical_condition_lbl.pack(pady=10)
        medical_condition_inp.pack()
        num_relatives_lbl.pack(pady=10)
        num_relatives_inp.pack()

        # Submit Button
        submit_btn = tk.Button(self.content_frame, text="Submit", font=('Arial', 14), 
                            command=lambda: self.submit_refugee_profile(
                                refugee_id_inp.get(),
                                Camp_ID_var.get(),
                                medical_condition_inp.get(),
                                num_relatives_inp.get()))
        submit_btn.pack(pady=20)

        def resize(e):
            size = e.width / 70
            submit_btn.config(font=('Arial', int(size)))
            
        self.content_frame.bind('<Configure>', resize)


    def submit_refugee_profile(self, refugee_id, Camp_ID, medical_condition, num_relatives):
        # Call create_refugee_profile from Refugee class
        result = self.refugee.create_refugee_profile(Camp_ID, medical_condition, 
                                                     num_relatives, refugee_id)
        messagebox.showinfo("Result", result)
        if result == "Refugee profile created successfully":
            self.welcome_message()

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

    # def run(self):
    #     self.root.mainloop()

# dummy = Volunteer("volunteer1")
# VGui = VolunteerGui(dummy)
# VGui.run()