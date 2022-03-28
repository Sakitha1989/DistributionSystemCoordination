######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     03/11/2022
# Project:  Distribution system coordination
######################################################################################################################

import tkinter as tk


def create_plots():
    chart_window = tk.Toplevel()
    chart_window.title("Charts")
    chart_window.iconbitmap(r"C:/Users/sakit/Documents/Academic/Research/CoordinationSystem/CoordinationDisSys/DisSys/images/chartIcon.ico")
    chart_window.geometry("900x500")
    chart_window.config(bg="#80c1ff")

    button_exit = tk.Button(chart_window, text="Exit", command=chart_window.destroy, bg="white", fg="black")
    button_exit.place(relx=0.9, rely=.93, relwidth=0.08, relheight=0.05)
