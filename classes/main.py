import sys
import subprocess

packages = ["geopandas", "matplotlib", "tkcalender", "pandas"]
for package in packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.call([sys.executable, "-m", "pip", "install", package])

from login_gui import Login
import tkinter as tk
from tkinter import *

root = Tk()
login = Login(root)
root.mainloop()
