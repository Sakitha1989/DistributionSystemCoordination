######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/16/2022
# Project:  Distribution system coordination
######################################################################################################################

import csv
from csv import writer


def distribution_solution_writer(model, header):

    column_names = ['Objective_Function_Value']
    data = [model.model.getObjective().getValue()]
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


def print_distribution_system_details(system):
    print_single_line()
    print(f"System name: {system.name}")
    print(f"Number of buses = {system.numBuses}")
    print(f"Number of generators = {system.numGenerators}")
    print(f"Number of loads = {system.numLoads}")
    print(f"Number of distribution lines = {system.numDistributionLines}")
    print(f"Number of transmission lines = {system.numTransmissionLines}")


def print_results(iteration_count, total_cost):
    print_double_line()
    print(f"Iteration count: {iteration_count + 1}")
    print(f"Total cost gap: {(total_cost[iteration_count - 1] - total_cost[iteration_count]) / total_cost[iteration_count - 1]}")
    print(f"Total cost: {total_cost[iteration_count]}")


def print_single_line():
    print('─' * 20)


def print_double_line():
    print('=' * 20)
