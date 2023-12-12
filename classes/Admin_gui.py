from Admin import Admin
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog, END
from Camps import Camps
from Plans import Plans
from Resource_requests import Resource_requests
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Data_visualisation import create_bar_graph, create_resources_bar_graph, create_world_map
from tkcalendar import *
import csv
import datetime
import time
from datetime import date
from FileManager import FileManager


class AdminGui:
    def __init__(self, admin, loginwindow):
        self.s_date = None
        self.e_date = None
        self.camp_num_id = None
        self.root = tk.Tk()
        self.root.minsize(1200,600)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()


        width_to_use = int(0.85*screen_width)
        height_to_use = int(0.9*screen_height)
        positioning_width = int(0.05*screen_width)
        positioning_height = int(0.01*screen_width)
        self.root.geometry(f"{width_to_use}x{height_to_use}+{positioning_width}+{positioning_height}")

        self.root.title("Admin View")
        self.admin = admin
        csv_manager = FileManager()
        self.volunteer_file = csv_manager.get_file_path("volunteers.csv")
        self.users_file  = csv_manager.get_file_path("logindetails.csv")  
        self.countries_file = csv_manager.get_file_path("countries.csv")
        # for mac
        # self.volunteer_file = "./files/volunteers.csv"
        # self.users_file = "./files/logindetails.csv"
        # self.countries_file = "./files/countries.csv"
        
        # for windows
        # self.users_file = 'files\\logindetails.csv'
        # self.volunteer_file = 'files\\volunteers.csv'
        
        self.create_nav_bar()
        self.welcome_message()
        self.camps = Camps()
        self.plans = Plans()
        self.requests = Resource_requests()
        self.camps_data = self.camps.get_data()
        self.plan_data_ = self.admin.plan_list
        self.loginwindow = loginwindow
        
        #for windows:
        # self.volunteer_file = "../files/volunteers.csv"
        # self.volunteer_data = pd.read_csv(self.volunteer_file)
        # self.users_file = "../files/logindetails.csv"
        # self.users = pd.read_csv(self.users_file)
        # self.countries_file = "../files/countries.csv"
        # countries_df = pd.read_csv(self.countries_file)

        

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
        s.configure('Nav.TButton', font=('Arial' ,11))

        self.home_btn = ttk.Button(self.headerarea, text="Home", command=self.welcome_message)

        self.home_btn.grid(row=0, column=0, padx=10, pady=10,sticky="nsew")

        self.create_plan_btn = ttk.Button(self.headerarea, text="Create New Plan", command=self.create_new_plan)


        self.create_plan_btn.grid(row=0, column=1, padx=10, pady=10,sticky="nsew")

        self.display_plans_btn = ttk.Button(self.headerarea, text="Display Existing Plans", command=self.display_plans)


        self.display_plans_btn.grid(row=0, column=2, padx=10, pady=10,sticky="nsew")

        self.create_camp_btn = ttk.Button(self.headerarea, text="Create New Camp", command=self.add_camp)


        self.create_camp_btn.grid(row=0, column=3, padx=10, pady=10,sticky="nsew")

        self.manage_camps_btn = ttk.Button(self.headerarea, text="Manage Camps", command=self.manage_camps)


        self.manage_camps_btn.grid(row=0, column=4, padx=10, pady=10,sticky="nsew")

        self.manage_volunteers_btn = ttk.Button(self.headerarea, text="Manage Volunteers", command=self.manage_volunteers)


        self.manage_volunteers_btn.grid(row=0, column=5, padx=10, pady=10,sticky="nsew")

        self.logout_btn = ttk.Button(self.headerarea, text="Logout", command=self.logout)

        self.logout_btn.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")

        self.headerarea.pack(fill ="both", padx=20)
        self.nav_bar = [self.headerarea, self.home_btn, self.display_plans_btn, self.create_plan_btn, self.create_camp_btn,
                        self.manage_camps_btn, self.manage_volunteers_btn, self.logout_btn]

            
    def welcome_message(self):
        self.clear_content()
        welcome_back_text = 'Welcome back, Admin'
        label_welcome = tk.Label(self.root, text=welcome_back_text, font=('Arial', 24))
        label_welcome.config(fg="medium slate blue")
        label_welcome.pack(pady=120)
        option_label_text = 'Please choose an option in the navigation bar above to begin'
        label_option = tk.Label(self.root, text=option_label_text, font=('Arial', 18))
        label_option.config(fg="medium slate blue")
        label_option.pack(pady=50)

    ## Admin feature a-c
    
    # Function to create a list of countries
    def get_countries_list(self):
        
        # for mac
        countries_df = pd.read_csv(self.countries_file)
        
        # for windows

        countries_list = countries_df["Location"].tolist()
        return countries_list
    
    def create_new_plan(self):
        self.clear_content()
        # intialise the countries list
        countries_list = self.get_countries_list()
        # Get the value by admin using entry
        self.Description = tk.StringVar(self.root)
        self.Location = tk.StringVar(self.root)
        # Build the label
        title = tk.Label(self.root, text='Add a New Plan',font = ('Arial',18))
        title.config(fg="medium slate blue")
        title.pack(pady=30)

        plan_ID = tk.Label(self.root, text='Plan ID (cannot be edited):',font = ('Arial',14))
        plan_ID.pack(pady=10)
        # Get the plan_ID automatically
        self.plan_id_num = (self.admin.last_plan_id() + 1)
        self.plan_id = "P" + str(self.plan_id_num)

        # Displaying the plan_ID in a read-only Entry widget
        self.plan_id_inp = ttk.Entry(self.root)

        # Insert the plan ID and make the entry read-only
        self.plan_id_inp.insert(0, self.plan_id)
        self.plan_id_inp.configure(state='readonly')

        self.plan_id_inp.pack(pady=15)  

        plan_desc = tk.Label(self.root, text='Description:',font = ('Arial',14))
        plan_desc.pack()
        self.des_entry = ttk.Entry(self.root, width=40, textvariable=self.Description)
        self.des_entry.pack(pady=25)

        plan_loc = tk.Label(self.root, text='Location:',font = ('Arial',14))
        plan_loc.pack()
        # Location menu dropdown setup - assign selected country to pass into option menu
        self.selected_country = tk.StringVar(self.root)
        self.selected_country.set(countries_list[0])
        
        # Pass countries list with unpacking (*)
        self.location_menu = tk.OptionMenu(self.root, self.selected_country, *countries_list)
        self.location_menu.pack(pady=10)
       
        date_frames = tk.Frame(self.root)
        date_frames.columnconfigure(1, weight=1)
        date_frames.columnconfigure(2, weight=1)
        date_frames.columnconfigure(3,weight=1)
        date_frames.rowconfigure(1, weight=1)
        date_frames.rowconfigure(2, weight=1)
        plan_start = tk.Label(date_frames, text='Start Date:',font = ('Arial',14))
        plan_start.grid(row=1, column=1, sticky="e")
        plan_end = tk.Label(date_frames, text='End Date:',font = ('Arial',14))
        plan_end.grid(row=2, column=1, sticky="e")
    
        # Build the button
        s = ttk.Style()
        s.configure('CreatePlan.TButton', font=('Arial',14))
        sdate_button = ttk.Button(date_frames, text='Choose the start date', style='CreatePlan.TButton', command=self.pick_sdate, width=15)
        sdate_button.grid(row=1, column=3, sticky="w")
        edate_button = ttk.Button(date_frames, text='Choose the end date',style='CreatePlan.TButton', command=self.pick_edate, width=15)
        edate_button.grid(row=2, column=3, sticky="w")
        date_frames.pack(pady=20)


        ttk.Button(self.root, text='Save this plan', command=self.save_data,style='CreatePlan.TButton').pack()

        # When admin click the entry date, admin will be informed that they need to use calendar
        def stest(content, reason, name):
            if self.start_date.get() is not None:
                messagebox.showwarning(title='Create a new plan - start date',
                                       message='Please use the button to choose the start date')
                # return False
        self.valid_input_sdate = tk.StringVar(self.root)
        sCMD = self.root.register(stest)
        self.start_date = ttk.Entry(date_frames, textvariable=self.valid_input_sdate, validate='focusin',
                                   validatecommand=(sCMD, '%P', '%V', '%W'))

        self.start_date.grid(row=1, column=2)

        def etest(content, reason, name):
            if self.end_date.get() is not None:
                messagebox.showwarning(title='Create a new plan - end date',
                                       message='Please use the button to choose the end date')
        self.valid_input_edate = tk.StringVar(self.root)
        eCMD = self.root.register(etest)
        self.end_date = ttk.Entry(date_frames, textvariable=self.valid_input_edate, validate='focusin',
                                 validatecommand=(eCMD, '%P', '%V', '%W'))

        self.end_date.grid(row=2, column=2)

    #  This method is to get the date using calendar and judge whether it is valid or not
    def pick_sdate(self):
        today = datetime.datetime.today()
        yr = today.year
        mth = today.month
        day = today.day
        self.date_window = tk.Toplevel(self.root)
        self.date_window.grab_set()
        self.date_window.geometry('230x230+590+370')
        self.cal = Calendar(self.date_window, selectmode='day', year=yr, month=mth, day=day, background='white', foreground='black', selectforeground='red', normalbackground = 'gray')
        self.date_window.resizable(False, False)
        self.cal.place(x=0, y=0)
        submit_btn = tk.Button(self.date_window, text='Submit', command=self.grab_sdate, font=('Arial', 16))
        submit_btn.place(x=80, y=190)

    def pick_edate(self):
        today = datetime.datetime.today()
        yr = today.year
        mth = today.month
        day = today.day + 1
        if len(self.start_date.get()) == 0 or self.s_date is None:
            messagebox.showwarning(title='Choose start date',
                                   message='Please choose a start date using calendar')
        else:
            self.date_window = tk.Toplevel(self.root)
            self.date_window.grab_set()
            self.date_window.geometry('230x230+590+370')
            self.date_window.resizable(False, False)
            self.cal = Calendar(self.date_window, selectmode='day', year=yr, month=mth, day=day, background='white', foreground='black', selectforeground='red', normalbackground = 'gray')
            self.cal.place(x=0, y=0)
            submit_btn = tk.Button(self.date_window, text='Submit', command=self.grab_edate)
            submit_btn.place(x=80, y=190)

    def grab_sdate(self):
        self.s_date = self.cal.selection_get()
        if self.admin.check_start_day(self.s_date):
            messagebox.showwarning(title='Choose a start date', message='The start date cannot be before today')

        else:
            self.start_date.delete(0, END)
            self.start_date.insert(0, self.s_date)
            self.date_window.destroy()
            # date = self.cal.get_date()
       
            return self.s_date

    def grab_edate(self):
        self.e_date = self.cal.selection_get()
        if self.admin.check_end_date(self.e_date, self.s_date):
            messagebox.showwarning(title='Choose start date', message='The end date should be after the start date')
        else:
            self.end_date.delete(0, END)
            self.end_date.insert(0, self.e_date)
            self.date_window.destroy()

        return self.e_date

    ## This is to save the new plan to csv file and it can be show directly later
    def save_data(self):
        Plan_ID_ = self.plan_id
        Description_ = self.Description.get()
        Location_ = self.selected_country.get()
        Start_date_ = self.s_date
        End_date_ = self.e_date
        var_start_day = self.valid_input_sdate.get()
        var_end_day = self.valid_input_edate.get()
        # ensure all the blank is not empty
        if len(self.des_entry.get()) == 0 or len(self.selected_country.get()) == 0 or len(self.start_date.get()) == 0 or len(
                self.end_date.get()) == 0:
            messagebox.showwarning(title='Create a new plan', message='Please fill in all the entries')
        # ensure choosing the date using calendar
        elif Start_date_ == None or End_date_ == None:
            messagebox.showwarning(title='Create a new plan', message='Use buttons to choose start and end date')
            self.start_date.delete(0, END)
            self.end_date.delete(0, END)
            self.e_date = None
            self.s_date = None
        elif Start_date_ is not None or End_date_ is not None:
            Start_date_ = self.s_date.strftime('%Y-%m-%d')
            End_date_ = self.e_date.strftime('%Y-%m-%d')
            if var_start_day == Start_date_ and var_end_day == End_date_ and not (
            self.admin.check_end_date(self.e_date, self.s_date)):
            ## check the status of this new plan-- onging or not started 
            
                Start_date_ = self.s_date.strftime('%d/%m/%Y')
                End_date_ = self.e_date.strftime('%d/%m/%Y')
                if self.s_date == date.today(): status = 'Ongoing'
                else: status = 'Not Started'
                plan_dic = {'Plan_ID': Plan_ID_, 'Description': Description_, 'Location': Location_,
                            'Start Date': Start_date_, 'End Date': End_date_,'Status':status}
                plan_list = pd.DataFrame({'Plan_ID': [Plan_ID_], 'Description': [Description_], 'Location': [Location_], 'Start Date': [Start_date_],
                        'End Date': [End_date_],'Status': [status]})
                header = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date','Status']
                
                self.plans.append_dateframe(plan_list)
                self.admin.insert_new_plan(plan_dic)

                messagebox.showinfo('Success', 'Plan successfully created')
                self.create_new_plan()
                
            ## check the date 
            elif self.admin.check_end_date(self.e_date, self.s_date):
                messagebox.showwarning(title='Choose start date', message='The end date cannot be before start date')
                self.start_date.delete(0, END)
                self.end_date.delete(0, END)
                self.e_date = None
                self.s_date = None
            ## check the data if using calendar 
            else:

                self.admin.is_date(var_start_day)
                messagebox.showwarning(title='Create a new plan',
                                       message='Use calender to enter date')
                self.start_date.delete(0, END)
                self.end_date.delete(0, END)
                self.e_date = None
                self.s_date = None

    def display_world_map(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Geographical Plans Visualisation")
        new_window.geometry("1200x800")
        
        fig = create_world_map()
        
        if fig is not None:
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    ## This is to show the plan by table

    def display_plans(self):
        self.clear_content()
        # add code here:
        # somewhere in here will be the end button for the individual plans which will maybe go to another function
        title = tk.Label(self.root, text="Display Humanitarian Plans", font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=20)
        header = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date','Status']
        self.table = ttk.Treeview(self.root)
        column_sizes = [60, 200, 120, 120, 120, 120]
        self.table.configure(columns=header, show='headings')
        for i in range(len(header)):
            self.table.column(header[i], width=column_sizes[i], anchor=tk.CENTER)
            self.table.heading(header[i], text=header[i])
        # this is to show if the end date in the plan has arrived, this End date will show "None"

        index = 0
        # with time passes, if start date arrives today, the status change from not starte to ongoing
        # with time passes, if end date arrives today, the status change from ongoing to finished
        df = self.plans.get_data()
  
        today_str = date.today()



        
        df['Start Date'] = pd.to_datetime(df['Start Date'], format='%d/%m/%Y')
        df['End Date'] = pd.to_datetime(df['End Date'], format='%d/%m/%Y')

        df.loc[(df['Start Date'].dt.date <= today_str) & (df['Status'] =='Not Started'), "Status"] = "Ongoing"
        df.loc[(df['End Date'].dt.date < today_str) & (df['Status'] == 'Ongoing'), "Status"] = "Finished"

        df['Start Date'] = df['Start Date'].dt.strftime('%d/%m/%Y')
        df['End Date'] = df['End Date'].dt.strftime('%d/%m/%Y')
        self.plans.write_entire_dataframe(df)

        for index, plan in (df.iterrows()):
            self.table.insert('', 'end', values=(plan['Plan_ID'], plan['Description'],
                                                          plan['Location'], plan['Start Date'], plan['End Date'],plan['Status']))
        vsb = ttk.Scrollbar(self.table, orient="vertical", command=self.table.yview)

        self.table.configure(yscrollcommand=vsb.set)

        self.table.pack(fill=tk.BOTH, expand=True)
        vsb.pack(side="right", fill="y")

        s = ttk.Style()
        s.configure('DisplayPlan.TButton', font=('Arial',14))

        self.data_vis_title = tk.Label(self.root, text="To end a plan, select the plan above and click 'End a Plan'", font=('Arial', 14))
        self.data_vis_title.pack(pady=10)

        self.end_a_plan_btn = ttk.Button(self.root, text='End a Plan', style='DisplayPlan.TButton', command=self.end_plan)
        self.end_a_plan_btn.pack()

        self.data_vis_title = tk.Label(self.root, text="Data Visualisation:", font=('Arial', 14))
        self.data_vis_title.pack(pady=10)

        self.display_refugees_btn_plans = ttk.Button(self.root, text="Refugees per plan", style='DisplayPlan.TButton', command=self.display_refugee_graph_plans)
        self.display_refugees_btn_plans.pack(pady=10)


        self.display_volunteers_btn_plans = ttk.Button(self.root, text="Volunteers per plan", style='DisplayPlan.TButton', command=self.display_volunteer_graph_plans) 
        self.display_volunteers_btn_plans.pack(pady=10)


        self.display_world_map_button = ttk.Button(self.root, text="Display world map of plans", style='DisplayPlan.TButton', command=self.display_world_map)
        self.display_world_map_button.pack(pady=10)

    def end_plan(self):
        item = self.table.selection()
        if item:
            # def valid_item_():
            item = self.table.selection()
            selected = self.table.focus()
            temp = self.table.item(selected, 'values')
            self.plan_sdate = temp[-3]
            self.plan_edate = temp[-2]
            self.status = temp[-1]
            self.plan_sdate_date = datetime.datetime.strptime(self.plan_sdate, '%d/%m/%Y').date()

            if self.plan_sdate_date > date.today():
                messagebox.showerror(title='Info', message='This plan has not started! It cannot be ended.')
            elif self.status == 'Ongoing':
                isok = messagebox.askyesno(title='infor', message='Do you want to end this plan？')
                # if isok:
                if isok:
                    # def update_item():
                    end_up = 'Finished'
                    end_date_today = time.strftime("%d/%m/%Y",time.localtime(time.time()))
                    number_id = int(temp[0][1:])
                        # add the new one (which has been edite based on the old one)
                    plans_data = self.plans.get_data()
                    plans_data.loc[plans_data["Plan_ID"] == temp[0], ["End Date", 'Status']] = [end_date_today, end_up]
                    self.plans.write_entire_dataframe(plans_data)
                    self.table.item(selected, values=(temp[0], temp[1], temp[2], temp[3], end_date_today,end_up))
                    messagebox.showinfo(title='Info', message='Plan successfully ended.')
                    self.display_plans()
            elif self.status == 'Finished':
                messagebox.showerror(title='Info', message='Plan has already ended.')
                self.display_plans()
        elif not item:
            messagebox.showerror(title='Info', message='Please choose a plan.')
            self.display_plans()

    def add_camp(self):
        self.clear_content()
        # Get the value by admin using entry
        self.capacity = tk.StringVar()
        # Build the label
        title = tk.Label(self.root, text='Add a New Camp', font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=30)
        
        tk.Label(self.root, text='Plan ID (choose from ongoing plans):', font=('Arial', 14)).pack(pady=10)

        if len(self.admin.valid_plan()) == 0 :
            plan_lbl = tk.Label(self.root, text='All plans have finished \n Create a new plan to add new camps', font=('Arial', 14))
            plan_lbl.pack(pady=30)
        else:
            self.OPTIONS = self.admin.valid_plan()
            self.first_option = self.OPTIONS[0]

            self.plan_id_camp = tk.StringVar(self.root)
            self.plan_id_camp.set(self.first_option)

            w = tk.OptionMenu(self.root, self.plan_id_camp, *self.OPTIONS)
            w.config(width=20)
            w.pack(pady=25)
            
            # # Label for "Camp ID"
            tk.Label(self.root, text='Camp ID (cannot be changed):', font=('Arial', 14)).pack(pady=20)

            # Calculate the camp ID
            self.camp_id_num = (self.admin.last_camp_id() + 1)
            self.camp_id = "C" + str(self.camp_id_num)

            # Entry widget for displaying the camp ID in a read-only mode
            self.camp_id_inp = ttk.Entry(self.root, width=25)
            self.camp_id_inp.insert(0, self.camp_id)
            self.camp_id_inp.configure(state='readonly')
            self.camp_id_inp.pack(pady=10)

            tk.Label(self.root, text='Capacity (between 100-10000):', font=('Arial', 14)).pack(pady=25)
            self.capacity_entry = ttk.Entry(self.root, width=25, textvariable=self.capacity)
            self.capacity_entry.pack()
            self.capacity_entry.config(
                validate="key",
                validatecommand=(self.root.register(lambda P: P.isdigit() or P == ""), "%P",),
            )


            s = ttk.Style()
            s.configure('AddCamp.TButton', font=('Arial',16))
            save_camp = ttk.Button(self.root, text='Save this camp', style='AddCamp.TButton', command=self.save_camp)
            save_camp.pack(pady=30)

    def save_camp(self):
        #Choose the plan 
        Plan_ID_C = self.plan_id_camp.get()
        Camp_ID  = self.camp_id
        Capacity_ = self.capacity_entry.get()
        Capacity_ = Capacity_.replace(' ', '') # delect all the " " make sure there is no " "
        Num_v = 0
        Num_r = 0
        if int(Capacity_) < 100 or int(Capacity_)>10000:
            messagebox.showwarning(title='Create a new camp', message='Please choose a capacity between 100 and 10000')
        elif int(Capacity_) >= 100 and int(Capacity_) <=10000:
            camp_plan_dic = {'Camp_ID': Camp_ID, 'Num_Of_Refugees': Num_r,
                        'Num_Of_Volunteers': Num_v, 'Plan_ID':Plan_ID_C, 'Capacity': Capacity_}
            camp_plan_list = pd.DataFrame({'Camp_ID': [Camp_ID], 'Num_Of_Refugees': [Num_r],
                 'Num_Of_Volunteers': [Num_v], 'Plan_ID': [Plan_ID_C], 'Capacity': [Capacity_]})

            self.camps.append_df(camp_plan_list)
            new_resource = pd.DataFrame({'Camp_ID': [Camp_ID], 'food_pac': [0], 'medical_sup': [0], 'tents': [0]})
            self.admin.insert_empty_resource(new_resource)
            self.admin.insert_new_plan(camp_plan_dic)
            messagebox.showinfo('Success', f'Camp added to Plan {Plan_ID_C}')
            self.capacity.set('')
            self.camp_id_num_1 = int(self.camp_id[1:])+1
            self.camp_id = "C" + str(self.camp_id_num_1)
            # Entry widget for displaying the camp ID in a read-only mode
            self.camp_id_inp.destroy()
            self.camp_id_inp = ttk.Entry(self.root, width=25)
            self.camp_id_inp.insert(0, self.camp_id)
            self.camp_id_inp.configure(state='readonly')
            self.camp_id_inp.pack(pady=10)
            # self.camp_id_label.destroy()
            # self.camp_id_label = tk.Label(self.root, text=self.camp_id,font=('Arial', 12))

            self.add_camp()

    def manage_camps(self):
        # when data visualisation is ready. we can have each camp name be clickable to bring up a new screen with the data visualised
        self.clear_content()

        title = tk.Label(self.root, text="Manage Camps", font=('Arial', 18))
        self.camps_data = self.camps.get_data()
        title.config(fg="medium slate blue")
        title.pack(pady=20)
        plans_data = self.admin.get_data()
        plans_ids = ["All Plans"]
        for val in plans_data['Plan_ID']:
            if val in plans_ids:
                continue
            plans_ids.append(val)
        self.selected_plan = tk.StringVar(self.root)
        self.selected_plan.set(plans_ids[0])
        plans_menu_lbl = tk.Label(self.root, text="Filter By Plan:", font=('Arial', 14))
        plans_menu = tk.OptionMenu(self.root, self.selected_plan, *plans_ids, command=self.filter_camps)
        plans_menu_lbl.pack()
        plans_menu.pack()
        info_lbl = tk.Label(self.root, text="Click on Allocate Resources to allocate to a specific camp", font=('Arial', 14), fg="gray")
        info_lbl.pack()
        camp_columns = ["Camp ID", "Plan ID", "No. of Volunteers", "No. of Refugees", "Capacity", "Food Packages", "Medical Supplies", "Tents", "Action (Click) ⬇"]
        column_widths = [60, 60, 100, 100, 60, 150, 150, 70, 150]
        self.camps_tree = ttk.Treeview(self.root, columns=camp_columns, show="headings")
        for i in range(len(camp_columns)):
            col = camp_columns[i]
            self.camps_tree.heading(col, text=col)
            self.camps_tree.column(col, width=column_widths[i], anchor=tk.CENTER)
        self.camps_tree.bind("<ButtonRelease-1>", self.can_allocate)        
        scrollbar = ttk.Scrollbar(self.camps_tree, orient="vertical", command=self.camps_tree.yview)
        # Configure the Treeview to use the scrollbar
        self.camps_tree.configure(yscrollcommand=scrollbar.set)
        # Place the scrollbar on the right side of the Treeview
        self.camps_tree.pack(fill=tk.BOTH, expand=True)
        

        scrollbar.pack(side="right", fill="y")
        self.data_vis_title = tk.Label(self.root, text="Resource Actions:", font=('Arial', 14))
        self.data_vis_title.pack(pady=10)
        self.unresolved = self.requests.get_unresolved()

        s = ttk.Style()
        s.configure('ManageCamp.TButton', font=('Arial',14))
        request_btn_text = f'Resource Requests ({len(self.unresolved)})'

        request_btn = ttk.Button(self.root, text=request_btn_text, style='ManageCamp.TButton', command=self.resource_requests_list)
        request_btn.pack()
        self.filter_camps()
        
        data_vis_label_res = tk.Label(self.root, text="Data Visualisation:", font=('Arial', 14))
        data_vis_label_res.pack(pady=10)
        

        self.display_resources_btn_camps = ttk.Button(self.root, text="Resources per camp", style='ManageCamp.TButton', command=self.display_resources_camps)
        self.display_resources_btn_camps.pack(pady=10)
        

        self.display_refugees_btn_camps = ttk.Button(self.root, text="Refugees per camp", style='ManageCamp.TButton', command=self.display_refugee_graph_camps)
        self.display_refugees_btn_camps.pack(pady=10)
        

        self.display_volunteers_btn_camps = ttk.Button(self.root, text="Volunteers per camp", style='ManageCamp.TButton', command=self.display_volunteer_graph_camps) 
        self.display_volunteers_btn_camps.pack(pady=10)
        
        
        


        
    def filter_camps(self, event=None):
        for item in self.camps_tree.get_children():
            self.camps_tree.delete(item)
        selected_plan = self.selected_plan.get()
        if selected_plan == "All Plans": filtered_data = self.camps_data
        else:
            filtered_data = self.camps_data[self.camps_data["Plan_ID"] == selected_plan]
        for index, row in (filtered_data.iterrows()):
            resources = self.camps.get_resource_data(row['Camp_ID'])
            values=[row['Camp_ID'], row['Plan_ID'], row['Num_Of_Volunteers'],row['Num_Of_Refugees'], row['Capacity'], resources[0], resources[1], resources[2], "Allocate Resources"]
            self.camps_tree.insert("", "end", values=values)

    def resource_requests_list(self):
        self.clear_content()
        self.unresolved = self.requests.get_unresolved()
        # self.unresolved = self.unresolved.sort_values(by='Date', ascending=False) ##Get elicia to store as datetime objects -> pd.to_datetime(date.today())
        request_title = tk.Label(self.root, text="Resource Requests", font=('Arial', 18))
        request_title.config(fg="medium slate blue")
        request_title.pack(pady=3)
        unresolved_title = tk.Label(self.root, text="Unresolved Requests", font=('Arial', 17))
        unresolved_title.config(fg="medium slate blue")
        unresolved_title.pack(pady=5)

        s = ttk.Style()
        s.configure('ResourceRequest.TButton', font=('Arial',12))
        unresolved_frame = tk.Frame(self.root)
        unresolved_frame.columnconfigure(0, weight=8)
        unresolved_frame.columnconfigure(1, weight=1)
        unresolved_columns = ["Camp ID", "Requester", "Food Packages Requested", "Medical Supplies Requested",
                              "Tents Requested", "Time Requested"]
        column_widths = [60, 120, 170, 170, 140, 100]

        refresh_btn = ttk.Button(self.root, text="Refresh", style='ResourceRequest.TButton', command=self.resource_requests_list)
        refresh_btn.pack(pady=2)
        grant_requests = ttk.Button(self.root, text="Allocate all requested resources", style='ResourceRequest.TButton', 
                                   command=self.grant_all_requests)
      
        grant_requests.pack()


        self.requests_tree = ttk.Treeview(unresolved_frame, columns=unresolved_columns, show="headings")
        self.requests_tree.grid(row=0, column=0)
        request_scrollbar = ttk.Scrollbar(unresolved_frame, orient="vertical", command=self.requests_tree.yview)
        # Configure the Treeview to use the scrollbar
        self.requests_tree.configure(yscrollcommand=request_scrollbar.set)
        request_scrollbar.grid(row=0, column=1)
        unresolved_frame.pack()
        for i in range(len(unresolved_columns)):
            col = unresolved_columns[i]
            self.requests_tree.heading(col, text=col)
            self.requests_tree.column(col, stretch=False, width=column_widths[i])
        for index, row in (self.unresolved[::-1].iterrows()):
            values = [row['Camp_ID'], row['Volunteer'], row['food_pac'], row['medical_sup'], row['tents'], row['date']]
            self.requests_tree.insert("", "end", values=values)
        self.requests_tree.bind("<ButtonRelease-1>", self.grant_specific_request)
  
        # completed requests
        self.resolved = self.requests.get_resolved()
        resolved_title = tk.Label(self.root, text="Resolved Requests", font=('Arial', 17))
        resolved_title.config(fg="medium slate blue")
        resolved_title.pack(pady=20)
        resolved_frame = tk.Frame(self.root)
        resolved_frame.columnconfigure(0, weight=8)
        resolved_frame.columnconfigure(1, weight=1)
        resolved_columns = ["Camp ID", "Requester", "Food Packages Requested", "Medical Supplies Requested",
                            "Tents Requested", "Time Requested"]
        column_widths = [60, 120, 170, 170, 140, 100]
        self.resolved_tree = ttk.Treeview(resolved_frame, columns=resolved_columns, show="headings")
        self.resolved_tree.grid(row=0, column=0)
        resolved_scrollbar = ttk.Scrollbar(resolved_frame, orient="vertical", command=self.resolved_tree.yview)
        # Configure the Treeview to use the scrollbar
        self.resolved_tree.configure(yscrollcommand=resolved_scrollbar.set)
        self.resolved_tree.configure(height=5)
        resolved_scrollbar.grid(row=0, column=1)
        resolved_frame.pack()
        for i in range(len(resolved_columns)):
            col = resolved_columns[i]
            self.resolved_tree.heading(col, text=col)
            self.resolved_tree.column(col, stretch=False, width=column_widths[i])
        for index, row in (self.resolved[::-1].iterrows()):
            
            values = [row['Camp_ID'], row['Volunteer'], row['food_pac'], row['medical_sup'], row['tents'], row['date']]
            self.resolved_tree.insert("", "end", values=values)
        
    def grant_all_requests(self):

        curr_unresolved = self.unresolved.copy()
        self.unresolved = self.requests.get_unresolved()
        temporary_unresolved = pd.merge(self.unresolved,curr_unresolved, how="inner")
        
        if temporary_unresolved.shape[0] == 0:
            messagebox.showinfo("Error", "Requests out of date. Refresh to see up-to-date requests")
        else:
            for index, row in (temporary_unresolved.iterrows()):
                self.admin.manual_resource_allocation(row['Camp_ID'], str(row['food_pac']), str(row['medical_sup']), str(row['tents']))
                self.requests.write_data(row['Camp_ID'])
            messagebox.showinfo("Success", "All Requested Resources Successfully Allocated!")
        self.resource_requests_list()
    
    def grant_specific_request(self, event):
        item_id = self.requests_tree.selection()
        if item_id:
            row = (self.requests_tree.item(item_id, "values"))
            self.unresolved = self.requests.get_unresolved()
            requested_resources = [row[2], row[3], row[4]]
            camp_id = row[0]
                
            
            matching_rows = self.unresolved.loc[(self.unresolved["Camp_ID"] == row[0]) & (self.unresolved["Volunteer"] == row[1]) & (self.unresolved["food_pac"].astype(int) == int(row[2])) & (self.unresolved["medical_sup"].astype(int)  == int(row[3])) & (self.unresolved["tents"].astype(int) == int(row[4])) & (self.unresolved["Resolved"] == False)]
            
            if not matching_rows.empty:

                can_allocate, suggest_resources_dict = self.admin.suggest_resources(row[0])
                if can_allocate == False:
                    messagebox.showinfo("Error", "Chosen camp now has 0 population and thus no resources can be allocated. Refresh requests to see up-to-date requests")
                    self.resource_requests_list()
                else:
                    resources = self.camps.get_resource_data(camp_id)
                    if resources == []:
                        resources = [0, 0, 0]
                    self.allocate_resources(camp_id, resources, suggest_resources_dict, requested_resources)
            else:
                messagebox.showinfo("Error", "Request is outdated. Refresh requests to see up-to-date requests")
                self.resource_requests_list()
                

    def can_allocate(self, event):
        item_id = self.camps_tree.selection()
        column = self.camps_tree.identify_column(event.x)
        if item_id and column == "#9":
            row = (self.camps_tree.item(item_id, "values"))
            camp_id = row[0]
            curr_resources = [row[5], row[6], row[7]]
            can_allocate, suggest_resources_dict = self.admin.suggest_resources(camp_id)
            if can_allocate == False:
                messagebox.showinfo("Error", "Chosen camp has 0 population and thus no resources can be allocated")
                self.manage_camps()
            else:
                request_data = self.requests.get_unresolved()
                if camp_id in request_data['Camp_ID'].values:
                    row = request_data[request_data['Camp_ID'] == camp_id].values[0]
                    requested_resources = [row[2], row[3], row[4]]
                    self.allocate_resources(camp_id, curr_resources, suggest_resources_dict, requested_resources)
                else:
                    self.allocate_resources(camp_id, curr_resources, suggest_resources_dict)
    def allocate_resources(self, camp_id, curr_resources, suggest_resources_dict, requested_resources=None):
            self.clear_content()
            if requested_resources != None:
                requested_strings = [f'Requested Food: {requested_resources[0]}', f'Requested Medical: {requested_resources[1]}', f'Requested Tents: {requested_resources[2]}']
            else:
                requested_strings = ["", "", ""]
            title_txt = f'Allocate Resources for Camp {camp_id}'
            title = tk.Label(self.root, text=title_txt, font=('Arial', 20))
            title.config(fg="medium slate blue")
            title.pack(pady=20)
            suggest_food_text = f'Suggested food supplies: {suggest_resources_dict["food"]}'
            suggest_med_text = f'Suggested medical supplies: {suggest_resources_dict["medical"]}'
            suggest_tents_text = f'Suggested tents: {suggest_resources_dict["tent"]}'
            food_lbl = tk.Label(self.root, text="Edit food supplies:", font=('Arial', 18))
            self.food_inp = ttk.Entry(self.root)
            self.food_inp.insert(0, curr_resources[0])
            suggest_food_lbl = tk.Label(self.root, text=suggest_food_text, font=('Arial', 13))
            requested_food_lbl = tk.Label(self.root, text=requested_strings[0], font=('Arial', 13))
            self.food_error = tk.Label(self.root, text="", fg="red", font=('Arial', 12))
            food_lbl.pack()
            self.food_inp.pack()
            requested_food_lbl.pack(pady=3)
            suggest_food_lbl.pack()
            self.food_error.pack(pady=(0,10))
            med_lbl = tk.Label(self.root, text="Edit medical supplies:", font=('Arial', 18))
            self.med_inp = ttk.Entry(self.root)
            self.med_inp.insert(0, curr_resources[1])
            suggest_med_lbl = tk.Label(self.root, text=suggest_med_text, font=('Arial', 13))
            requested_med_lbl = tk.Label(self.root, text=requested_strings[1], font=('Arial', 13))
            self.med_error = tk.Label(self.root, text="", fg="red", font=('Arial', 12))
            med_lbl.pack()
            self.med_inp.pack()
            requested_med_lbl.pack(pady=3)
            suggest_med_lbl.pack()
            self.med_error.pack(pady=(0,10))
            tents_lbl = tk.Label(self.root, text="Edit tents:", font=('Arial', 18))
            self.tents_inp = ttk.Entry(self.root)
            self.tents_inp.insert(0, curr_resources[2])
            suggest_tents_lbl = tk.Label(self.root, text=suggest_tents_text, font=('Arial', 13))
            requested_tents_lbl = tk.Label(self.root, text=requested_strings[2], font=('Arial', 13))
            self.tents_error = tk.Label(self.root, text="", fg="red", font=('Arial', 12))
            tents_lbl.pack()
            self.tents_inp.pack()
            requested_tents_lbl.pack(pady=3)
            suggest_tents_lbl.pack()
            
            self.tents_error.pack(pady=(0,10))
            self.submitframe = tk.Frame(self.root)
            self.submitframe.columnconfigure(0, weight=1)
            self.submitframe.columnconfigure(1, weight=1)
            self.submitframe.columnconfigure(2, weight=1)

            s = ttk.Style()
            s.configure('AllocateResources.TButton', font=('Arial',20))

            cancel_btn = ttk.Button(self.submitframe, text="Cancel", style='AllocateResources.TButton', command=self.manage_camps)            
            cancel_btn.grid(row=0, column=0, padx=20)

            submit_suggest_btn = ttk.Button(self.submitframe, text="Allocate Suggested Resources", style='AllocateResources.TButton', 
                                           command=lambda: self.submit_resources(camp_id, 
                                                                                 str(suggest_resources_dict["food"]), 
                                                                                 str(suggest_resources_dict["medical"]), 
                                                                                 str(suggest_resources_dict["tent"])))
            submit_suggest_btn.grid(row=0, column=1, padx=20)

            submit_btn = ttk.Button(self.submitframe, text="Allocate Edited Resources", style='AllocateResources.TButton',  
                                   command=lambda: self.submit_resources(camp_id, 
                                                                         self.food_inp.get(), 
                                                                         self.med_inp.get(), 
                                                                         self.tents_inp.get()))
            submit_btn.grid(row=0, column=2, padx=20)
            self.submitframe.pack()

            

    def submit_resources(self, camp_id, food_sup, med_sup, tents):
        res = self.admin.manual_resource_allocation(camp_id, food_sup, med_sup, tents)
        if res == True:
            self.food_inp.delete(0, tk.END)  # Clear the current content
            self.food_inp.insert(0, food_sup)
            self.med_inp.delete(0, tk.END)
            self.med_inp.insert(0, med_sup)
            self.tents_inp.delete(0, tk.END)
            self.tents_inp.insert(0, tents)
            self.food_error.config(text="Food supplies saved", fg="green")
            self.med_error.config(text="Medical supplies saved", fg="green")
            self.tents_error.config(text="Tents saved", fg="green")
            self.requests.write_data(camp_id)
            self.root.update_idletasks()
            messagebox.showinfo("Success", "Resources Successfully Allocated!")
            self.manage_camps()
        else:
            self.food_error.config(text=res['food'])
            self.med_error.config(text=res['medical'])
            self.tents_error.config(text=res['tent'])

        # code here to manage camp (alllocate resources etc.)

    def manage_volunteers(self):
        self.clear_content()
        # add code here to edit volunteer data
        self.volunteer_data = pd.read_csv(self.volunteer_file)
        self.users = pd.read_csv(self.users_file)
        title = tk.Label(self.root, text="Manage Volunteers", font=('Arial', 18))
        title.config(fg="medium slate blue")
        title.pack(pady=20)
        camps_ids = ["All Camps"]
        for val in self.camps_data['Camp_ID']:
            if val in camps_ids:
                continue
            camps_ids.append(val)
        self.selected_camp = tk.StringVar(self.root)
        self.selected_camp.set(camps_ids[0])
        camps_menu_lbl = tk.Label(self.root, text="Filter By Camp:", font=('Arial', 14))
        camps_menu = tk.OptionMenu(self.root, self.selected_camp, *camps_ids, command=self.filter_volunteers)
        camps_menu_lbl.pack()
        camps_menu.pack()

        s = ttk.Style()
        s.configure('ManageVolunteer.TButton', font=('Arial',17))
        all_buttons = tk.Frame(self.root, pady=20)
        all_buttons.columnconfigure(1, weight=1)
        all_buttons.columnconfigure(2, weight=1)
        activate_all_btn = ttk.Button(all_buttons, text="Activate All", style='ManageVolunteer.TButton', command=self.activate_all)
        deactivate_all_btn = ttk.Button(all_buttons, text="Deactivate All", style='ManageVolunteer.TButton', command=self.deactivate_all)
        activate_all_btn.grid(row=0, column=0,padx=10)
        deactivate_all_btn.grid(row=0, column=1)
        all_buttons.pack()
        info_lbl  = tk.Label(self.root, text="Click on items within a State or Delete column to activate / deactivate / delete an individual volunteer", font=('Arial', 14), fg="gray")
        info_lbl.pack()
        camp_columns = ["Camp ID", "Username", "First Name", "Surname", "Phone", "Age", "Availability", "State", "Delete"]
        column_widths = [70, 80, 80, 80, 80, 40, 220, 70, 70]
        self.volun_tree = ttk.Treeview(self.root, columns=camp_columns, show="headings")
        for i in range(len(camp_columns)):
            col = camp_columns[i]
            self.volun_tree.heading(col, text=col)
            self.volun_tree.column(col, width=column_widths[i], anchor=tk.CENTER)
        self.volun_tree.bind("<ButtonRelease-1>", self.individual_volunteer)
        scrollbar = ttk.Scrollbar(self.volun_tree, orient="vertical", command=self.volun_tree.yview)
        # Configure the Treeview to use the scrollbar
        self.volun_tree.configure(yscrollcommand=scrollbar.set)
        # Place the scrollbar on the right side of the Treeview
        self.volun_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.pack(side="right", fill="y")
        self.filter_volunteers()
        tk.Label(self.root, text="").pack(pady=50) ##stops table going all the way to bottom
    def activate_all(self):
        self.admin.activate_all()
        self.manage_volunteers()
    def deactivate_all(self):
        self.admin.deactivate_all()
        self.manage_volunteers()
    def filter_volunteers(self, event=None):
        for item in self.volun_tree.get_children():
            self.volun_tree.delete(item)

        selected_camp = self.selected_camp.get()
        if selected_camp == "All Camps": filtered_data = self.volunteer_data
        else:
            filtered_data = self.volunteer_data[self.volunteer_data["CampID"] == selected_camp]
        if not filtered_data.empty:
            for index, row in (filtered_data.iterrows()):
                days = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]
                availability_array = []
                availability =  str(row['Availability']).zfill(7)
                for i in range(len(availability)):
                    if availability[i] == "1":
                        availability_array.append(days[i])
                if len(availability_array) == 7:
                    availability_string = "All Days"
                elif len(availability_array) == 0:
                    availability_string = "No Days"
                else:
                    if len(availability_array) == 2:
                        availability_string = f'{availability_array[0]} and {availability_array[1]}'
                    else:
                        availability_string = ", ".join(availability_array)
                state = self.users[self.users["Username"] == row["Username"]]["Active"].values[0]
                if state: state = "Active"
                else: state = "Inactive"
                values=[row['CampID'], row['Username'], row['First Name'], row['Last Name'],row['Phone'], row['Age'], availability_string, state, "Delete?"]
                self.volun_tree.insert("", "end", values=values)

    def individual_volunteer(self, event):
        item_id = self.volun_tree.selection()
        column = self.volun_tree.identify_column(event.x)
        if item_id and column == "#8":
            row = (self.volun_tree.item(item_id, "values"))
            self.activate_deactivate(row)
        elif item_id and column == "#9":
            row = (self.volun_tree.item(item_id, "values"))
            self.delete_volunteer(row[1],row[0])

    def activate_deactivate(self, row):
        username = row[1]
        if row[-2] == "Active":
            volunteer_choice = messagebox.askyesno(title="Manage Volunteer", message=f"Deactivate {username}'s Account:\n")
            if volunteer_choice == True:
                self.admin.deactivate_account(username)
                # self.root.update_idletasks()
                self.manage_volunteers()
        else:
            volunteer_choice = messagebox.askyesno(title="Manage Volunteer", message=f"Activate {username}'s Account:\n")
            if volunteer_choice == True:
                self.admin.activate_account(username)
                # self.root.update_idletasks()
                self.manage_volunteers()
            
    def delete_volunteer(self, username,camp_id):
        volunteer_choice = messagebox.askyesno(title="Manage Volunteer", message=f"Delete {username}'s Account:\n" )
        if volunteer_choice == True:
            self.admin.delete_account(username,camp_id)
            # self.root.update_idletasks()
            self.manage_volunteers()

    def display_resources_graph(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Resources Data Visualisation")
        new_window.geometry("1400x800")
        
        fig = create_resources_bar_graph()
        
        if fig is not None:
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def display_refugee_graph_camps(self):
        self.display_graphs("camps","refugees")

    def display_volunteer_graph_camps(self):
        self.display_graphs("camps","volunteers")
        
    def display_refugee_graph_plans(self):
        self.display_graphs("plans","refugees")

    def display_volunteer_graph_plans(self):
        self.display_graphs("plans","volunteers")
        
    def display_resources_camps(self):
        self.display_resources_graph()

    def display_graphs(self, camps_or_plans, volunteers_or_refugees):
        self.camps_or_plans = camps_or_plans
        self.volunteers_or_refugees = volunteers_or_refugees
        new_window = tk.Toplevel(self.root)
        new_window.title("Camp Data Visualisation")
        new_window.geometry("800x800")
        
        fig = create_bar_graph(self.camps_or_plans, self.volunteers_or_refugees)
        
        if fig is not None:
            canvas = FigureCanvasTkAgg(fig, master=new_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
    def clear_content(self):
        for widget in self.root.winfo_children():
            if widget not in self.nav_bar:
                widget.destroy()

    def logout(self):
        self.root.destroy()
        self.loginwindow.deiconify() 

    def run(self):
    
        self.root.mainloop()

