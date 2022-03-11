######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     03/08/2022
# Project:  Distribution system coordination
######################################################################################################################

import os
import tkinter as tk
from tkinter import messagebox

from loops import read_system_data, main_loop
from graphs import create_plots


def user_inputs(directory, network_name, system_name, num_systems, root) -> None:
    input_dir = directory + r"/inputData/" + network_name + r"/"
    output_dir = directory + r"/outputData/" + network_name + r"/"

    # Create system folder in the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        messagebox.showinfo("New Output Directory", "Output directed created.")

    os.chdir(output_dir)

    # reading and creating distribution systems
    distribution_systems = read_system_data(input_dir, system_name, num_systems)

    network_details(root, distribution_systems)

    algorithm_parameters(root, distribution_systems, input_dir, network_name, num_systems)


def network_details(root, distribution_systems):

    def display_details(event):

        selection = event.widget.curselection()
        if selection:
            for system in distribution_systems:
                if event.widget.get(selection[0]) == system.name:
                    label_display_details_heading.config(anchor='w', justify='left', text="\t\tSystem Details")
                    label_information.config(text=f"System name: \t\t\t{system.name} \n"
                                                  f"Number of buses: \t\t\t{system.numBuses} \n"
                                                  f"Number of generators: \t\t{system.numGenerators} \n"
                                                  f"Number of loads: \t\t\t{system.numLoads} \n"
                                                  f"Number of distribution lines: \t\t{system.numDistributionLines} \n"
                                                  f"Number of transmission lines: \t{system.numTransmissionLines}")
        else:
            label_information.config(text="")

    label_distribution_systems_listbox = tk.Label(root, text="System List:", anchor='w', bd=5)
    label_distribution_systems_listbox.place(relx=0.01, rely=0.3, relwidth=0.14, relheight=0.05)

    # label_display_details = tk.Label(root, text="System Details", bd=5)
    # label_display_details.place(relx=0.16, rely=0.3, relwidth=0.14, relheight=0.05)

    listbox_distribution_systems = tk.Listbox(root)
    listbox_distribution_systems.place(relx=0.01, rely=0.36, relwidth=0.14, relheight=0.25)
    listbox_distribution_systems.bind("<<ListboxSelect>>", display_details)

    scrollbar_distribution_systems_list = tk.Scrollbar(listbox_distribution_systems, orient="vertical")
    listbox_distribution_systems.config(yscrollcommand=scrollbar_distribution_systems_list.set)

    scrollbar_distribution_systems_list.config(command=listbox_distribution_systems.yview)
    scrollbar_distribution_systems_list.pack(side="right", fill="y")

    for system in distribution_systems:
        listbox_distribution_systems.insert('end', system.name)

    label_display_details_heading = tk.Label(root, text="Select a system", anchor='n', justify='center', font=("", "10"), bd=2)
    label_display_details_heading.place(relx=0.16, rely=0.36, relwidth=0.73, relheight=0.04)

    label_information = tk.Label(root, anchor='nw', justify='left', font=("", "10"))
    label_information.place(relx=0.16, rely=0.4, relwidth=0.73, relheight=0.21)


def algorithm_parameters(root, distribution_systems, input_dir, network_name, num_systems):
    def solve():

        results = {}
        num_iterations = 0
        deviation_penalty = 0.0
        tolerance = 0.0

        try:
            if int(entry_num_iteration.get()) > 0:
                num_iterations = int(entry_num_iteration.get())
            else:
                raise ValueError
            try:
                if float(entry_deviation_penalty.get()) >= 0:
                    deviation_penalty = float(entry_deviation_penalty.get())
                else:
                    raise ValueError
                try:
                    if 0 <= float(entry_tolerance.get()) < 1:
                        tolerance = float(entry_tolerance.get())
                    else:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Invalid Entry!", "Tolerance must be a positive value between 0 and 1")
            except ValueError:
                messagebox.showerror("Invalid Entry!", "Deviation penalty must be a positive value greater than 1")
        except ValueError:
            messagebox.showerror("Invalid Entry!", "Number of iteration must be a positive integer greater than 0.")

        if not (num_iterations == 0 or deviation_penalty == 0.0 or tolerance == 0.0):
            results = main_loop(distribution_systems, input_dir, network_name, num_systems, num_iterations, deviation_penalty, tolerance)

        cost_gap = "${:,.2f}".format((results['total_cost'][results['iteration_count'] - 1] - results['total_cost'][results['iteration_count']]) / results['total_cost'][results['iteration_count'] - 1])
        final_cost = "${:,.2f}".format(results['total_cost'][results['iteration_count']])

        label_results.config(text=f"Iteration count: {results['iteration_count'] + 1} \n"
                                  f"Achieved cost gap: {cost_gap} \n"
                                  f"Final total cost: {final_cost}")

        button_charts.config(state="normal")

    def charts():
        create_plots()

    canvas_user_inputs = tk.Canvas(root, bg="#80c1ff")
    canvas_user_inputs.place(relx=0.075, rely=0.65, relwidth=0.87, relheight=0.26)

    label_num_iterations = tk.Label(root, text="Number of Iterations:", anchor='w', bd=5)
    label_num_iterations.place(relx=0.01, rely=0.67, relwidth=0.14, relheight=0.05)

    entry_num_iteration = tk.Entry(root)
    entry_num_iteration.place(relx=0.16, rely=0.67, relwidth=0.1, relheight=0.05)

    label_deviation_penalty = tk.Label(root, text="Deviation Penalty:", anchor='w', bd=5)
    label_deviation_penalty.place(relx=0.01, rely=0.74, relwidth=0.14, relheight=0.05)

    entry_deviation_penalty = tk.Entry(root)
    entry_deviation_penalty.place(relx=0.16, rely=0.74, relwidth=0.1, relheight=0.05)

    label_tolerance = tk.Label(root, text="Tolerance:", anchor='w', bd=5)
    label_tolerance.place(relx=0.01, rely=0.81, relwidth=0.14, relheight=0.05)

    # termination criteria
    entry_tolerance = tk.Entry(root)
    entry_tolerance.place(relx=0.16, rely=0.81, relwidth=0.1, relheight=0.05)

    button_solve = tk.Button(root, text="Solve", command=solve, bg="white", fg="black")
    button_solve.place(relx=0.17, rely=0.88, relwidth=0.08, relheight=0.05)

    label_results = tk.Label(root, anchor='w', justify='left', font=("", "12"), bd=10)
    label_results.place(relx=0.27, rely=0.67, relwidth=0.62, relheight=0.19)

    button_charts = tk.Button(root, text="Charts", command=charts, bg="white", fg="black", state="disabled")
    button_charts.place(relx=0.9, rely=0.74, relwidth=0.08, relheight=0.05)
