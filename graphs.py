######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     03/11/2022
# Project:  Distribution system coordination
######################################################################################################################

import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import os
from tkinter import messagebox
import regex as re


def create_plots(num_systems):
    chart_window = tk.Tk()
    chart_window.title("Charts")
    chart_window.iconbitmap(r"C:/Users/sakit/Documents/Academic/Research/CoordinationSystem/CoordinationDisSys/DisSys/images/chartIcon.ico")
    chart_window.geometry("900x500")
    chart_window.config(bg="#80c1ff")

    def display_variables(event):

        def select_variable(var_event):

            def plot_variable():

                var_list = []
                for item in listbox_system_variable_names.curselection():
                    var_list.append(str(listbox_system_variable_names.get(item)))

                if len(var_list) == 0:
                    messagebox.showerror("Selection Error!", "Select at least one variable name from the variable names list")

                if len(var_list) == 1:
                    plt.plot(data[var_list[0]], marker='o')
                    plt.title("Convergence of " + var_list[0] + "\n", fontsize=14)
                    plt.xlabel('Iteration count')
                    plt.ylabel(var_list[0])

                else:
                    for item in var_list:
                        plt.plot(data[item],  marker='o')
                        plt.title("Convergence comparison \n", fontsize=14)
                        plt.xlabel('Iteration count')
                    plt.legend(var_list, loc=0)

                plt.show()

            button_plot = tk.Button(chart_window, text="Plot", command=plot_variable, bg="white", fg="black")
            button_plot.place(relx=0.6, rely=0.44, relwidth=0.08, relheight=0.05)

            button_clear = tk.Button(chart_window, text="Clear", command=lambda: listbox_system_variable_names.select_clear(0, 'end'), bg="white", fg="black")
            button_clear.place(relx=0.6, rely=0.51, relwidth=0.08, relheight=0.05)

        data = pd.read_csv(listbox_network_attributes.get('anchor') + ".csv")

        label_system_variable_names = tk.Label(chart_window, text="Variable Names", anchor='w', bd=5)
        label_system_variable_names.place(relx=0.28, rely=0.01, relwidth=0.22, relheight=0.05)

        listbox_system_variable_names = tk.Listbox(chart_window, exportselection=0, selectmode='multiple')
        listbox_system_variable_names.place(relx=0.28, rely=0.06, relwidth=0.22, relheight=0.9)
        listbox_system_variable_names.bind("<<ListboxSelect>>", select_variable)

        scrollbar_system_variable_list = tk.Scrollbar(listbox_system_variable_names, orient="vertical")
        listbox_system_variable_names.config(yscrollcommand=scrollbar_system_variable_list.set)
        scrollbar_system_variable_list.config(command=listbox_system_variable_names.yview)
        scrollbar_system_variable_list.pack(side="right", fill="y")

        for col_name in data.columns:
            listbox_system_variable_names.insert('end', col_name)

    label_network_attributes = tk.Label(chart_window, text="Network Attributes", anchor='w', bd=5)
    label_network_attributes.place(relx=0.01, rely=0.01, relwidth=0.22, relheight=0.05)

    listbox_network_attributes = tk.Listbox(chart_window, exportselection=0)
    listbox_network_attributes.place(relx=0.01, rely=0.06, relwidth=0.22, relheight=0.9)
    listbox_network_attributes.bind("<<ListboxSelect>>", display_variables)

    scrollbar_network_attributes_list = tk.Scrollbar(listbox_network_attributes, orient="vertical")
    listbox_network_attributes.config(yscrollcommand=scrollbar_network_attributes_list.set)
    scrollbar_network_attributes_list.config(command=listbox_network_attributes.yview)
    scrollbar_network_attributes_list.pack(side="right", fill="y")

    listbox_network_attributes.insert('end', "Transmission_System")

    for file in os.listdir():
        if "Transmission_System" not in file and ".csv" in file:
            listbox_network_attributes.insert('end', file.split('.')[0])
            if re.search(r'\d+', file).group() == str(num_systems):
                break

    button_exit = tk.Button(chart_window, text="Exit", command=chart_window.destroy, bg="white", fg="black")
    button_exit.place(relx=0.9, rely=.93, relwidth=0.08, relheight=0.05)

    chart_window.mainloop()
