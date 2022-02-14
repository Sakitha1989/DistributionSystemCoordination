######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     03/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# model development

import gurobipy as gb
from gurobipy import GRB, quicksum


class DistributionSystemModel(object):
    def __init__(self, distribution_system, transmission_system, transmission_system_solution):
        self.name = distribution_system.name
        self.model = gb.Model(distribution_system.name)
        self.modelSense = gb.GRB.MINIMIZE
        self.model.setParam('LogToConsole', 0)

        # variables
        self.active_generation = self.model.addVars(distribution_system.numGenerators, lb=0, vtype=GRB.CONTINUOUS,
                                                    name=f"Active_Generation")
        self.reactive_generation = self.model.addVars(distribution_system.numGenerators, lb=0, vtype=GRB.CONTINUOUS,
                                                      name=f"Reactive_Generation")
        self.active_load = self.model.addVars(distribution_system.numLoads, lb=0, vtype=GRB.CONTINUOUS, name=f"Active_Load")
        self.reactive_load = self.model.addVars(distribution_system.numLoads, lb=0, vtype=GRB.CONTINUOUS, name=f"Reactive_Load")
        self.bus_voltage = self.model.addMVar(distribution_system.numBuses, lb=0, vtype=GRB.CONTINUOUS, name=f"Bus_Voltage")
        self.distribution_line_susceptance = self.model.addMVar(distribution_system.numDistributionLines, lb=0, vtype=GRB.CONTINUOUS,
                                                                name=f"Distribution_Line_Susceptance")
        self.distribution_line_conductance = self.model.addMVar(distribution_system.numDistributionLines, lb=0, vtype=GRB.CONTINUOUS,
                                                                name=f"Distribution_Line_Conductance")
        self.transmission_line_susceptance = self.model.addMVar(distribution_system.numTransmissionLines, lb=0, vtype=GRB.CONTINUOUS,
                                                                name=f"Transmission_Line_Susceptance")
        self.transmission_line_conductance = self.model.addMVar(distribution_system.numTransmissionLines, lb=0, vtype=GRB.CONTINUOUS,
                                                                name=f"Transmission_Line_Conductance")
        self.model.update()

        # objective function
        expression = 0
        for i in range(distribution_system.numTransmissionLines):
            expression += quicksum(transmission_system.bus_constant*(self.transmission_line_susceptance[i]**2) +
              transmission_system_solution.capacity_at_bus[t]*self.transmission_line_susceptance[i]
              if distribution_system.transmission_lines[i].destination == transmission_system.buses[t].id else 0
              for t in range(transmission_system.numBuses))

        self.model.setObjective(quicksum(distribution_system.generators[i].cost * self.active_generation[i] for i in self.active_generation)
                                - distribution_system.VOLL * (quicksum(self.active_load[i] for i in self.active_load)) + expression)

        # constraints
        for b in range(distribution_system.numBuses):
            expression = quicksum(self.active_generation[g] if distribution_system.generators[g].bus == b + 1 else 0
                                  for g in range(distribution_system.numGenerators)) \
                - quicksum(self.active_load[d] if distribution_system.loads[d].bus == b+1 else 0 for d in range(distribution_system.numLoads)) \
                - quicksum(distribution_system.distribution_lines[e].conductance * self.distribution_line_conductance[e]
                           if distribution_system.distribution_lines[e].source == b+1 else 0 for e in range(distribution_system.numDistributionLines)) \
                + quicksum(distribution_system.distribution_lines[e].susceptance * self.distribution_line_susceptance[e]
                           if distribution_system.distribution_lines[e].source == b+1 else 0 for e in range(distribution_system.numDistributionLines)) \
                - quicksum(distribution_system.distribution_lines[e].conductance * self.distribution_line_conductance[e]
                           if distribution_system.distribution_lines[e].destination == b+1 else 0 for e in range(distribution_system.numDistributionLines)) \
                + quicksum(distribution_system.distribution_lines[e].susceptance * self.distribution_line_susceptance[e]
                           if distribution_system.distribution_lines[e].destination == b+1 else 0 for e in range(distribution_system.numDistributionLines)) \
                - quicksum(distribution_system.transmission_lines[e].conductance * self.transmission_line_conductance[e]
                           if distribution_system.transmission_lines[e].source == b + 1 else 0 for e in range(distribution_system.numTransmissionLines)) \
                + quicksum(distribution_system.transmission_lines[e].susceptance * self.transmission_line_susceptance[e]
                           if distribution_system.transmission_lines[e].source == b + 1 else 0 for e in range(distribution_system.numTransmissionLines)) \
                - quicksum(distribution_system.transmission_lines[e].conductance * self.transmission_line_conductance[e]
                           if distribution_system.transmission_lines[e].destination == b + 1 else 0 for e in range(distribution_system.numTransmissionLines)) \
                + quicksum(distribution_system.transmission_lines[e].susceptance * self.transmission_line_susceptance[e]
                           if distribution_system.transmission_lines[e].destination == b + 1 else 0 for e in range(distribution_system.numTransmissionLines)) \
                - distribution_system.buses[b].conductance * self.bus_voltage[b]

            self.model.addConstr(expression == 0, name=f"Active_Flow_Balance[{b}]")

            expression = quicksum(self.reactive_generation[g] if distribution_system.generators[g].bus == b + 1 else 0
                                  for g in range(distribution_system.numGenerators)) \
                - quicksum(self.reactive_load[d] if distribution_system.loads[d].bus == b+1 else 0 for d in range(distribution_system.numLoads)) \
                + quicksum(distribution_system.distribution_lines[e].susceptance * self.distribution_line_conductance[e]
                           if distribution_system.distribution_lines[e].source == b+1 else 0 for e in range(distribution_system.numDistributionLines)) \
                + quicksum(distribution_system.distribution_lines[e].conductance * self.distribution_line_susceptance[e]
                           if distribution_system.distribution_lines[e].source == b+1 else 0 for e in range(distribution_system.numDistributionLines)) \
                - quicksum(distribution_system.distribution_lines[e].susceptance * self.distribution_line_conductance[e]
                           if distribution_system.distribution_lines[e].destination == b+1 else 0 for e in range(distribution_system.numDistributionLines)) \
                - quicksum(distribution_system.distribution_lines[e].conductance * self.distribution_line_susceptance[e]
                           if distribution_system.distribution_lines[e].destination == b+1 else 0 for e in range(distribution_system.numDistributionLines)) \
                + quicksum(distribution_system.transmission_lines[e].susceptance * self.distribution_line_conductance[e]
                           if distribution_system.transmission_lines[e].source == b + 1 else 0 for e in range(distribution_system.numTransmissionLines)) \
                + quicksum(distribution_system.transmission_lines[e].conductance * self.distribution_line_susceptance[e]
                           if distribution_system.transmission_lines[e].source == b + 1 else 0 for e in range(distribution_system.numTransmissionLines)) \
                - quicksum(distribution_system.transmission_lines[e].susceptance * self.distribution_line_conductance[e]
                           if distribution_system.transmission_lines[e].destination == b + 1 else 0 for e in range(distribution_system.numTransmissionLines)) \
                - quicksum(distribution_system.transmission_lines[e].conductance * self.distribution_line_susceptance[e]
                           if distribution_system.transmission_lines[e].destination == b + 1 else 0 for e in range(distribution_system.numTransmissionLines)) \
                + distribution_system.buses[b].susceptance * self.bus_voltage[b]

            self.model.addConstr(expression == 0, name=f"Reactive_Flow_Balance[{b}]")

            self.model.addConstr((self.bus_voltage[b] >= distribution_system.buses[b].min_voltage ** 2), name=f'Min_Bus_voltage[{b}]')
            self.model.addConstr((self.bus_voltage[b] <= distribution_system.buses[b].max_voltage ** 2), name=f'Max_Bus_voltage[{b}]')

        self.model.addConstrs((self.active_generation[g] >= distribution_system.generators[g].active_min for g in self.active_generation),
                              name="Active_Generation_Min")
        self.model.addConstrs((self.active_generation[g] <= distribution_system.generators[g].active_max for g in self.active_generation),
                              name="Active_Generation_Max")
        self.model.addConstrs((self.reactive_generation[g] >= distribution_system.generators[g].reactive_min for g in self.reactive_generation),
                              name="Reactive_Generation_Min")
        self.model.addConstrs((self.reactive_generation[g] <= distribution_system.generators[g].reactive_max for g in self.reactive_generation),
                              name="Reactive_Generation_Max")

        self.model.addConstrs((self.active_load[d] <= distribution_system.loads[d].active_max for d in self.active_load),
                              name="Active_Load_Max")
        self.model.addConstrs((self.reactive_load[d] <= distribution_system.loads[d].reactive_max for d in self.active_load),
                              name="Reactive_Load_Max")

        self.model.addConstrs((self.distribution_line_conductance[e] ** 2 + self.distribution_line_susceptance[e] ** 2 -
                    self.bus_voltage[distribution_system.distribution_lines[e].source-1] * self.bus_voltage[distribution_system.distribution_lines[e].destination-1] <= 0
                    for e in range(distribution_system.numDistributionLines)), name="SOCP")

        self.model.update()
        self.model.write(self.name + '.lp')


def create_distribution_system_model(distribution_system, transmission_system, transmission_system_solution):

    system_model = DistributionSystemModel(distribution_system, transmission_system, transmission_system_solution)

    return system_model


def update_distribution_system_model(model, distribution_system, transmission_system, transmission_system_solution):

    # objective function
    for i in range(distribution_system.numTransmissionLines):
        for t in range(transmission_system.numBuses):
            if distribution_system.transmission_lines[i].destination == transmission_system.buses[t].id:
                model.transmission_line_susceptance[i].Obj = transmission_system_solution.capacity_at_bus[t]

    # TODO: expression for true flow through transmission line
    # TODO: setting up quadratic term for the deviations

    return model
