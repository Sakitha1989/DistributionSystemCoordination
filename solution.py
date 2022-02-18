######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# solution class to store solutions

import copy

from utilities import compare_solutions
from print import distribution_solution_writer


class DistributionSystemSolution(object):
    def __init__(self):
        self.name = ''
        self.objective_value = None
        self.active_generation = []
        self.reactive_generation = []
        self.active_load = []
        self.reactive_load = []
        self.bus_voltage = []
        self.distribution_line_susceptance = []
        self.distribution_line_conductance = []
        self.active_line_transmission = []
        self.reactive_line_transmission = []
        self.comparison_test = None

    def clear(self):
        self.name = ''
        self.objective_value = None
        self.active_generation = []
        self.reactive_generation = []
        self.active_load = []
        self.reactive_load = []
        self.bus_voltage = []
        self.distribution_line_susceptance = []
        self.distribution_line_conductance = []
        self.active_line_transmission = []
        self.reactive_line_transmission = []
        self.comparison_test = None

    def update_distribution_system_solution(self, model, header):

        previous_solution = copy.deepcopy(self)
        self.clear()

        self.name = model.name

        model.model.optimize()
        print(model.model.status)
        self.objective_value = model.model.getObjective().getValue()
        for v in model.model.getVars():
            if 'Active_Generation' in v.varName:
                self.active_generation.append(v.x)
            elif 'Reactive_Generation' in v.varName:
                self.reactive_generation.append(v.x)
            elif 'Active_Load' in v.varName:
                self.active_load.append(v.x)
            elif 'Reactive_Load' in v.varName:
                self.reactive_load.append(v.x)
            elif 'Bus_Voltage' in v.varName:
                self.bus_voltage.append(v.x)
            elif 'Distribution_Line_Susceptance' in v.varName:
                self.distribution_line_susceptance.append(v.x)
            elif 'Distribution_Line_Conductance' in v.varName:
                self.distribution_line_conductance.append(v.x)
            elif 'Active_Line_Transmission' in v.varName:
                self.active_line_transmission.append(v.x)
            elif 'Reactive_Line_Transmission' in v.varName:
                self.reactive_line_transmission.append(v.x)

        if not header == 0:
            self.comparison_test = compare_solutions(previous_solution, self)

        distribution_solution_writer(model, header)


class TransmissionSolution(object):
    def __init__(self, num_buses):
        self.capacity_at_bus = [0] * num_buses

    def update_transmission_system_solution(self, distribution_solution, transmission_system,
                                            distribution_system):

        for busId in range(len(self.capacity_at_bus)):
            for lineId in range(len(distribution_solution.active_line_transmission)):
                if transmission_system.buses[busId].id == distribution_system.transmission_lines[lineId].destination:
                    self.capacity_at_bus[busId] += distribution_solution.active_line_transmission[
                        lineId]
