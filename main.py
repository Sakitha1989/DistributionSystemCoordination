######################################################################################################################
# Author:   Sakitha Ariyarathne
# Date:     02/08/2022
# Project:  Distribution system coordination
######################################################################################################################

# Need two command line inputs;
#           1. Directory path
#           2. System name
#
# The script assumes that there are 'inputData' and 'outputData' folders exist inside the directory. Also, inside the
# 'inputData' folder there must be folder for the system containing all the data files.

import os
import sys

import numpy as np
import numpy.random

from model import DistributionSystemModel
from readingData import DistributionSystem, TransmissionSystem
from solution import DistributionSystemSolution, TransmissionSolution

np.random.seed(10)

# default inputs if not provided
directory = "C:\\Users\\sakit\\Documents\\Academic\\Research\\CoordinationSystem\\CoordinationDisSys\\"
network_name = "Test"
system_name = "System1"
num_systems = 2
num_iterations = 2
input_dir = ""
output_dir = ""


def cmdinputs() -> None:
    global directory, network_name, system_name, num_systems, num_iterations, input_dir, output_dir

    if len(sys.argv) >= 2:
        if not os.path.exists(sys.argv[1]):
            print(f"{sys.argv[1]}, Directory does not exists!")
            sys.exit()
        else:
            directory = sys.argv[1]
            input_dir = directory + "inputData\\"
            if len(sys.argv) >= 3:
                if not os.path.exists(input_dir + sys.argv[2] + "\\"):
                    print(f"{sys.argv[2]} network does not exists!")
                    sys.exit()
                else:
                    network_name = sys.argv[2]
                    input_dir = input_dir + network_name + "\\"
                if len(sys.argv) >= 4:
                    system_name = sys.argv[3]
                    if len(sys.argv) >= 5:
                        if len(os.listdir(input_dir))-1 >= int(sys.argv[4]):
                            num_systems = int(sys.argv[4])
                        else:
                            print(f"Invalid number of systems! The program will run for the available number of systems, {len(os.listdir(input_dir))-1}.")
                            num_systems = len(os.listdir(input_dir))-1
                        if len(sys.argv) >= 6:
                            num_iterations = int(sys.argv[5])

    output_dir = directory + "outputData\\" + network_name + "\\"

    # Create system folder in the output directory if it does not exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print("Directory: ", output_dir, " Created ")


# reading command line arguments
cmdinputs()

total_cost = []

probability_list = np.random.dirichlet(np.ones(num_systems), size=1)
system_list = list(np.arange(0, num_systems))
system_list = [x for _, x in sorted(zip(probability_list[0], system_list), reverse=True)]

# transmission system attributes
transmission_system = TransmissionSystem(network_name)
transmission_system.create_transmission_system(input_dir)
transmission_system_solution = TransmissionSolution(transmission_system.numBuses)

# distribution systems attributes
distribution_system = [DistributionSystem] * num_systems
distribution_system_model = [DistributionSystemModel] * num_systems
distribution_system_solution = [DistributionSystemSolution] * num_systems
temporary_distribution_system_solution = DistributionSystemSolution()

for iteration_count in range(num_iterations):

    cost = 0
    comparison = []

    for system_number in system_list:

        if iteration_count == 0:
            if not os.path.exists(input_dir + system_name + f"{system_number+1}\\"):
                print(f"{system_name + str(system_number+1)} does not exists!")
                sys.exit()
            else:
                file_path = input_dir + system_name + f"{system_number+1}\\"
                distribution_system[system_number] = DistributionSystem(system_name + f"{system_number+1}")
                distribution_system[system_number].create_distribution_system(file_path)

                distribution_system_solution[system_number] = DistributionSystemSolution()
                distribution_system_model[system_number] = DistributionSystemModel(distribution_system[system_number])
                distribution_system_solution[system_number].update_distribution_system_solution(distribution_system_model[system_number], iteration_count)
                cost += distribution_system_solution[system_number].objective_value

        else:
            transmission_system_solution.update_transmission_system_solution(transmission_system, distribution_system[system_number],
                                                                             distribution_system_solution[system_number], False)
            distribution_system_model[system_number].update_distribution_system_model(distribution_system[system_number],
                                                                                        distribution_system_solution[system_number], transmission_system, transmission_system_solution)
            distribution_system_solution[system_number].update_distribution_system_solution(distribution_system_model[system_number], iteration_count)
            cost += distribution_system_solution[system_number].objective_value

        transmission_system_solution.update_transmission_system_solution(transmission_system, distribution_system[system_number],
                                                                         distribution_system_solution[system_number], True)

    total_cost.append(cost)
    comparison.append(distribution_system_solution[system_number].comparison_test)

    if all(comparison):
        print("No improvement from previous solution!")
        break

print(f"Iteration count: {iteration_count+1}")
print(f"Total cost gap: {(total_cost[iteration_count-1] - total_cost[iteration_count])/total_cost[iteration_count-1]}")
print(f"Total cost: {total_cost[iteration_count]}")
