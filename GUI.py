######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     03/08/2022
# Project:  Distribution system coordination
######################################################################################################################

import PySimpleGUI as sg
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os

from analysis import display_graphs
from userInputs import user_inputs


def main_frame(root):
    # assign values for the command line inputs from user
    def submit_network_data():

        directory = ""
        network_name = ""
        system_name = ""
        num_systems = 0

        if not label_directory_display["text"] == "" and os.path.exists(label_directory_display["text"]):
            directory = label_directory_display["text"]
            input_dir = directory + r"/inputData/"
            if not entry_network.get() == "" and os.path.exists(input_dir + entry_network.get() + r"/"):
                network_name = entry_network.get()
                input_dir = input_dir + network_name + r"/"
                if not entry_system.get() == "" and os.path.exists(input_dir + entry_system.get() + str(1) + r"/"):
                    system_name = entry_system.get()
                    if not int(label_num_system_num['text']) == 0 and len(os.listdir(input_dir)) > int(
                            label_num_system_num['text']):
                        num_systems = int(label_num_system_num['text'])
                    else:
                        response_system_number = messagebox.askokcancel("System Error!",
                                                                        f"{len(os.listdir(input_dir)) - 1} systems available. "
                                                                        f"\n Continue with {len(os.listdir(input_dir)) - 1} systems?")
                        if response_system_number == 1:
                            num_systems = len(os.listdir(input_dir)) - 1
                        else:
                            pass
                else:
                    messagebox.showerror("System Error!", "System does not exit.")
            else:
                messagebox.showerror("System Error!", "Network does not exit.")
        else:
            messagebox.showerror("System Error!", "Directory does not exist.")

        # reading command line arguments
        if not (directory == "" or network_name == "" or system_name == "" or num_systems == 0):
            user_inputs(directory, network_name, system_name, num_systems, root)

    def clear_all_inputs():
        label_directory_display["text"] = " "
        entry_network.delete(0, 'end')
        entry_system.delete(0, 'end')
        label_num_system_num['text'] = "0"
        scale_num_system.set(0)
        scale_num_system.config(state="disabled")

    def update_num_systems(value):
        label_num_system_num['text'] = scale_num_system.get()

    def search_directory():
        filename = filedialog.askdirectory(
            initialdir=r"C:/Users/sakit/Documents/Academic/Research/CoordinationSystem/CoordinationDisSys",
            title="Select a directory")
        label_directory_display["text"] = filename
        scale_num_system.config(state="normal")

    canvas_user_inputs = tk.Canvas(root, bg="#80c1ff")
    canvas_user_inputs.place(relx=0.075, rely=0.035, relwidth=0.87, relheight=0.25)

    label_directory = tk.Label(root, text="Directory:", anchor='w', bd=5)
    label_directory.place(relx=0.01, rely=0.01, relwidth=0.14, relheight=0.05)

    label_directory_display = tk.Label(root, bg='white', anchor='w', relief="sunken")
    label_directory_display.place(relx=0.16, rely=0.01, relwidth=0.73, relheight=0.05)

    button_browse = tk.Button(root, text="Browse", command=search_directory, bg="white", fg="black")
    button_browse.place(relx=0.90, rely=0.01, relwidth=0.08, relheight=0.05)

    label_network = tk.Label(root, text="Network Name:", anchor='w', bd=5)
    label_network.place(relx=0.01, rely=0.07, relwidth=0.14, relheight=0.05)

    entry_network = tk.Entry(root)
    entry_network.place(relx=0.16, rely=0.07, relwidth=0.73, relheight=0.05)

    label_system = tk.Label(root, text="System Name:", anchor='w', bd=5)
    label_system.place(relx=0.01, rely=0.14, relwidth=0.14, relheight=0.05)

    entry_system = tk.Entry(root)
    entry_system.place(relx=0.16, rely=0.14, relwidth=0.73, relheight=0.05)

    label_num_system = tk.Label(root, text="Number of Systems:", anchor='w', bd=5)
    label_num_system.place(relx=0.01, rely=0.20, relwidth=0.14, relheight=0.05)

    scale_num_system = tk.Scale(root, from_=0, to=10, orient="horizontal", showvalue=False,
                                command=update_num_systems,
                                state="disabled")
    scale_num_system.place(relx=0.22, rely=0.20, relwidth=0.67, relheight=0.05)

    label_num_system_num = tk.Label(root, text="0", bd=5)
    label_num_system_num.place(relx=0.16, rely=0.20, relwidth=0.05, relheight=0.05)

    button_submit = tk.Button(root, text="Submit", command=submit_network_data, bg="white", fg="black")
    button_submit.place(relx=0.4, rely=0.26, relwidth=0.08, relheight=0.05)

    button_clear = tk.Button(root, text="Clear", command=clear_all_inputs, bg="white", fg="black")
    button_clear.place(relx=0.5, rely=0.26, relwidth=0.08, relheight=0.05)
