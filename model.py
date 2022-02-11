######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     03/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# model development

import gurobipy as gb
from gurobipy import GRB, quicksum

from solution import update_solution


class DistributionSystemModel(object):
    def __init__(self, system):
        self.name = system.name
        self.model = gb.Model(system.name)
        self.modelSense = gb.GRB.MINIMIZE
        self.model.setParam('LogToConsole', 0)

        # variables
        self.active_generation = self.model.addVars(system.numGenerators, lb=0, vtype=GRB.CONTINUOUS,
                                                    name=f"Active_Generation")
        self.reactive_generation = self.model.addVars(system.numGenerators, lb=0, vtype=GRB.CONTINUOUS,
                                                      name=f"Reactive_Generation")
        self.active_load = self.model.addVars(system.numLoads, lb=0, vtype=GRB.CONTINUOUS, name=f"Active_Load")
        self.reactive_load = self.model.addVars(system.numLoads, lb=0, vtype=GRB.CONTINUOUS, name=f"Reactive_Load")
        self.bus_voltage = self.model.addMVar(system.numBuses, lb=0, vtype=GRB.CONTINUOUS, name=f"Bus_Voltage")
        self.line_susceptance = self.model.addMVar(system.numLines, lb=0, vtype=GRB.CONTINUOUS,
                                                   name=f"Line_Susceptance")
        self.line_conductance = self.model.addMVar(system.numLines, lb=0, vtype=GRB.CONTINUOUS,
                                                   name=f"Line_Conductance")
        self.model.update()

        # objective function
        self.model.setObjective(quicksum(system.generators[i].cost * self.active_generation[i]**2
                                         for i in self.active_generation)
                                - system.VOLL * (quicksum(self.active_load[i] for i in self.active_load)))

        # constraints
        for b in range(system.numBuses):
            expression = quicksum(self.active_generation[g] if system.generators[g].bus == b + 1 else 0
                                  for g in range(system.numGenerators)) \
                - quicksum(self.active_load[d] if system.loads[d].bus == b+1 else 0 for d in range(system.numLoads)) \
                - quicksum(system.lines[e].conductance * self.line_conductance[e] if system.lines[e].source == b+1
                           else 0 for e in range(system.numLines)) \
                + quicksum(system.lines[e].susceptance * self.line_susceptance[e] if system.lines[e].source == b+1
                           else 0 for e in range(system.numLines)) \
                - quicksum(system.lines[e].conductance * self.line_conductance[e] if system.lines[e].destination == b+1
                           else 0 for e in range(system.numLines)) \
                + quicksum(system.lines[e].susceptance * self.line_susceptance[e] if system.lines[e].destination == b+1
                           else 0 for e in range(system.numLines)) \
                - system.buses[b].conductance * self.bus_voltage[b]

            self.model.addConstr(expression == 0, name=f"Active_Flow_Balance[{b}]")

            expression = quicksum(self.reactive_generation[g] if system.generators[g].bus == b + 1 else 0
                                  for g in range(system.numGenerators)) \
                - quicksum(self.reactive_load[d] if system.loads[d].bus == b+1 else 0 for d in range(system.numLoads)) \
                + quicksum(system.lines[e].susceptance * self.line_conductance[e] if system.lines[e].source == b+1
                           else 0 for e in range(system.numLines)) \
                + quicksum(system.lines[e].conductance * self.line_susceptance[e] if system.lines[e].source == b+1
                           else 0 for e in range(system.numLines)) \
                - quicksum(system.lines[e].susceptance * self.line_conductance[e] if system.lines[e].destination == b+1
                           else 0 for e in range(system.numLines)) \
                - quicksum(system.lines[e].conductance * self.line_susceptance[e] if system.lines[e].destination == b+1
                           else 0 for e in range(system.numLines)) \
                + system.buses[b].susceptance * self.bus_voltage[b]

            self.model.addConstr(expression == 0, name=f"Reactive_Flow_Balance[{b}]")

            self.model.addConstr((self.bus_voltage[b] >= system.buses[b].min_voltage ** 2), name=f'Min_Bus_voltage[{b}]')
            self.model.addConstr((self.bus_voltage[b] <= system.buses[b].max_voltage ** 2), name=f'Max_Bus_voltage[{b}]')

        self.model.addConstrs((self.active_generation[g] >= system.generators[g].active_min for g in self.active_generation),
                              name="Active_Generation_Min")
        self.model.addConstrs((self.active_generation[g] <= system.generators[g].active_max for g in self.active_generation),
                              name="Active_Generation_Max")
        self.model.addConstrs((self.reactive_generation[g] >= system.generators[g].reactive_min for g in self.reactive_generation),
                              name="Reactive_Generation_Min")
        self.model.addConstrs((self.reactive_generation[g] <= system.generators[g].reactive_max for g in self.reactive_generation),
                              name="Reactive_Generation_Max")

        self.model.addConstrs((self.active_load[d] <= system.loads[d].active_max for d in self.active_load),
                              name="Active_Load_Max")
        self.model.addConstrs((self.reactive_load[d] <= system.loads[d].reactive_max for d in self.active_load),
                              name="Reactive_Load_Max")

        self.model.addConstrs((self.line_conductance[e] ** 2 + self.line_susceptance[e] ** 2 <=
                               self.bus_voltage[system.lines[e].source-1] * self.bus_voltage[system.lines[e].destination-1]
                               for e in range(system.numLines)), name="SOCP")

        self.model.update()


def model_builder(system, output_dir):

    system_model = DistributionSystemModel(system)
    solution = update_solution(system_model)

    return solution
