from login_gui import Login
import tkinter as tk
from tkinter import *
import sys
import subprocess
packages = ["geopandas", "matplotlib", "tkcalender"]
if sys.platform == "win32": 
    pip_var = 'pip'
else: 
    pip_var = "pip3"
for package in packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.call([sys.executable, "-m", pip_var, "install", package])

if __name__ == "__main__":
    root = Tk()
    login = Login(root)
    root.mainloop()