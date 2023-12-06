import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import tkinter as tk
import geopandas
import pandas as pd

def create_pie_chart(data, labels, title):
    colors = ['#1f77b466', '#ff7f0e66', '#2ca02c66']  # Blue, Orange, Green
    explode = [0.05] * len(data)  # To slightly separate the slices

    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        data,
        autopct='%1.1f%%',  # Show one decimal place
        startangle=90,
        colors=colors,
        explode=explode,  # Separate slices
        pctdistance=0.85,  # Percentage placement
        wedgeprops=dict(width=0.3)  # Donut width
    )

    plt.setp(autotexts, size=10, weight="bold", color="white")  # Set the properties for the autopct

    # Draw a circle at the center to make it a donut chart
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie chart is drawn as a circle
    ax.axis('equal')

    # Add a legend
    legend_labels = labels
    ax.legend(wedges, legend_labels, title="Resources", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), frameon=False)

    # plt.title(title)
    # plt.tight_layout(rect=[0, 0.03, 0.75, 0.95])  # Adjust as needed
    # plt.show()
    
    return fig
    
    
def create_bar_graph(camps_or_plans, vol_or_ref):
    """ Takes camps or plans and volunteers or refugees as arguments and displays volunteers or refugees (y axis) plotted against camps or plans (x axis).
    Can use plt.show or wire into Tkinter using FigureCanvasTkAgg from matplotlib backends

    Args:
        camps_or_plans (str): specifies camps or plans as the x axis
        vol_or_ref (str): specifies volunteers or refugees as the y axis

    Returns:
        bar graph figure
    """
    
    # Takes camps or plans and volunteers or refugees and outputs a figure into tkinter
    x_axis_variable = []
    y_axis_variable = []
    
    try:
        with open("./files/camps_file.csv") as file:
            csv_reader = csv.reader(file)
            next(csv_reader) # Skips header row
            for row in csv_reader:
                camp, refugee, volunteer, camp_capacity, plan = row
                if camps_or_plans == "camps":
                    x_axis_variable.append(camp)
                elif camps_or_plans == "plans":
                    x_axis_variable.append(plan)
                if vol_or_ref == "refugees":
                    y_axis_variable.append(int(refugee))
                elif vol_or_ref == "volunteers":
                    y_axis_variable.append(int(volunteer))
    except FileNotFoundError:
        return None
    
    # plt.bar(x_axis_variable, y_axis_variable, width=0.8)
    # plt.xlabel(camps_or_plans.capitalize())
    # plt.xticks(rotation=45, ha='left')
    # plt.ylabel(vol_or_ref.capitalize())
    # plt.title(f"{vol_or_ref.capitalize()} split by {camps_or_plans.capitalize()}")
    # plt.show()
    
    fig = Figure(figsize=(6,4))
    ax = fig.add_subplot(111)
    ax.bar(x_axis_variable, y_axis_variable, width=0.8)
    ax.set_xlabel(camps_or_plans.capitalize())
    ax.set_xticklabels(x_axis_variable, rotation=45, ha="center")
    ax.set_ylabel(vol_or_ref.capitalize())
    ax.set_title(f"{vol_or_ref.capitalize()} within each of the {camps_or_plans}")

    return fig

def create_resources_bar_graph():
    
    camps = []
    food_packs = []
    medical_sups = []
    tents = []
    
    try:
        with open("./files/resources.csv") as file:
            csv_reader = csv.reader(file)
            next(csv_reader) # Skips header row
            for row in csv_reader:
                Camp_ID,food_pac,medical_sup,tent = row
                camps.append(Camp_ID)
                food_packs.append(int(food_pac))
                medical_sups.append(int(medical_sup))
                tents.append(int(tent))
    except FileNotFoundError:
        return None
    
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    axs[0].bar(camps, food_packs, color="blue")
    axs[0].set_title("Food Packs")
    axs[0].set_xlabel("Camp ID")
    axs[0].set_ylabel("Number")
    axs[0].set_xticklabels(camps,rotation=45, ha="center")

    axs[1].bar(camps, medical_sups, color="red")
    axs[1].set_title('Medical Supplies')
    axs[1].set_xlabel("Camp ID")
    axs[1].set_ylabel("Number")
    axs[1].set_xticklabels(camps,rotation=45, ha="center")
    
    axs[2].bar(camps, tents, color="purple")
    axs[2].set_title("Tents")
    axs[2].set_xlabel("Camp ID")
    axs[2].set_ylabel("Number")
    axs[2].set_xticklabels(camps,rotation=45, ha="center")
    
    plt.tight_layout()

    return fig



def create_world_map():

    df_plans = pd.read_csv("./files/plans_file.csv") # Load data

    df_locations = pd.read_csv("./files/countries.csv")
    
    df_merged = pd.merge(df_plans, df_locations, on='Location') # Merge data
    worldmap = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres")) # Load world map
    
    fig, ax = plt.subplots(figsize=(16, 10))
    worldmap.plot(color="lightgrey", ax=ax)
    
    # for _, row in df_merged.iterrows():
    #     plt.plot(row["Longitude"], row["Latitude"], marker='o', color='red', markersize=5)
    # print(df_merged)
    # x = df_merged["Longitude"]
    # y = df_merged["Latitude"]

    # plt.xlim([-180, 180])
    # plt.ylim([-90, 90])
    # plt.title("Geographical locations of each plan")
    # plt.xlabel("Longitude")
    # plt.ylabel("Latitude")
    # plt.show()
    
    for _, row in df_merged.iterrows():
        ax.plot(row["Longitude"], row["Latitude"], marker='o', color='red', markersize=5) # Iterates through merged dataframe
    
    x = df_merged["Longitude"]
    y = df_merged["Latitude"]

    ax.set_xlim([-180, 180])
    ax.set_ylim([-90, 90])
    ax.set_title("Geographical locations of each plan")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    
    return fig
    
# def display_bar_graph_tkinter_test(): # For more info see https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html#sphx-glr-gallery-user-interfaces-embedding-in-tk-sgskip-py
#     root = tk.Tk() # Create tkinter window
#     root.title("Bar Graph in Tkinter")
    
#     fig = create_bar_graph("camps", "volunteers") # create figure using above function
    
#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas.draw()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
#     root.mainloop()
    
# def display_world_map_tkinter_test():
#     root = tk.Tk()
#     root.title("Geographical locations of each plan")
    
#     fig = create_world_map()
    
#     canvas = FigureCanvasTkAgg(fig, master=root)
#     canvas.draw()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    
#     root.mainloop()
# if __name__ == "__main__":
#     display_world_map_tkinter_test()