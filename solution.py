######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# solution class to store solutions

import csv
from csv import writer


class Solution(object):
    def __init__(self, name):
        self.name = name
        self.objective_value = []
        self.active_generation = []
        self.reactive_generation = []
        self.active_load = []
        self.reactive_load = []
        self.bus_voltage = []
        self.line_susceptance = []
        self.line_conductance = []


def solution_writer(model, header):
    column_names = []
    if header:
        column_names = []
    data = []
    for v in model.model.getVars():
        if header:
            column_names.append(v.varName)
        data.append(v.x)

    # file path and name
    file = "C:\\Users\\sakit\\Documents\\Academic\\Research\\CoordinationSystem\\CoordinationDisSys\\outputData" \
           "\\Test\\" + model.name + ".csv"

    if header:
        # writing to csv file
        with open(file, 'w', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(column_names)

    # writing to existing csv file
    with open(file, 'a') as f_object:
        # creating a csv writer object
        writer_object = writer(f_object)

        writer_object.writerow(data)
        f_object.close()


def update_solution(model):
    system_solution = Solution(model.name)

    model.model.optimize()
    system_solution.objective_value = model.model.getObjective().getValue()
    for v in model.model.getVars():
        if 'Active_Generation' in v.varName:
            system_solution.active_generation.append(v.x)
        elif 'Reactive_Generation' in v.varName:
            system_solution.reactive_generation.append(v.x)
        elif 'Active_Load' in v.varName:
            system_solution.active_load.append(v.x)
        elif 'Reactive_Load' in v.varName:
            system_solution.reactive_load.append(v.x)
        elif 'Bus_Voltage' in v.varName:
            system_solution.bus_voltage.append(v.x)
        elif 'Line_Susceptance' in v.varName:
            system_solution.line_susceptance.append(v.x)
        elif 'Line_Conductance' in v.varName:
            system_solution.line_conductance.append(v.x)

    solution_writer(model, True)

    return system_solution
