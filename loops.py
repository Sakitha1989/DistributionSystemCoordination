######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     03/08/2022
# Project:  Distribution system coordination
######################################################################################################################

import os
import time

import numpy as np
import numpy.random

from model import DistributionSystemModel
from readingData import DistributionSystem, TransmissionSystem
from solution import DistributionSystemSolution, TransmissionSolution
from GUI import *


def read_system_data(input_dir, system_name, num_systems):

    distribution_system = [DistributionSystem] * num_systems

    for system_number in range(num_systems):
        if not os.path.exists(input_dir + system_name + f"{system_number + 1}\\"):
            print(f"{system_name + str(system_number + 1)} does not exists!")
        else:
            file_path = input_dir + system_name + f"{system_number + 1}\\"
            distribution_system[system_number] = DistributionSystem(system_name + f"{system_number + 1}")
            distribution_system[system_number].create_distribution_system(file_path)

    return distribution_system


def main_loop(distribution_system, input_dir, network_name, num_systems, num_iterations, deviation_penalty, tolerance):

    probability_list = np.random.dirichlet(np.ones(num_systems), size=1)
    system_list = list(np.arange(0, num_systems))
    # system_list = [x for _, x in sorted(zip(probability_list[0], system_list), reverse=True)]

    total_cost = []

    # transmission system attributes
    transmission_system = TransmissionSystem(network_name)
    transmission_system.create_transmission_system(input_dir)
    transmission_system_solution = TransmissionSolution(transmission_system.numBuses)

    # distribution systems attributes
    distribution_system_model = [DistributionSystemModel] * num_systems
    distribution_system_solution = [DistributionSystemSolution] * num_systems
    temporary_distribution_system_solution = DistributionSystemSolution()
    start = time.process_time()

    for iteration_count in range(num_iterations):

        cost = 0
        comparison = []

        for system_number in system_list:

            if iteration_count == 0:
                distribution_system_solution[system_number] = DistributionSystemSolution()
                distribution_system_model[system_number] = DistributionSystemModel(distribution_system[system_number])
                distribution_system_solution[system_number].update_distribution_system_solution(distribution_system_model[system_number], iteration_count, tolerance)
                cost += distribution_system_solution[system_number].objective_value

            else:
                transmission_system_solution.update_transmission_system_solution(transmission_system, distribution_system[system_number], distribution_system_solution[system_number], False)
                distribution_system_model[system_number].update_distribution_system_model(distribution_system[system_number], distribution_system_solution[system_number], transmission_system, transmission_system_solution, deviation_penalty)
                distribution_system_solution[system_number].update_distribution_system_solution(distribution_system_model[system_number], iteration_count, tolerance)
                cost += distribution_system_solution[system_number].objective_value

            transmission_system_solution.update_transmission_system_solution(transmission_system, distribution_system[system_number], distribution_system_solution[system_number], True)
            comparison.append(distribution_system_solution[system_number].comparison_test)

        total_cost.append(cost)

        if all(comparison):
            break

    return {"iteration_count": iteration_count, "total_cost": total_cost}
