######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# solution class to store solutions

import csv
from csv import writer


class DistributionSystemSolution(object):
    def __init__(self):
        self.name = ''
        self.objective_value = []
        self.active_generation = []
        self.reactive_generation = []
        self.active_load = []
        self.reactive_load = []
        self.bus_voltage = []
        self.distribution_line_susceptance = []
        self.distribution_line_conductance = []
        self.transmission_line_susceptance = []
        self.transmission_line_conductance = []

    def clear(self):
        self.name = ''
        self.objective_value = []
        self.active_generation = []
        self.reactive_generation = []
        self.active_load = []
        self.reactive_load = []
        self.bus_voltage = []
        self.distribution_line_susceptance = []
        self.distribution_line_conductance = []
        self.transmission_line_susceptance = []
        self.transmission_line_conductance = []


class TransmissionSolution(object):
    def __init__(self, num_buses):
        self.capacity_at_bus = [0] * num_buses


def distribution_solution_writer(model, header):

    column_names = []
    data = []
    for v in model.model.getVars():
        if header == 0:
            column_names.append(v.varName)
        data.append(v.x)

    # file path and name
    file = model.name + ".csv"

    if header == 0:
        # writing to csv file
        with open(file, 'w', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(column_names)

    # writing to existing csv file
    with open(file, 'a', newline='') as f_object:
        # creating a csv writer object
        writer_object = writer(f_object)

        writer_object.writerow(data)
        f_object.close()


def update_distribution_system_solution(solution, model, header):

    solution.clear()

    solution.name = model.name

    model.model.optimize()
    solution.objective_value = model.model.getObjective().getValue()
    for v in model.model.getVars():
        if 'Active_Generation' in v.varName:
            solution.active_generation.append(v.x)
        elif 'Reactive_Generation' in v.varName:
            solution.reactive_generation.append(v.x)
        elif 'Active_Load' in v.varName:
            solution.active_load.append(v.x)
        elif 'Reactive_Load' in v.varName:
            solution.reactive_load.append(v.x)
        elif 'Bus_Voltage' in v.varName:
            solution.bus_voltage.append(v.x)
        elif 'Distribution_Line_Susceptance' in v.varName:
            solution.distribution_line_susceptance.append(v.x)
        elif 'Distribution_Line_Conductance' in v.varName:
            solution.distribution_line_conductance.append(v.x)
        elif 'Transmission_Line_Susceptance' in v.varName:
            solution.transmission_line_susceptance.append(v.x)
        elif 'Transmission_Line_Conductance' in v.varName:
            solution.transmission_line_conductance.append(v.x)

    distribution_solution_writer(model, header)

    return solution


def update_transmission_system_solution(transmission_solution, distribution_solution, transmission_system, distribution_system):

    for busId in range(len(transmission_solution.capacity_at_bus)):
        for lineId in range(len(distribution_solution.transmission_line_conductance)):
            if transmission_system.buses[busId].id == distribution_system.transmission_lines[lineId].destination:
                transmission_solution.capacity_at_bus[busId] += distribution_solution.transmission_line_susceptance[lineId]

    return transmission_solution
