import tkinter as tk
from tkinter import messagebox
import csv
import re
from tkinter import *
from tkcalendar import *
from tkinter import ttk
from tkinter import *


class PlanData:
    def __init__(self):
        with open('plan_file_.csv', 'r', encoding='utf-8') as plan_file:
            # read = csv.reader(plan_file)
            read = csv.DictReader(plan_file)
            self.plan_list = []
            for row in read:
                self.plan_list.append(row)
            # print(plan_list)

    def plan(self):
        return self.plan_list
class ManageMenu:
    # Menu window configration
    def __init__(self):
        manage_win = Tk()
        self.root = manage_win
        self.root.title('Admin manage window')
        self.root.geometry('300x400+600+300')
        self.root.resizable(False, False)
        self.create_button()
        manage_win.mainloop()

    def create_button(self):

        Label(self.root, text='This can be xxxx xxxx').pack(pady=20, ipady=20)
        Button(self.root, text='Manage Plan', command=self.show_view_win).pack(pady=8)
        Button(self.root, text='Manage volunteers').pack(pady=8)
        Button(self.root, text='Manage resources').pack(pady=8)

    def show_view_win(self):
        self.root.destroy()
        PlanWin()

class PlanWin:
    def __init__(self):
        plan_win = Tk()
        self.root = plan_win
        self.root.title('Admin manage window')
        self.root.geometry('650x350+400+300')
        self.root.resizable(False, False)
        self.plan_menu()


        self.init_frame()
        self.root.mainloop()
    def init_frame(self):

        self.welcomeFrame = IntroductionFrame(self.root)
        self.view_plan_frame = ViewPlan(self.root)



        self.introduction_plan()
    def change_page(self,frame):
        self.current_page.pack_forget()
        self.current_page = frame
        self.view_plan_frame.pack()
    def plan_menu(self):
        # self.view_plan_frame = ViewPlan(self.root)

        menubar = Menu(self.root)
        menubar.add_command(label='plan information', command=self.show_view_plan)
        menubar.add_command(label='camp information')
        menubar.add_command(label='Back to Admin menu',command = self.back_main_menu)


        self.root['menu'] = menubar

    def introduction_plan(self):
        self.current_page = self.welcomeFrame
        self.current_page.pack()
    def show_view_plan(self):
       self.change_page(self.view_plan_frame)
    #



    def back_main_menu(self):
        self.root.destroy()
        ManageMenu()
class IntroductionFrame(Frame):
    def __init__(self,plan_win):
        super().__init__(plan_win)
        Label(self, text='Welcome to use this functionality,you can check,manage the plan information and plan details about camp').pack(pady=60,ipady=30)


class ViewPlan(Frame):
    def __init__(self, plan_win):
        super().__init__(plan_win)
        self.table_view = Frame()
        self.table_view.pack()
        self.creat_table_page()
        self.show_date_frame()

    def creat_table_page(self):
        header = ['plan_ID', 'Description', 'Location', 'Start Date', 'End Date']
        table = ttk.Treeview(self)
        self.table = table
        table.configure(columns=header, show='headings')
        for item in header:
            table.column(item, width=120, anchor=CENTER)
            table.heading(item, text=item)

        self.table.pack(fill=BOTH, expand=True)
        Button(self, text='Add a new plan', command=self.add_plan).pack(side='left', pady=20)
        Button(self, text='End a plan').pack(side='left', pady=20)
        Button(self, text='Refresh plans ', command=self.show_date_frame).pack(side='left', pady=20)
    def show_date_frame(self):
        for _ in map(self.table.delete, self.table.get_children('')):
            pass
        plan_data = PlanData()
        plan_data_=plan_data.plan()
        index = 0
        for plan in plan_data_:
            # print(plan)
            self.table.insert('', index + 1, values=(plan['Plan_ID'], plan['Description'],
                                                     plan['Location'], plan['Start Date'], plan['End Date']))


    def add_plan(self):
        add_plan_window = Toplevel()
        add_plan_window.geometry('400x400+600+300')
        self.Plan_ID = StringVar()
        self.Description = StringVar()
        self.Location = StringVar()
        self.Start_Date = StringVar()
        self.End_Date = StringVar()
        Label(add_plan_window, text='Add a new plan').place(x=50,y=40)
        Label(add_plan_window, text='Plan_ID:').place(x=50,y=60)
        Entry(add_plan_window, width=30, textvariable=self.Plan_ID).place(x=50,y=80)
        Label(add_plan_window, text='Description:').place(x=50,y=100)
        Entry(add_plan_window, width=30, textvariable=self.Description).place(x=50,y=120)
        Label(add_plan_window, text='Location:').place(x=50,y=140)
        Entry(add_plan_window, width=30, textvariable=self.Location).place(x=50,y=160)
        Label(add_plan_window, text='Start_Date:').place(x=50,y=180)
        Entry(add_plan_window, width=30, textvariable=self.Start_Date).place(x=50,y=200)
        Label(add_plan_window, text='End_Date:').place(x=50,y=220)
        Entry(add_plan_window, width=30, textvariable=self.End_Date).place(x=50,y=240)
        Button(add_plan_window, text='Save this plan').place(x=150,y=300)




if __name__ == '__main__':
    ManageMenu()