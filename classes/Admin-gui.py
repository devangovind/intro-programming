from Admin import Admin
import tkinter as tk
from tkinter import END
from tkinter import messagebox
from tkcalendar import *

class AdminGui:
    def __init__(self, admin):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Volunteer View")
        self.admin = admin
        # self.volunteer_data = self.volunteer.get_volunteer_data()
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
        self.create_plan_btn = tk.Button(self.headerarea, text="Create New Plan", font=('Arial', 16), command=self.create_new_plan)
        self.create_plan_btn.grid(row=0, column=1)
        self.display_plans_btn = tk.Button(self.headerarea, text="Display Existing Plans", font=('Arial', 16), command=self.display_plans)
        self.display_plans_btn.grid(row=0, column=2)
        self.manage_camps_btn = tk.Button(self.headerarea, text="Manage Camps", font=('Arial', 16), command=self.manage_camps)
        self.manage_camps_btn.grid(row=0, column=3)
        self.manage_volunteers_btn = tk.Button(self.headerarea, text="Manage Volunteers", font=('Arial', 16), command=self.manage_volunteers)
        self.manage_volunteers_btn.grid(row=0, column=4)
        self.logout_btn = tk.Button(self.headerarea, text="Logout", font=('Arial', 16))
        self.logout_btn.grid(row=0, column=5)
        self.headerarea.pack(padx=20)
        self.nav_bar = [self.headerarea, self.home_btn,self.display_plans_btn, self.create_plan_btn, self.manage_camps_btn, self.manage_volunteers_btn, self.logout_btn]
    def welcome_message(self):
        self.clear_content()
        welcome_back = f'Welcome Back, Admin'
        label = tk.Label(self.root, text=welcome_back, font=('Arial', 24))
        label.pack(pady=100)

    def create_new_plan(self):
        self.clear_content()
        # add the code for creating a new plan here

        self.clear_content()
        # add_plan_window = Toplevel()
        # add_plan_window.geometry('400x400+600+300')
        self.Plan_ID = tk.StringVar()
        self.Description = tk.StringVar()
        self.Location = tk.StringVar()
        # self.Start_Date = tk.StringVar()
        # self.End_Date = tk.StringVar()
        tk.Label(self.root,text='Add a new plan').place(x=50, y=40)
        tk.Label(self.root,text='Plan_ID:').place(x=50, y=60)
        tk.Entry(self.root, width=30, textvariable=self.Plan_ID).place(x=50, y=80)
        tk.Label(self.root, text='Description:').place(x=50, y=100)
        tk.Entry(self.root, width=30, textvariable=self.Description).place(x=50, y=120)
        tk.Label(self.root, text='Location:').place(x=50, y=140)
        tk.Entry(self.root, width=30, textvariable=self.Location).place(x=50, y=160)
        tk.Label(self.root, text='Start_Date:').place(x=50, y=180)
        date_button = tk.Button(self.root,text = 'choose the date',command=self.pick_date).place(x=350, y=160)

        self.start_date = tk.Entry(self.root, width=30)
        self.start_date.place(x=50, y=200)
        self.start_date.insert(0,'dd/mm/yyyy')



        tk.Label(self.root, text='End_Date:').place(x=50, y=220)
        tk.Entry(self.root, width=30).place(x=50, y=240)
        tk.Button(self.root, text='Save this plan', command=self.save_data).place(x=150, y=300)
    def pick_date(self):

        self.date_window = tk.Toplevel()
        self.date_window.grab_set()
        self.date_window.geometry('250x220+590+370')
        self.cal = Calendar(self.date_window,selectmode='day',year=2023, month=11, day=16)
        self.cal.place(x=0,y=0)
        submit_btn = tk.Button(self.date_window,text = 'submit',command=self.grab_date)
        submit_btn.place(x=80,y=190)
    def grab_date(self):
        self.s_date = self.cal.selection_get()
        self.start_date.delete(0,END)
        self.start_date.insert(0,self.s_date)
        self.date_window.destroy()
        # date = self.cal.get_date()
        print(type(self.s_date))
        print(self.admin.is_date(self.s_date))
        pass

    def save_data(self):
        Plan_ID_ = self.Plan_ID.get()
        Description_ = self.Description.get()
        Location_= self.Location.get()
        Start_date_= self.Start_Date.get()
        End_date_ = self.End_Date.get()
        plan_ = [{'Plan_ID': Plan_ID_,'Description':Description_,'Location':Location_,'Start Date':Start_date_,'End Date':End_date_}] # 空字典
        header = ['Plan_ID', 'Description', 'Location', 'Start Date', 'End Date']
        with open('plan_file.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)

            writer.writerows(plan_)

    def display_plans(self):
        self.clear_content()


        # add code here:
        # somewhere in here will be the end button for the individual plans which will maybe go to another function

        header = ['plan_ID', 'Description', 'Location', 'Start Date', 'End Date']
        table = ttk.Treeview(self.root)
        self.root.table = table
        table.configure(columns=header, show='headings')
        for item in header:
            table.column(item, width=120, anchor=tk.CENTER)
            table.heading(item, text=item)

        self.root.table.pack(fill=tk.BOTH, expand=True)
        # tk.Button(self.root, text='Add a new plan').pack(side='left', pady=20)
        tk.Button(self.root, text='End a plan').pack(side='left', pady=20)
        tk.Button(self.root, text='Refresh plans ').pack(side='left', pady=20)
        # plan_data = PlanData()
        index = 0
        for plan in self.plan_data_:
            # print(plan)
            self.root.table.insert('', index + 1, values=(plan['Plan_ID'], plan['Description'],
                                                     plan['Location'], plan['Start Date'], plan['End Date']))


    def manage_camps(self):
        self.clear_content()
        # code here to manage camp (alllocate resources etc.)
        
    def manage_volunteers(self):
        self.clear_content()
        # add code here to edit volunteer data

    

    def clear_content(self):
        for widget in self.root.winfo_children():
            if widget not in self.nav_bar:
                widget.destroy()
    def run(self):
    
        self.root.mainloop()

dummy = Admin()
VGui = AdminGui(dummy)
VGui.run()

